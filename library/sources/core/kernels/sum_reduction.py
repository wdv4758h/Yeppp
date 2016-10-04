from peachpy.x86_64 import *
from peachpy import *
import common.YepStatus as YepStatus
from common.pipeline import software_pipelined_loop
from common.instruction_selection import *

def sum_Haswell(arg_x, arg_z, arg_n):
    op_size = arg_x.c_type.base.size
    op_type = arg_x.c_type.base
    unroll_factor = 5

    SIMD_MOV, SIMD_ADD, SIMD_ALIGNED_MOV = avx2_vector_instruction_select(op_type, op_type, "add")
    SCALAR_MOV, SCALAR_ADD, _ = avx2_scalar_instruction_select(op_type, op_type, "add")


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


    align_loop = Loop()
    scalar_loop = Loop()

    acc_regs = [YMMRegister() for _ in range(unroll_factor)]
    scalar_acc = YMMRegister()

    # Zero out all of the accumulation registers
    for acc_reg in acc_regs:
        VXORPS(acc_reg, acc_reg, acc_reg)
    VXORPS(scalar_acc, scalar_acc, scalar_acc)

    # Align the X input on YMMRegister size boundary
    TEST(reg_x_addr, YMMRegister.size - 1)
    JZ(align_loop.end)
    with align_loop:
        SCALAR_ADD(scalar_acc.as_xmm, scalar_acc.as_xmm, [reg_x_addr])
        ADD(reg_x_addr, op_size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_x_addr, YMMRegister.size - 1)
        JNZ(align_loop.begin)

    instruction_columns = [InstructionStream() for _ in range(1)]
    instruction_offsets = (0,)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            SIMD_ADD(acc_regs[i], acc_regs[i], [reg_x_addr + i * YMMRegister.size])
    with instruction_columns[0]:
        ADD(reg_x_addr, YMMRegister.size * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * YMMRegister.size / op_size, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    with scalar_loop:
        SCALAR_ADD(scalar_acc.as_xmm, scalar_acc.as_xmm, [reg_x_addr])
        ADD(reg_x_addr, op_size)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        tmp = YMMRegister()
        # Reduce the accumulators
        for i in range(1, len(acc_regs)):
            SIMD_ADD(acc_regs[0], acc_regs[0], acc_regs[i])
        SIMD_ADD(acc_regs[0], acc_regs[0], scalar_acc)

        if op_type == Yep32f:
            VHADDPS(acc_regs[0], acc_regs[0], acc_regs[0])
            VHADDPS(acc_regs[0], acc_regs[0], acc_regs[0])
        elif op_type == Yep64f:
            VHADDPD(acc_regs[0], acc_regs[0], acc_regs[0])
        else:
            assert False, "Kernel expects either single or double precision floating point"

        # acc_regs[0] has the sum of the top 4 elements duplicated 4 times in the upper bits
        # and the sum of the lower 4 elements duplicated 4 times in the lower bits
        # Move the upper sum into the lower bits of tmp and then add them to get the sum of all 8 elements in the accumlator
        VPERM2F128(tmp, acc_regs[0], acc_regs[0], 0x1)
        SIMD_ADD(acc_regs[0].as_xmm, acc_regs[0].as_xmm, tmp.as_xmm)
        SCALAR_MOV([reg_z_addr], acc_regs[0].as_xmm)
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_empty_arrays):
        if op_type == Yep32f:
            MOV(dword[reg_z_addr], 0)
        elif op_type == Yep64f:
            MOV(qword[reg_z_addr], 0)
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatus.YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatus.YepStatusMisalignedPointer)

