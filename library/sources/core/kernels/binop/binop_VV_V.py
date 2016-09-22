from peachpy.x86_64 import *
from peachpy import *
import common.YepStatus as YepStatus
from common.pipeline import software_pipelined_loop
from common.instruction_selection import *

def binop_VV_V(arg_x, arg_y, arg_z, arg_n, op, isa_ext):
    """
    This kernel is a software pipelined loop that can be
    used for most binary operators: in particular,
    addition, subtraction, max, min.  Multiply and division
    are separate, as they require a different load/store pattern.
    This general is generic in the sense that all data types can
    use this kernel.  The instruction selection functions along
    with the instruction maps will select the right instructions
    for load / store, the operation itself, and for the correct
    instruction extension.

    :param arg_x The first input argument
    :param arg_y The second input argument
    :param arg_z The output vector
    :param arg_n The length parameter
    :param op The binary operation to perform
    :param isa_ext The ISA extension to use
    """

    # First we set some constants based on the input/output types
    # so that we can use the same code for any input/output
    # type combination
    input_type = arg_x.c_type.base
    output_type = arg_z.c_type.base
    input_type_size = arg_x.c_type.base.size
    output_type_size = arg_z.c_type.base.size

    SX_SIZE = { 1: byte,
                2: word,
                4: dword,
                8: qword }[input_type_size]

    unroll_factor = 5

    simd_register_size = { "AVX2": YMMRegister.size,
                           "AVX" : YMMRegister.size,
                           "SSE" : XMMRegister.size }[isa_ext]

    SCALAR_LOAD, SCALAR_OP, SCALAR_STORE = scalar_instruction_select(input_type, output_type, op, isa_ext)
    SIMD_LOAD, SIMD_OP, SIMD_STORE = vector_instruction_select(input_type, output_type, op, isa_ext)
    reg_x_scalar, reg_y_scalar = scalar_reg_select(output_type, isa_ext)
    simd_accs, simd_ops = vector_reg_select(isa_ext, unroll_factor)

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
    TEST(reg_z_addr, output_type_size - 1) # Make sure arg_z is aligned on the proper boundary
    JNZ(ret_misaligned_pointer)


    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on Z addr
    # Process elements 1 at a time until z is aligned on simd_register_size boundary
    TEST(reg_z_addr, simd_register_size - 1) # Check if already aligned
    JZ(align_loop.end) # If so, skip this loop entirely
    with align_loop:
        # Process elements one at a time until our output stores will be aligned
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_LOAD(reg_y_scalar, SX_SIZE[reg_y_addr])
        if (op == "max" or op == "min") and not input_type.is_floating_point:
            # There is no scalar instruction for integer min-max
            CMP(reg_y_scalar, reg_x_scalar)
            if input_type.is_signed_integer:
                if op == "max":
                    CMOVGE(reg_x_scalar, reg_y_scalar)
                else:
                    CMOVLE(reg_x_scalar, reg_y_scalar)
            else:
                if op == "max":
                    CMOVAE(reg_x_scalar, reg_y_scalar)
                else:
                    CMOVBE(reg_x_scalar, reg_y_scalar)
            MOV([reg_z_addr], reg_x_scalar)
        else:
            SCALAR_OP(reg_x_scalar, reg_x_scalar, reg_y_scalar)
            SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, input_type_size)
        ADD(reg_y_addr, input_type_size)
        ADD(reg_z_addr, output_type_size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, simd_register_size - 1)
        JNZ(align_loop.begin)

    # Batch loop for processing the rest of the array in a pipelined loop
    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2, 3)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            SIMD_LOAD(simd_accs[i], [reg_x_addr + i * simd_register_size * input_type_size / output_type_size])
        with instruction_columns[1]:
            SIMD_LOAD(simd_ops[i], [reg_y_addr + i * simd_register_size * input_type_size / output_type_size])
        with instruction_columns[2]:
            SIMD_OP(simd_accs[i], simd_accs[i], simd_ops[i])
        with instruction_columns[3]:
            SIMD_STORE([reg_z_addr + i * simd_register_size], simd_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, simd_register_size * unroll_factor * input_type_size / output_type_size)
    with instruction_columns[1]:
        ADD(reg_y_addr, simd_register_size * unroll_factor * input_type_size / output_type_size)
    with instruction_columns[3]:
        ADD(reg_z_addr, simd_register_size * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * simd_register_size / output_type_size, instruction_columns, instruction_offsets)

    # Check if there are leftover elements that were not processed in the pipelined loop
    # This loop should iterate at most #(elems processed per iteration in the batch loop) - 1 times
    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop: # Process the remaining elements
        SCALAR_LOAD(reg_x_scalar, SX_SIZE[reg_x_addr])
        SCALAR_LOAD(reg_y_scalar, SX_SIZE[reg_y_addr])
        if (op == "max" or op == "min") and not input_type.is_floating_point:
            # There is no scalar instruction for integer min-max
            CMP(reg_y_scalar, reg_x_scalar)
            if input_type.is_signed_integer:
                if op == "max":
                    CMOVGE(reg_x_scalar, reg_y_scalar)
                else:
                    CMOVLE(reg_x_scalar, reg_y_scalar)
            else:
                if op == "max":
                    CMOVAE(reg_x_scalar, reg_y_scalar)
                else:
                    CMOVBE(reg_x_scalar, reg_y_scalar)
            MOV([reg_z_addr], reg_x_scalar)
        else:
            SCALAR_OP(reg_x_scalar, reg_x_scalar, reg_y_scalar)
            SCALAR_STORE([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, input_type_size)
        ADD(reg_y_addr, input_type_size)
        ADD(reg_z_addr, output_type_size)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatus.YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatus.YepStatusMisalignedPointer)
