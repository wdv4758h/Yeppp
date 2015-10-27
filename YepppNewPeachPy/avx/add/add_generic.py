from peachpy.x86_64 import *
from peachpy import *
from avx_add_instruction_maps import * # The correct instructions to use depending on argument type
from common.YepStatus import YepStatus
from common.pipeline import software_pipelined_loop
# Write AVX 512 and SSE2 versions of the addition kernels.
# Complex conjugate multiplication and pairwise complex of vectors
# Tutorial for peachpy assembly
def scalar_add_instr_select(reg_x, reg_y, op_type):
    """
    Selects the correct add instruction depending on the operand size.
    This function is necessary since some add instructions in x86_64 take
    two arguments while some take 3.
    """
    if op_type in [Yep8s, Yep8u, Yep16s, Yep16u, Yep32s, Yep32u, Yep64s, Yep64u]: # Their add function takes two args
        return scalar_add_map[op_type](reg_x, reg_y)
    else: # Takes 3 args
        return scalar_add_map[op_type](reg_x, reg_x, reg_y)

def scalar_mov_instr_select(reg, addr, input_type, output_type):
    """
    Selects the correct move instruction depending on operand type.
    Chooses SX / ZX instructions if necessary.
    """
    if input_type.size == output_type.size:
        return scalar_move_map[input_type](reg, addr)
    else: # Must sign-extend on the move
        return scalar_movsx_map[(input_type, output_type)](reg, addr)

def packed_mov_instr_select(reg, addr, input_type, output_type):
    """
    Selects the correct move instruction for packed operands depending on type.
    Chooses SX / ZX instructions if necessary
    """
    if input_type.size == output_type.size:
        return packed_unaligned_move_map[input_type](reg, addr)
    else:
        return packed_movsx_map[(input_type, output_type)](reg, addr)

def add_generic(arg_x, arg_y, arg_z, arg_n):
    """
    Add function which uses avx_add_instruction_maps to execute the addition
    kernel on any type operands.
    """

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
    TEST(reg_z_addr, arg_z.ctype.base.size - 1) # Make sure arg_z is aligned on the proper boundary
    JNZ(ret_misaligned_pointer)

    unroll_factor = 6
    ymm_accs = [YMMRegister() for _ in range(unroll_factor)]
    ymm_ops = [YMMRegister() for _ in range(unroll_factor)]

    reg_x_scalar = scalar_register_map[arg_z.ctype.base]()
    reg_y_scalar = scalar_register_map[arg_z.ctype.base]()

    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on Z addr
    # Process elements 1 at a time until x is aligned on YMMRegister.size boundary
    TEST(reg_z_addr, YMMRegister.size - 1)
    JZ(align_loop.end)
    with align_loop:
        scalar_mov_instr_select(reg_x_scalar, [reg_x_addr], arg_x.ctype.base, arg_z.ctype.base)
        scalar_mov_instr_select(reg_y_scalar, [reg_y_addr], arg_x.ctype.base, arg_z.ctype.base)
        scalar_add_instr_select(reg_x_scalar, reg_y_scalar, arg_z.ctype.base)
        scalar_move_map[arg_z.ctype.base]([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, arg_x.ctype.base.size)
        ADD(reg_y_addr, arg_x.ctype.base.size)
        ADD(reg_z_addr, arg_z.ctype.base.size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, YMMRegister.size - 1)
        JNZ(align_loop.begin)

    # Batch loop prologue
    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 1, 1)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            packed_mov_instr_select(ymm_accs[i], [reg_x_addr + i * YMMRegister.size * arg_x.ctype.base.size / arg_z.ctype.base.size], arg_x.ctype.base, arg_z.ctype.base)
        with instruction_columns[1]:
            packed_mov_instr_select(ymm_ops[i], [reg_y_addr + i * YMMRegister.size * arg_x.ctype.base.size / arg_z.ctype.base.size], arg_x.ctype.base, arg_z.ctype.base)
        with instruction_columns[2]:
            packed_add_map[arg_z.ctype.base](ymm_accs[i], ymm_accs[i], ymm_ops[i])
        with instruction_columns[3]:
            packed_aligned_move_map[arg_z.ctype.base]([reg_z_addr + i * YMMRegister.size], ymm_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, YMMRegister.size * unroll_factor * arg_x.ctype.base.size / arg_z.ctype.base.size)
    with instruction_columns[1]:
        ADD(reg_y_addr, YMMRegister.size * unroll_factor * arg_x.ctype.base.size / arg_z.ctype.base.size)
    with instruction_columns[3]:
        ADD(reg_z_addr, YMMRegister.size * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * YMMRegister.size / arg_z.ctype.base.size, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop: # Process the remaining elements
        scalar_mov_instr_select(reg_x_scalar, [reg_x_addr], arg_x.ctype.base, arg_z.ctype.base)
        scalar_mov_instr_select(reg_y_scalar, [reg_y_addr], arg_x.ctype.base, arg_z.ctype.base)
        scalar_add_instr_select(reg_x_scalar, reg_y_scalar, arg_z.ctype.base)
        scalar_move_map[arg_z.ctype.base]([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, arg_x.ctype.base.size)
        ADD(reg_y_addr, arg_x.ctype.base.size)
        ADD(reg_z_addr, arg_z.ctype.base.size)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatus.YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatus.YepStatusMisalignedPointer)
