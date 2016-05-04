from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.sse_add_instruction_maps import *
from common.pipeline import software_pipelined_loop
from common.YepStatus import *

def scalar_mov_instr_select(reg, addr, input_type, output_type):
    """
    Selects the correct move instruction depending on operand type.
    Chooses SX / ZX instructions if necessary
    """
    if input_type.size == output_type.size:
        return scalar_move_map[input_type](reg, addr)
    else: # Must sign-extend on the move, TODO map this
        return MOVSX(reg, addr)

def packed_mov_instr_select(reg, addr, input_type, output_type):
    """
    Selects the correct move instruction for packed unaligned operands.
    Chooses SX / ZX instructions if necessary
    """
    if input_type.size == output_type.size:
        return packed_unaligned_move_map[input_type](reg, addr)
    else:
        return packed_movsx_map[(input_type, output_type)](reg, addr)

def add_generic(arg_x, arg_y, arg_z, arg_n):
    """
    Uses sse_add_instruction_maps to execute the addition
    kernel on any type operand
    """
    # Compile time constants
    INPUT_SIZE = arg_x.c_type.base.size
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_SIZE = arg_z.c_type.base.size
    OUTPUT_TYPE = arg_z.c_type.base

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
    TEST(reg_z_addr, arg_z.c_type.base.size - 1) # Make sure arg_z is aligned
    JNZ(ret_misaligned_pointer)

    reg_x_scalar = scalar_register_map[arg_z.c_type.base]()
    reg_y_scalar = scalar_register_map[arg_z.c_type.base]()

    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on Z addr
    # Process elements 1 at a time until x is aligned
    TEST(reg_z_addr, XMMRegister.size - 1)
    JZ(align_loop.end)
    with align_loop:
        scalar_mov_instr_select(reg_x_scalar, [reg_x_addr], arg_x.c_type.base, arg_z.c_type.base)
        scalar_mov_instr_select(reg_y_scalar, [reg_y_addr], arg_x.c_type.base, arg_z.c_type.base)
        scalar_add_map[arg_z.c_type.base](reg_x_scalar, reg_y_scalar)
        scalar_move_map[arg_z.c_type.base]([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, arg_x.c_type.base.size)
        ADD(reg_y_addr, arg_x.c_type.base.size)
        ADD(reg_z_addr, arg_z.c_type.base.size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, XMMRegister.size - 1)
        JNZ(align_loop.begin)

    # instruction_columns = [ InstructionStream() for _ in range(6) ]
    # instruction_offsets = tuple(range(6))
    # xmm_xs = [ XMMRegister() for _ in range(6) ]
    # xmm_ys = [ XMMRegister() for _ in range(6) ]
    # for i in range(6):
    #     with instruction_columns[i]:
    #         packed_mov_instr_select(xmm_xs[i], [reg_x_addr + XMMRegister.size * INPUT_SIZE], INPUT_TYPE, OUTPUT_TYPE)
    #         ADD(reg_x_addr, XMMRegister.size * INPUT_SIZE / OUTPUT_SIZE)
    #         packed_mov_instr_select(xmm_ys[i], [reg_y_addr + XMMRegister.size * INPUT_SIZE], INPUT_TYPE, OUTPUT_TYPE)
    #         ADD(reg_y_addr, XMMRegister.size * INPUT_SIZE / OUTPUT_SIZE)
    #         packed_add_map[OUTPUT_TYPE](xmm_xs[i], xmm_ys[i])
    #         packed_aligned_move_map[OUTPUT_TYPE]([reg_z_addr + XMMRegister.size], xmm_xs[i])
    #         ADD(reg_z_addr, XMMRegister.size)

    unroll_factor = 2
    xmm_accs = [XMMRegister() for _ in range(unroll_factor)]
    xmm_ops = [XMMRegister() for _ in range(unroll_factor)]

    # Batch loop prologue
    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 0, 1, 1)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            packed_mov_instr_select(xmm_accs[i], [reg_x_addr + i * XMMRegister.size * arg_x.c_type.base.size / arg_z.c_type.base.size], arg_x.c_type.base, arg_z.c_type.base)
        with instruction_columns[1]:
            packed_mov_instr_select(xmm_ops[i], [reg_y_addr + i * XMMRegister.size * arg_x.c_type.base.size / arg_z.c_type.base.size], arg_x.c_type.base, arg_z.c_type.base)
        with instruction_columns[2]:
            packed_add_map[arg_z.c_type.base](xmm_accs[i], xmm_ops[i])
        with instruction_columns[3]:
            packed_aligned_move_map[arg_z.c_type.base]([reg_z_addr + i * XMMRegister.size], xmm_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, XMMRegister.size * unroll_factor * arg_x.c_type.base.size / arg_z.c_type.base.size)
    with instruction_columns[1]:
        ADD(reg_y_addr, XMMRegister.size * unroll_factor * arg_x.c_type.base.size / arg_z.c_type.base.size)
    with instruction_columns[3]:
        ADD(reg_z_addr, XMMRegister.size * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * XMMRegister.size / OUTPUT_SIZE, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop: # Process the remaining elements
        scalar_mov_instr_select(reg_x_scalar, [reg_x_addr], arg_x.c_type.base, arg_z.c_type.base)
        scalar_mov_instr_select(reg_y_scalar, [reg_y_addr], arg_x.c_type.base, arg_z.c_type.base)
        scalar_add_map[arg_z.c_type.base](reg_x_scalar, reg_y_scalar)
        scalar_move_map[arg_z.c_type.base]([reg_z_addr], reg_x_scalar)
        ADD(reg_x_addr, arg_x.c_type.base.size)
        ADD(reg_y_addr, arg_x.c_type.base.size)
        ADD(reg_z_addr, arg_z.c_type.base.size)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatusMisalignedPointer)

