from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.avx_add_instruction_maps import * # The correct instructions to use depending on argument type
from common.YepStatus import *
from common.pipeline import software_pipelined_loop

def scalar_mov_instr_select(input_type, output_type):
    """
    Selects the correct move instruction depending on operand type.
    Chooses SX / ZX instructions if necessary.
    """
    if input_type.size == output_type.size:
        return scalar_move_map[input_type]
    else: # Must sign-extend on the move
        return scalar_movsx_map[(input_type, output_type)]

def packed_mov_instr_select(input_type, output_type):
    """
    Selects the correct move instruction for packed operands depending on type.
    Chooses SX / ZX instructions if necessary
    """
    if input_type.size == output_type.size:
        return packed_unaligned_move_map[input_type]
    else:
        return packed_movsx_map[(input_type, output_type)]

def add_generic(arg_x, arg_y, arg_z, arg_n):
    """
    Add function which uses avx_add_instruction_maps to execute the addition
    kernel on any type operands.
    """
    INPUT_TYPE_SIZE = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_z.c_type.base.size
    SIMD_REGISTER_SIZE = YMMRegister.size

    if arg_x.c_type.base == Yep32u and arg_z.c_type.base == Yep64u:
        SCALAR_LOAD = lambda x, y: scalar_mov_instr_select(arg_x.c_type.base, arg_z.c_type.base)(x.as_dword, y)
    else:
        SCALAR_LOAD = scalar_mov_instr_select(arg_x.c_type.base, arg_z.c_type.base)

    if INPUT_TYPE_SIZE == 1:
        SX_SIZE = byte
    elif INPUT_TYPE_SIZE == 2:
        SX_SIZE = word
    elif INPUT_TYPE_SIZE == 4:
        SX_SIZE = dword
    elif INPUT_TYPE_SIZE == 8:
        SX_SIZE = qword

    SCALAR_STORE = scalar_move_map[arg_z.c_type.base]
    if arg_z.c_type.base in [Yep8s, Yep8u, Yep16s, Yep16u, Yep32s, Yep32u,
            Yep64s, Yep64u]:
        SCALAR_ADD = lambda x, y, z: scalar_add_map[arg_z.c_type.base](x, z) \
            if x == y else scalar_add_map[arg_z.c_type.base](x, y)
    else:
        SCALAR_ADD = lambda x, y, z: scalar_add_map[arg_z.c_type.base](x, y, z)

    SIMD_LOAD = packed_mov_instr_select(arg_x.c_type.base, arg_z.c_type.base)
    SIMD_STORE = packed_aligned_move_map[arg_z.c_type.base]
    SIMD_ADD = packed_add_map[arg_z.c_type.base]

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

    reg_x_scalar = scalar_register_map[arg_z.c_type.base]()
    reg_y_scalar = scalar_register_map[arg_z.c_type.base]()

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
    unroll_factor = 5
    ymm_accs = [YMMRegister() for _ in range(unroll_factor)]
    ymm_ops = [YMMRegister() for _ in range(unroll_factor)]

    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2, 3)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            SIMD_LOAD(ymm_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[1]:
            SIMD_LOAD(ymm_ops[i], [reg_y_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[2]:
            SIMD_ADD(ymm_accs[i], ymm_accs[i], ymm_ops[i])
        with instruction_columns[3]:
            SIMD_STORE([reg_z_addr + i * SIMD_REGISTER_SIZE], ymm_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, SIMD_REGISTER_SIZE * unroll_factor * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[1]:
        ADD(reg_y_addr, SIMD_REGISTER_SIZE * unroll_factor * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[3]:
        ADD(reg_z_addr, SIMD_REGISTER_SIZE * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

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

