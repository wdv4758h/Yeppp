from peachpy.x86_64 import *
from peachpy import *
import common.YepStatus as YepStatus
from common.pipeline import software_pipelined_loop
from common.instruction_selection import *

def dot_product_V32fV32f_S32f_Haswell(arg_x, arg_y, arg_z, arg_n):
    op_size = 4 # 4 byte operands
    unroll_factor = 5

    ret_ok = Label()
    ret_empty_arrays = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()

    # Make sure we load the output pointer before checking the length > 0
    # So that if the length is 0, we can store 0 in the output pointer
    reg_z_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_z_addr, arg_z)
    TEST(reg_z_addr, reg_z_addr)
    JZ(ret_null_pointer)
    TEST(reg_z_addr, op_size - 1)
    JNZ(ret_misaligned_pointer)

    reg_length = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_empty_arrays)

    reg_x_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_x_addr, arg_x)
    TEST(reg_x_addr, reg_x_addr)
    JZ(ret_null_pointer)
    TEST(reg_x_addr, op_size - 1)
    JNZ(ret_misaligned_pointer)

    reg_y_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_y_addr, arg_y)
    TEST(reg_y_addr, reg_y_addr)
    JZ(ret_null_pointer)
    TEST(reg_y_addr, op_size - 1)
    JNZ(ret_misaligned_pointer)

    align_loop = Loop()
    scalar_loop = Loop()


    acc_regs = [YMMRegister() for _ in range(unroll_factor)]
    op_regs_out = [YMMRegister() for _ in range(unroll_factor)]
    op_regs = [YMMRegister() for _ in range(unroll_factor)]
    scalar_acc = YMMRegister()

    # Zero out all of the accumulation registers
    for acc_reg in acc_regs:
        VXORPS(acc_reg, acc_reg, acc_reg)
    VXORPS(scalar_acc, scalar_acc, scalar_acc)

    # Align the X input on YMMRegister size boundary
    op_reg_out = op_regs_out[0].as_xmm
    op_reg = op_regs[0].as_xmm
    TEST(reg_x_addr, YMMRegister.size - 1)
    JZ(align_loop.end)
    with align_loop:
        VMOVSS(op_reg_out, [reg_x_addr])
        VMOVSS(op_reg, [reg_y_addr])
        VMULSS(op_reg_out, op_reg_out, op_reg)
        VADDSS(scalar_acc.as_xmm, scalar_acc.as_xmm, op_reg_out)
        ADD(reg_x_addr, op_size)
        ADD(reg_y_addr, op_size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_x_addr, YMMRegister.size - 1)
        JNZ(align_loop.begin)

    instruction_columns = [InstructionStream() for _ in range(4)]
    instruction_offsets = (0, 1, 2, 3)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            VMOVAPS(op_regs_out[i], [reg_x_addr + i * YMMRegister.size])
        with instruction_columns[1]:
            VMOVUPS(op_regs[i], [reg_y_addr + i * YMMRegister.size])
        with instruction_columns[2]:
            VMULPS(op_regs_out[i], op_regs_out[i], op_regs[i])
        with instruction_columns[3]:
            VADDPS(acc_regs[i], acc_regs[i], op_regs_out[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, YMMRegister.size * unroll_factor)
    with instruction_columns[1]:
        ADD(reg_y_addr, YMMRegister.size * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * YMMRegister.size / op_size, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    with scalar_loop:
        VMOVSS(op_reg_out, [reg_x_addr])
        VMOVSS(op_reg, [reg_y_addr])
        VMULSS(op_reg_out, op_reg_out, op_reg)
        VADDSS(scalar_acc.as_xmm, scalar_acc.as_xmm, op_reg_out)
        ADD(reg_x_addr, op_size)
        ADD(reg_y_addr, op_size)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        tmp = YMMRegister()
        # Reduce the accumulators
        for i in range(1, len(acc_regs)):
            VADDPS(acc_regs[0], acc_regs[0], acc_regs[i])
        VADDPS(acc_regs[0], acc_regs[0], scalar_acc)

        VHADDPS(acc_regs[0], acc_regs[0], acc_regs[0])
        VHADDPS(acc_regs[0], acc_regs[0], acc_regs[0])
        # acc_regs[0] has the sum of the top 4 elements duplicated 4 times in the upper bits
        # and the sum of the lower 4 elements duplicated 4 times in the lower bits
        # Move the upper sum into the lower bits of tmp and then add them to get the sum of all 8 elements in the accumlator
        VPERM2F128(tmp, acc_regs[0], acc_regs[0], 0x1)
        VADDSS(acc_regs[0].as_xmm, acc_regs[0].as_xmm, tmp.as_xmm)

        VMOVSS([reg_z_addr], acc_regs[0].as_xmm)
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_empty_arrays):
        MOV(dword[reg_z_addr], 0)
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatus.YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatus.YepStatusMisalignedPointer)
