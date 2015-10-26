from peachpy.x86_64 import *
from peachpy import *
from mult_instruction_maps import *
from common.YepStatus import YepStatus
from common.pipeline import software_pipelined_loop

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
    TEST(reg_z_addr, arg_z.ctype.base.size - 1)
    JNZ(ret_misaligned_pointer)

    align_loop = Loop()
    vector_loop = Loop()
    scalar_loop = Loop()

    # unroll_factor = 6
    # xmm_accs = [XMMRegister() for _ in range(unroll_factor)]
    # xmm_ops = [XMMRegister() for _ in range(unroll_factor)]

    vector_x_reg = XMMRegister()
    vector_y_reg = XMMRegister()
    vector_low_res = XMMRegister()
    vector_high_res = XMMRegister()

    scalar_x_reg = scalar_register_map[arg_z.ctype.base]
    scalar_y_reg = scalar_register_map[arg_z.ctype.base]

    # TEST(reg_z_addr, XMMRegister.size - 1)
    # JZ(align_loop.end)
    # with align_loop:
    #     scalar_move_map[arg_x.ctype.base](scalar_x_reg, [reg_x_addr])
    #     scalar_move_map[arg_y.ctype.base](scalar_y_reg, [reg_y_addr])
    #     IMUL(scalar_x_reg, scalar_y_reg)
    #     scalar_move_map[arg_z.ctype.base]([reg_z_addr], scalar_x_reg)
    #     ADD(reg_x_addr, arg_x.ctype.base.size)
    #     ADD(reg_y_addr, arg_y.ctype.base.size)
    #     ADD(reg_z_addr, arg_z.ctype.base.size)
    #     SUB(reg_length, 1)
    #     JZ(ret_ok)
    #     TEST(reg_z_addr, XMMRegister.size - 1)
    #     JNZ(align_loop.begin)

    # instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream(), InstructionStream()]
    # instruction_offsets = (0, 1, 1, 1)
    # for i in range(unroll_factor):
    #     with instruction_columns[0]:
    #         packed_aligned_move_map[arg_x.ctype.base](xmm_accs[i], [reg_x_addr + i * XMMRegister.size * arg_x.ctype.base.size / arg_z.ctype.base.size])
    #     with instruction_columns[1]:
    #         packed_aligned_move_map[arg_y.ctype.base](xmm_accs[i], [reg_y_addr + i * XMMRegister.size * arg_y.ctype.base.size / arg_z.ctype.base.size])
    #     with instruction_columns[2]:
    #         packed_high_mult_map[arg_x.ctype.base](ymm



    CMP(reg_length, XMMRegister.size / arg_x.ctype.base.size) # Not enough elements to use SIMD instructions
    JB(vector_loop.end)
    with vector_loop:
        VMOVDQA(vector_x_reg, [reg_x_addr])
        VMOVDQA(vector_y_reg, [reg_y_addr])
        if arg_x.ctype.base in [Yep32s, Yep64s]:
            VPMULDQ(vector_x_reg, vector_x_reg, vectory_y_reg)
            VMOVDQA([reg_z_addr], vector_x_reg)
        else:
            packed_low_mult_map[arg_x.ctype.base](vector_low_res, vector_x_reg, vector_y_reg)
            packed_high_mult_map[arg_x.ctype.base](vector_high_res, vector_x_reg, vector_y_reg)
            high_unpack_map[(arg_x.ctype.base, arg_z.ctype.base)](vector_y_reg, vector_low_res, vector_high_res)
            low_unpack_map[(arg_x.ctype.base, arg_z.ctype.base)](vector_x_reg, vector_low_res, vector_high_res)
            VMOVDQA([reg_z_addr], vector_x_reg)
            VMOVDQA([reg_z_addr + XMMRegister.size], vector_y_reg)
        ADD(reg_x_addr, XMMRegister.size)
        ADD(reg_y_addr, XMMRegister.size)
        ADD(reg_z_addr, 2 * XMMRegister.size)
        SUB(reg_length, XMMRegister.size / arg_x.ctype.base.size)
        CMP(reg_length, XMMRegister.size / arg_x.ctype.base.size)
        JAE(vector_loop.begin)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    with scalar_loop:
        MOVSX(scalar_x_reg, [reg_x_addr])
        MOVSX(scalar_y_reg, [reg_y_addr])
        IMUL(scalar_x_reg, scalar_y_reg)
        MOV([reg_z_addr], scalar_x_reg)
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
