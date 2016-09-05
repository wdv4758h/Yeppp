from peachpy.x86_64 import *
from peachpy import *
from common.YepStatus import *
from common.pipeline import software_pipelined_loop
from binop_common import *

def binop_IVS_IV(arg_x, arg_y, arg_n, op, isa_ext):
    """
    This kernel can be used for addition, subtraction, max, min
    for an operand that operates on a vector and a scalar and stores
    the result in the vector.
    :param arg_x The input and output vector
    :param arg_y The input scalar
    :param arg_n The length of the vector
    :param op Select the correct operation
    :param isa_ext Select the correct instructions for the given
        extension
    """
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_TYPE = arg_x.c_type.base
    INPUT_TYPE_SIZE = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_x.c_type.base.size

    UNROLL_FACTOR = 5

    SIMD_REGISTER_SIZE = { "AVX2": YMMRegister.size,
                           "AVX" : YMMRegister.size,
                           "SSE" : XMMRegister.size }[isa_ext]

    SCALAR_LOAD, SCALAR_OP, SCALAR_STORE = scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE, op, isa_ext)
    SIMD_LOAD, SIMD_OP, SIMD_STORE = vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE, op, isa_ext)
    reg_x_scalar, reg_y_scalar = scalar_reg_select(OUTPUT_TYPE, isa_ext)
    simd_accs, reg_y_vector = vector_reg_select(isa_ext, UNROLL_FACTOR, scalar=True)

    if isa_ext == "SSE" and INPUT_TYPE in [ Yep32f, Yep64f ]:
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

    align_loop = Loop()
    scalar_loop = Loop()

    # Aligning on output address
    TEST(reg_x_addr, SIMD_REGISTER_SIZE - 1) # Check if already aligned
    JZ(align_loop.end) # If so, skip this loop entirely
    with align_loop:
        SCALAR_LOAD(reg_x_scalar, [reg_x_addr])
        SCALAR_OP(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_x_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_x_addr, SIMD_REGISTER_SIZE - 1)
        JNZ(align_loop.begin)

    # Batch loop for processing the rest of the array in a pipelined loop
    MOV_GPR_TO_VECTOR(reg_y_vector, reg_y_scalar, INPUT_TYPE, OUTPUT_TYPE, isa_ext)

    # Make a copy of reg_x that points to the output
    # so we can pipeline
    reg_x_addr_out = GeneralPurposeRegister64()
    MOV(reg_x_addr_out, reg_x_addr)

    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2)

    for i in range(UNROLL_FACTOR):
        with instruction_columns[0]:
            SIMD_LOAD(simd_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[1]:
            SIMD_OP(simd_accs[i], simd_accs[i], reg_y_vector)
        with instruction_columns[2]:
            SIMD_STORE([reg_x_addr_out + i * SIMD_REGISTER_SIZE], simd_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[2]:
        ADD(reg_x_addr_out, SIMD_REGISTER_SIZE * UNROLL_FACTOR)

    software_pipelined_loop(reg_length, UNROLL_FACTOR * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop:
        SCALAR_LOAD(reg_x_scalar, [reg_x_addr])
        SCALAR_OP(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_x_addr], reg_x_scalar)
        ADD(reg_x_addr, INPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatusMisalignedPointer)