def sum_squared_Haswell(arg_x, arg_z, arg_n):
    op_size = arg_x.c_type.base.size
    op_type = arg_x.c_type.base
    unroll_factor = 5

    SIMD_MOV, SIMD_ADD, SIMD_ALIGNED_MOV = avx2_vector_instruction_select(op_type, op_type, "add")
    _, SIMD_MUL, _ = avx2_vector_instruction_select(op_type, op_type, "multiply")
    SCALAR_MOV, SCALAR_ADD, _ = avx2_scalar_instruction_select(op_type, op_type, "add")
    _, SCALAR_MUL, _ = avx2_scalar_instruction_select(op_type, op_type, "multiply")

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


    align_loop = Loop()
    scalar_loop = Loop()

    acc_regs = [YMMRegister() for _ in range(unroll_factor)]
    scalar_acc = YMMRegister()
    op_regs = [YMMRegister() for _ in range(unroll_factor)]

    # Zero out all of the accumulation registers
    for acc_reg in acc_regs:
        VXORPS(acc_reg, acc_reg, acc_reg)
    VXORPS(scalar_acc, scalar_acc, scalar_acc)

    # Align the X input on YMMRegister size boundary
    op_reg = op_regs[0].as_xmm
    TEST(reg_x_addr, YMMRegister.size - 1)
    JZ(align_loop.end)
    with align_loop:
        SCALAR_MOV(op_reg, [reg_x_addr])
        SCALAR_MUL(op_reg, op_reg, op_reg) # Square this value
        SCALAR_ADD(scalar_acc.as_xmm, scalar_acc.as_xmm, op_reg)
        ADD(reg_x_addr, op_size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_x_addr, YMMRegister.size - 1)
        JNZ(align_loop.begin)

    instruction_columns = [InstructionStream() for _ in range(3)]
    instruction_offsets = (0, 1, 2)
    for i in range(unroll_factor):
        with instruction_columns[0]:
            SIMD_ALIGNED_MOV(op_regs[i], [reg_x_addr + i * YMMRegister.size])
        with instruction_columns[1]:
            SIMD_MUL(op_regs[i], op_regs[i], op_regs[i])
        with instruction_columns[2]:
            SIMD_ADD(acc_regs[i], acc_regs[i], op_regs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, YMMRegister.size * unroll_factor)

    software_pipelined_loop(reg_length, unroll_factor * YMMRegister.size / op_size, instruction_columns, instruction_offsets)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    with scalar_loop:
        SCALAR_MOV(op_reg, [reg_x_addr])
        SCALAR_MUL(op_reg, op_reg, op_reg) # Square this value
        SCALAR_ADD(scalar_acc.as_xmm, scalar_acc.as_xmm, op_reg)
        ADD(reg_x_addr, op_size)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_x_addr, YMMRegister.size - 1)
        JNZ(align_loop.begin)

    with LABEL(ret_ok):
        tmp = YMMRegister()
        # Reduce the accumulators
        for i in range(1, len(acc_regs)):
            SIMD_ADD(acc_regs[0], acc_regs[0], acc_regs[i])
        SIMD_ADD(acc_regs[0], acc_regs[0], scalar_acc)

        if op_type == Yep32f:
            VHADDPS(acc_regs[0], acc_regs[0], acc_regs[0])
            VHADDPS(acc_regs[0], acc_regs[0], acc_regs[0])
        elif op_type == Yep64f:
            VHADDPD(acc_regs[0], acc_regs[0], acc_regs[0])
        else:
            assert False, "Kernel expects either single or double precision floating point"

        # acc_regs[0] has the sum of the top 4 elements duplicated 4 times in the upper bits
        # and the sum of the lower 4 elements duplicated 4 times in the lower bits
        # Move the upper sum into the lower bits of tmp and then add them to get the sum of all 8 elements in the accumlator
        VPERM2F128(tmp, acc_regs[0], acc_regs[0], 0x1)
        SIMD_ADD(acc_regs[0].as_xmm, acc_regs[0].as_xmm, tmp.as_xmm)
        SCALAR_MOV([reg_z_addr], acc_regs[0].as_xmm)
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_empty_arrays):
        if op_type == Yep32f:
            MOV(dword[reg_z_addr], 0)
        elif op_type == Yep64f:
            MOV(qword[reg_z_addr], 0)
        RETURN(YepStatus.YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatus.YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatus.YepStatusMisalignedPointer)
