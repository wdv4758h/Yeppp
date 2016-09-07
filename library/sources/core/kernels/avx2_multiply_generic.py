from peachpy.x86_64 import *
from peachpy import *
from common.instruction_selection import *
from common.YepStatus import *
from common.pipeline import software_pipelined_loop

def multiply_VV_V(arg_x, arg_y, arg_z, arg_n, isa_ext):
    """
    Multiply two vectors and store the result in a third vector

    :param arg_x The first input vector
    :param arg_y The second input vector
    :param arg_z The output vector
    :param arg_n The length of the vectors
    :param isa_ext The ISA extension to use
    """

    # Set some constants that will allow us to write more generic code
    INPUT_TYPE       = arg_x.c_type.base
    OUTPUT_TYPE      = arg_z.c_type.base
    INPUT_TYPE_SIZE  = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_z.c_type.base.size

    SX_SIZE = { 1: byte,
                2: word,
                4: dword,
                8: qword }[INPUT_TYPE_SIZE]

    UNROLL_FACTOR = 5

    SIMD_REGISTER_SIZE = { "AVX2": YMMRegister.size,
                           "AVX" : YMMRegister.size,
                           "SSE" : XMMRegister.size }[isa_ext]

    SCALAR_LOAD, SCALAR_MUL, SCALAR_STORE = scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE, "multiply", isa_ext)
    SIMD_LOAD, SIMD_MUL, SIMD_STORE       = vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE, "multiply", isa_ext)
    reg_x_scalar, reg_y_scalar            = scalar_reg_select(OUTPUT_TYPE, isa_ext)
    simd_accs, simd_ops                   = vector_reg_select(isa_ext, UNROLL_FACTOR)

    ret_ok = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()

    reg_length = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_ok) # There are no elements to process

    # Load arguments and test for null pointers / misalignment
    reg_x_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_x_addr, arg_x)
    TEST(reg_x_addr, reg_x_addr)
    JZ(ret_null_pointer)

    reg_y_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_y_addr, arg_y)
    TEST(reg_y_addr, reg_y_addr)
    JZ(ret_null_pointer)

    reg_z_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_z_addr, arg_z)
    TEST(reg_z_addr, reg_z_addr)
    JZ(ret_null_pointer)
    TEST(reg_z_addr, OUTPUT_TYPE_SIZE - 1) # TODO: fix this in case we want Z aligned on XMMsize - 1
    JNZ(ret_misaligned_pointer)

    align_loop  = Loop()
    vector_loop = Loop()
    scalar_loop = Loop()

    TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1)
    JZ(align_loop.end)
    with align_loop:
        SCALAR_LOAD(reg_x_scalar, [reg_x_addr])
        SCALAR_LOAD(reg_y_scalar, [reg_y_addr])
        SCALAR_MUL(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        ADD(reg_y_addr, INPUT_TYPE_SIZE)
        ADD(reg_z_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, SIMD_REGISTER_SIZE - 1)
        JNZ(align_loop.begin)

    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2, 3)
    for i in range(UNROLL_FACTOR):
        with instruction_columns[0]:
            SIMD_LOAD(simd_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE])
        with instruction_columns[1]:
            SIMD_LOAD(simd_ops[i], [reg_y_addr + i * SIMD_REGISTER_SIZE])
        with instruction_columns[2]:
            SIMD_MUL(simd_accs[i], simd_accs[i], simd_ops[i])
        with instruction_columns[3]:
            SIMD_STORE([reg_z_addr + i * SIMD_REGISTER_SIZE], simd_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, UNROLL_FACTOR * SIMD_REGISTER_SIZE)
    with instruction_columns[1]:
        ADD(reg_y_addr, UNROLL_FACTOR * SIMD_REGISTER_SIZE)
    with instruction_columns[3]:
        ADD(reg_z_addr, UNROLL_FACTOR * SIMD_REGISTER_SIZE)

    software_pipelined_loop(reg_length, UNROLL_FACTOR * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    with scalar_loop:
        SCALAR_LOAD(reg_x_scalar, [reg_x_addr])
        SCALAR_LOAD(reg_y_scalar, [reg_y_addr])
        SCALAR_MUL(reg_x_scalar, reg_x_scalar, reg_y_scalar)
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
