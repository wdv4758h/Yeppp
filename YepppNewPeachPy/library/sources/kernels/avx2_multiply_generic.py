from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.avx_mult_instruction_maps import *
from common.YepStatus import YepStatus
from common.pipeline import software_pipelined_loop

def scalar_mult_inst_select(reg_x, reg_y, op_type):
    """
    Determines the correct scalar multiplication instruction
    to use by using scalar_mult_map.
    If the needed instruction takes 3 arguments, then
    reg_x is both the destination and the 1st source.
    """
    if op_type in [Yep32f, Yep64f]:
        scalar_mult_map[op_type](reg_x, reg_x, reg_y)
    else:
        scalar_mult_map[op_type](reg_x, reg_y)

def multiply_generic(arg_x, arg_y, arg_z, arg_n):
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
    TEST(reg_z_addr, YMMRegister.size - 1) # TODO: fix this in case we want Z aligned on XMMsize - 1
    JNZ(ret_misaligned_pointer)

    vector_loop = Loop()
    scalar_loop = Loop()

    # Determine which register type to use for vector operations.
    # For certain data types (e.g 16s -> 32s multiplication)
    # where multiplication requires unpacking, XMM implementations are simpler
    # TODO: Implement everything with YMM and test speed vs. XMM implementations
    if arg_x.ctype.base in [Yep16s, Yep16u] and arg_z.ctype.base in [Yep32s, Yep32u]:
        vector_x_reg = XMMRegister()
        vector_y_reg = XMMRegister()
        vector_low_res = XMMRegister()
        vector_high_res = XMMRegister()
        vec_reg_size = XMMRegister.size
    else:
        vector_x_reg = YMMRegister()
        vector_y_reg = YMMRegister()
        vec_reg_size = YMMRegister.size

    scalar_x_reg = scalar_register_map[arg_z.ctype.base]()
    scalar_y_reg = scalar_register_map[arg_z.ctype.base]()

    CMP(reg_length, vec_reg_size / arg_x.ctype.base.size) # Not enough elements to use SIMD instructions
    JB(vector_loop.end)
    with vector_loop:
        if arg_x.ctype.base in [Yep16s, Yep32s, Yep64s] and arg_x.ctype.base == arg_z.ctype.base: # We are only going to keep the lower bits
            packed_aligned_move_map[arg_x.ctype.base](vector_x_reg, [reg_x_addr])
            packed_aligned_move_map[arg_y.ctype.base](vector_y_reg, [reg_y_addr])
            packed_low_mult_map[arg_x.ctype.base](vector_x_reg, vector_x_reg, vector_y_reg)
            packed_aligned_move_map[arg_x.ctype.base]([reg_z_addr], vector_x_reg)
            ADD(reg_z_addr, vec_reg_size)
            ADD(reg_x_addr, vec_reg_size)
            ADD(reg_y_addr, vec_reg_size)
            SUB(reg_length, vec_reg_size / arg_x.ctype.base.size)
            CMP(reg_length, vec_reg_size / arg_x.ctype.base.size)
        elif arg_x.ctype.base in [Yep16s, Yep16u] and arg_z.ctype.base in [Yep32s, Yep32u]: # Multiplication requires unpacking the low and high results
            packed_aligned_move_map[arg_x.ctype.base](vector_x_reg, [reg_x_addr])
            packed_aligned_move_map[arg_y.ctype.base](vector_y_reg, [reg_y_addr])
            packed_low_mult_map[arg_x.ctype.base](vector_low_res, vector_x_reg, vector_y_reg)
            packed_high_mult_map[arg_x.ctype.base](vector_high_res, vector_x_reg, vector_y_reg)
            VPUNPCKHWD(vector_x_reg, vector_low_res, vector_high_res)
            VPUNPCKLWD(vector_y_reg, vector_low_res, vector_high_res)
            packed_aligned_move_map[arg_x.ctype.base]([reg_z_addr], vector_y_reg)
            packed_aligned_move_map[arg_x.ctype.base]([reg_z_addr + vec_reg_size], vector_x_reg)
            ADD(reg_z_addr, 2 * vec_reg_size)
            ADD(reg_x_addr, vec_reg_size)
            ADD(reg_y_addr, vec_reg_size)
            SUB(reg_length, vec_reg_size / arg_x.ctype.base.size)
            CMP(reg_length, vec_reg_size / arg_x.ctype.base.size)
        elif arg_x.ctype.base in [Yep32s, Yep32u] and arg_z.ctype.base in [Yep64s, Yep64u]: # Multiply from 32s -> 64s using the VMULDQ instr
            VPMOVZXDQ(vector_x_reg, [reg_x_addr])
            VPMOVZXDQ(vector_y_reg, [reg_y_addr])
            if arg_x.ctype.base == Yep32s:
                VPMULDQ(vector_x_reg, vector_x_reg, vector_y_reg)
            else:
                VPMULUDQ(vector_x_reg, vector_x_reg, vector_y_reg)
            VMOVDQA([reg_z_addr], vector_x_reg)
            ADD(reg_z_addr, vec_reg_size)
            ADD(reg_x_addr, vec_reg_size / 2)
            ADD(reg_y_addr, vec_reg_size / 2)
            SUB(reg_length, vec_reg_size / (2 * arg_x.ctype.base.size))
            CMP(reg_length, vec_reg_size / (2 * arg_x.ctype.base.size))
        elif arg_x.ctype.base in [Yep32f, Yep64f]: # Multiplication can be performed in 1 instruction on floats
            packed_aligned_move_map[arg_x.ctype.base](vector_x_reg, [reg_x_addr])
            packed_aligned_move_map[arg_y.ctype.base](vector_y_reg, [reg_y_addr])
            packed_mult_map[arg_x.ctype.base](vector_x_reg, vector_x_reg, vector_y_reg)
            packed_aligned_move_map[arg_x.ctype.base]([reg_z_addr], vector_x_reg)
            ADD(reg_z_addr, vec_reg_size)
            ADD(reg_x_addr, vec_reg_size)
            ADD(reg_y_addr, vec_reg_size)
            SUB(reg_length, vec_reg_size / arg_x.ctype.base.size)
            CMP(reg_length, vec_reg_size / arg_x.ctype.base.size)
        JAE(vector_loop.begin)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    with scalar_loop:
        scalar_move_map[arg_x.ctype.base](scalar_x_reg, [reg_x_addr])
        scalar_move_map[arg_x.ctype.base](scalar_y_reg, [reg_y_addr])
        scalar_mult_inst_select(scalar_x_reg, scalar_y_reg, arg_x.ctype.base)
        scalar_move_map[arg_z.ctype.base]([reg_z_addr], scalar_x_reg)
        ADD(reg_x_addr, arg_x.ctype.base.size)
        ADD(reg_y_addr, arg_y.ctype.base.size)
        ADD(reg_z_addr, arg_z.ctype.base.size)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatus.YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatus.YepStatusMisalignedPointer)
