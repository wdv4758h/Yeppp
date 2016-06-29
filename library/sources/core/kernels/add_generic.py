from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.avx_instruction_maps import * # The correct instructions to use depending on argument type
from instruction_maps.sse_instruction_maps import *
from common.YepStatus import *
from common.pipeline import software_pipelined_loop

def avx_scalar_instruction_select(input_type, output_type):
    # Choose the scalar load instruction.
    # The special case is 32u -> 64u, as there is no zero-extension
    # instruction, we have to cast the register from 64 bit to 32 bit.
    if input_type == Yep32u and output_type == Yep64u:
        SCALAR_LOAD = lambda x, y: MOV(x.as_dword, y)
    elif input_type.size == output_type.size:
        SCALAR_LOAD = avx_scalar_mov_map[input_type]
    else:
        SCALAR_LOAD = avx_scalar_movsx_map[(input_type, output_type)]

    # We don't want to have to worry about the order of operands if we
    # use the generic add instruction
    if output_type in [Yep8s, Yep8u, Yep16s, Yep16u, Yep32s, Yep32u,
            Yep64s, Yep64u]:
        SCALAR_ADD = lambda x, y, z: avx_scalar_add_map[output_type](x, z) \
            if x == y else avx_scalar_add_map[output_type](x, y)
    else:
        SCALAR_ADD = lambda x, y, z: avx_scalar_add_map[output_type](x, y, z)

    SCALAR_STORE = avx_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE

def avx_vector_instruction_select(input_type, output_type):
    if input_type.size == output_type.size:
        SIMD_LOAD = avx_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = avx_vector_movsx_map[(input_type, output_type)]

    SIMD_ADD = avx_vector_add_map[output_type]
    SIMD_STORE = avx_vector_aligned_mov_map[output_type]

    if input_type.size != output_type.size:
        UNPACK = avx_high_unpack_map[(input_type, output_type)]
    else:
        UNPACK = None
    return SIMD_LOAD, SIMD_ADD, SIMD_STORE, UNPACK

def sse_scalar_instruction_select(input_type, output_type):
    # Choose the scalar load instruction.
    # The special case is 32u -> 64u, as there is no zero-extension
    # instruction, we have to cast the register from 64 bit to 32 bit.
    if input_type == Yep32u and output_type == Yep64u:
        SCALAR_LOAD = lambda x, y: MOV(x.as_dword, y)
    elif input_type.size == output_type.size:
        SCALAR_LOAD = sse_scalar_mov_map[input_type]
    else:
        SCALAR_LOAD = sse_scalar_movsx_map[(input_type, output_type)]

    # We don't want to have to worry about the order of operands if we
    # use the generic add instruction
    SCALAR_ADD = lambda x, y, z: sse_scalar_add_map[output_type](x, z) \
        if x == y else sse_scalar_add_map[output_type](x, y)

    SCALAR_STORE = sse_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE

def sse_vector_instruction_select(input_type, output_type):
    if input_type.size == output_type.size:
        SIMD_LOAD = sse_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = sse_vector_movsx_map[(input_type, output_type)]

    SIMD_ADD = lambda x, y, z: sse_vector_add_map[output_type](x, z) \
        if x == y else sse_vector_add_map[output_type](x, y)
    SIMD_STORE = sse_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_ADD, SIMD_STORE


