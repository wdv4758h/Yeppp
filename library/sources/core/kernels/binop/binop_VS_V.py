from peachpy.x86_64 import *
from peachpy import *
from common.YepStatus import *
from common.pipeline import software_pipelined_loop
from binop_common import *

def binop_VS_V(arg_x, arg_y, arg_z, arg_n, op, isa_ext):
    """
    This kernel can be used for addition, subtraction, max, min
    for an operand that operates on a vector and a scalar and stores
    the result in a third vector.
    :param arg_x The input vector
    :param arg_y The input scalar
    :param arg_z The output vector: z[i] := x[i] op y
    :param arg_n The number of elements
    :param op Used to select the correct operation instruction
    :param isa_ext Used to select the correct instructions for the
        given extension
    """
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_TYPE = arg_z.c_type.base
    INPUT_TYPE_SIZE = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_z.c_type.base.size


    SX_SIZE = { 1: byte,
                2: word,
                4: dword,
                8: qword }[INPUT_TYPE_SIZE]

    UNROLL_FACTOR = 5

    SIMD_REGISTER_SIZE = { "AVX2": YMMRegister.size,
                           "AVX" : YMMRegister.size,
                           "SSE" : XMMRegister.size }[isa_ext]

    SCALAR_LOAD, SCALAR_OP, SCALAR_STORE = scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE, op, isa_ext)
    SIMD_LOAD, SIMD_OP, SIMD_STORE = vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE, op, isa_ext)
    reg_x_scalar, reg_y_scalar = scalar_reg_select(OUTPUT_TYPE, isa_ext)
    simd_accs, reg_y_vector = vector_reg_select(isa_ext, UNROLL_FACTOR, scalar=True)

    if isa_ext == "SSE":
        if INPUT_TYPE in [ Yep32f, Yep64f ]:
            # in this case, the arg is passed in xmm and we don't need to move it
            reg_y_vector = reg_y_scalar


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

    if INPUT_TYPE_SIZE < 4:
        LOAD.ARGUMENT(reg_y_scalar.as_dword, arg_y)
    else:
        LOAD.ARGUMENT(reg_y_scalar, arg_y)

    reg_z_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_z_addr, arg_z)
    TEST(reg_z_addr, reg_z_addr)
    JZ(ret_null_pointer)
    TEST(reg_z_addr, OUTPUT_TYPE_SIZE - 1) # Make sure arg_z is aligned on the proper boundary
    JNZ(ret_misaligned_pointer)


    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on output addr
    # Process elements 1 at a time until output is aligned on YMMRegister.size boundary
    TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1) # Check if already aligned
    JZ(align_loop.end) # If so, skip this loop entirely
    with align_loop:
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_OP(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1)
        JNZ(align_loop.begin)


    # Batch loop for processing the rest of the array in a pipelined loop
    MOV_GPR_TO_VECTOR(reg_y_vector, reg_y_scalar, INPUT_TYPE, OUTPUT_TYPE, isa_ext)

    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2)
    for i in range(UNROLL_FACTOR):
        with instruction_columns[0]:
            SIMD_LOAD(simd_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[1]:
            SIMD_OP(simd_accs[i], simd_accs[i], reg_y_vector)
        with instruction_columns[2]:
            SIMD_STORE([reg_z_addr + i * SIMD_REGISTER_SIZE], simd_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[2]:
        ADD(reg_z_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR)

    software_pipelined_loop(reg_length, UNROLL_FACTOR * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

    # Check if there are leftover elements that were not processed in the pipelined loop
    # This loop should iterate at most #(elems processed per iteration in the batch loop) - 1 times
    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop: # Process the remaining elements
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_OP(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatusMisalignedPointer)