def add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, isa_ext):
    """
    Add function which uses avx_add_instruction_maps to execute the addition
    kernel on any type operands.
    """
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_TYPE = arg_z.c_type.base
    INPUT_TYPE_SIZE = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_z.c_type.base.size

    if INPUT_TYPE_SIZE == 1:
        SX_SIZE = byte
    elif INPUT_TYPE_SIZE == 2:
        SX_SIZE = word
    elif INPUT_TYPE_SIZE == 4:
        SX_SIZE = dword
    elif INPUT_TYPE_SIZE == 8:
        SX_SIZE = qword

    UNROLL_FACTOR = 5

    if isa_ext == "avx":
        SIMD_REGISTER_SIZE = YMMRegister.size
        SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE = avx_scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        SIMD_LOAD, SIMD_ADD, SIMD_STORE, _ = avx_vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        reg_x_scalar = avx_scalar_register_map[OUTPUT_TYPE]()
        reg_y_scalar = avx_scalar_register_map[OUTPUT_TYPE]()
        simd_accs = [YMMRegister() for _ in range(UNROLL_FACTOR)]
        simd_ops = [YMMRegister() for _ in range(UNROLL_FACTOR)]
    elif isa_ext == "sse":
        SIMD_REGISTER_SIZE = XMMRegister.size
        SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE = sse_scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        SIMD_LOAD, SIMD_ADD, SIMD_STORE = sse_vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        reg_x_scalar = sse_scalar_register_map[OUTPUT_TYPE]()
        reg_y_scalar = sse_scalar_register_map[OUTPUT_TYPE]()
        simd_accs = [XMMRegister() for _ in range(UNROLL_FACTOR)]
        simd_ops = [XMMRegister() for _ in range(UNROLL_FACTOR)]

    ret_ok = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()

    # Load args and test for null pointers and invalid arguments
    reg_length = GeneralPurposeRegister64() # Keeps track of how many elements are left to process
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_ok) # Check there is at least 1 element to process

    reg_x_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_x_addr, arg_x)
    TEST(reg_x_addr, reg_x_addr) # Make sure arg_x is not null
    JZ(ret_null_pointer)

    reg_y_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_y_addr, arg_y)
    TEST(reg_y_addr, reg_y_addr) # Make sure arg_y is not null
    JZ(ret_null_pointer)

    reg_z_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_z_addr, arg_z)
    TEST(reg_z_addr, reg_z_addr)
    JZ(ret_null_pointer)
    TEST(reg_z_addr, OUTPUT_TYPE_SIZE - 1) # Make sure arg_z is aligned on the proper boundary
    JNZ(ret_misaligned_pointer)


    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on Z addr
    # Process elements 1 at a time until z is aligned on YMMRegister.size boundary
    TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1) # Check if already aligned
    JZ(align_loop.end) # If so, skip this loop entirely
    with align_loop:
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_LOAD(reg_y_scalar, SX_SIZE[reg_y_addr])
        SCALAR_ADD(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        ADD(reg_y_addr, INPUT_TYPE_SIZE)
        ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1)
        JNZ(align_loop.begin)

    # Batch loop for processing the rest of the array in a pipelined loop
    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2, 3)
    for i in range(UNROLL_FACTOR):
        with instruction_columns[0]:
            SIMD_LOAD(simd_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[1]:
            SIMD_LOAD(simd_ops[i], [reg_y_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[2]:
            SIMD_ADD(simd_accs[i], simd_accs[i], simd_ops[i])
        with instruction_columns[3]:
            SIMD_STORE([reg_z_addr + i * SIMD_REGISTER_SIZE], simd_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[1]:
        ADD(reg_y_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[3]:
        ADD(reg_z_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR)

    software_pipelined_loop(reg_length, UNROLL_FACTOR * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

    # Check if there are leftover elements that were not processed in the pipelined loop
    # This loop should iterate at most #(elems processed per iteration in the batch loop) - 1 times
    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop: # Process the remaining elements
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_LOAD(reg_y_scalar, SX_SIZE[reg_y_addr])
        SCALAR_ADD(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        ADD(reg_y_addr, INPUT_TYPE_SIZE)
        ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatusMisalignedPointer)


def add_vector_to_scalar_generic(arg_x, arg_y, arg_z, arg_n, isa_ext):
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_TYPE = arg_z.c_type.base
    INPUT_TYPE_SIZE = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_z.c_type.base.size

    if INPUT_TYPE_SIZE == 1:
        SX_SIZE = byte
    elif INPUT_TYPE_SIZE == 2:
        SX_SIZE = word
    elif INPUT_TYPE_SIZE == 4:
        SX_SIZE = dword
    elif INPUT_TYPE_SIZE == 8:
        SX_SIZE = qword

    UNROLL_FACTOR = 5

    if isa_ext == "avx":
        SIMD_REGISTER_SIZE = YMMRegister.size
        SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE = avx_scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        SIMD_LOAD, SIMD_ADD, SIMD_STORE, UNPACK = avx_vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        reg_x_scalar = avx_scalar_register_map[OUTPUT_TYPE]()
        reg_y_scalar = avx_scalar_register_map[OUTPUT_TYPE]()
        reg_y_vector = YMMRegister()
        simd_accs = [YMMRegister() for _ in range(UNROLL_FACTOR)]
    elif isa_ext == "sse":
        SIMD_REGISTER_SIZE = XMMRegister.size
        SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE = sse_scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        SIMD_LOAD, SIMD_ADD, SIMD_STORE = sse_vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        reg_x_scalar = sse_scalar_register_map[OUTPUT_TYPE]()
        reg_y_scalar = sse_scalar_register_map[OUTPUT_TYPE]()
        reg_y_vector = XMMRegister()
        simd_accs = [XMMRegister() for _ in range(UNROLL_FACTOR)]

    ret_ok = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()

    # Load args and test for null pointers and invalid arguments
    reg_length = GeneralPurposeRegister64() # Keeps track of how many elements are left to process
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_ok) # Check there is at least 1 element to process

    reg_x_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_x_addr, arg_x)
    TEST(reg_x_addr, reg_x_addr) # Make sure arg_x is not null
    JZ(ret_null_pointer)

    LOAD.ARGUMENT(reg_y_scalar, arg_y)

    reg_z_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_z_addr, arg_z)
    TEST(reg_z_addr, reg_z_addr)
    JZ(ret_null_pointer)
    TEST(reg_z_addr, OUTPUT_TYPE_SIZE - 1) # Make sure arg_z is aligned on the proper boundary
    JNZ(ret_misaligned_pointer)


    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on Z addr
    # Process elements 1 at a time until z is aligned on YMMRegister.size boundary
    TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1) # Check if already aligned
    JZ(align_loop.end) # If so, skip this loop entirely
    with align_loop:
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_ADD(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1)
        JNZ(align_loop.begin)

    # Batch loop for processing the rest of the array in a pipelined loop
    # MOVQ(reg_y_vector, reg_y_scalar)
    # UNPACK(reg_y_vector, reg_y_vector)
    # instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()]
    # instruction_offsets = (0, 1, 2)
    # for i in range(UNROLL_FACTOR):
    #     with instruction_columns[0]:
    #         SIMD_LOAD(simd_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
    #     with instruction_columns[1]:
    #         SIMD_ADD(simd_accs[i], simd_accs[i], reg_y_vector)
    #     with instruction_columns[2]:
    #         SIMD_STORE([reg_z_addr + i * SIMD_REGISTER_SIZE], simd_accs[i])
    # with instruction_columns[0]:
    #     ADD(reg_x_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    # with instruction_columns[2]:
    #     ADD(reg_z_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR)

    # software_pipelined_loop(reg_length, UNROLL_FACTOR * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

    # # Check if there are leftover elements that were not processed in the pipelined loop
    # # This loop should iterate at most #(elems processed per iteration in the batch loop) - 1 times
    # TEST(reg_length, reg_length)
    # JZ(scalar_loop.end)
    # with scalar_loop: # Process the remaining elements
    #     SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
    #     SCALAR_ADD(reg_x_scalar, reg_x_scalar, reg_y_scalar)
    #     SCALAR_STORE([reg_z_addr], reg_x_scalar)
    #     ADD(reg_x_addr, INPUT_TYPE_SIZE)
    #     ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
    #     SUB(reg_length, 1)
    #     JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatusMisalignedPointer)
