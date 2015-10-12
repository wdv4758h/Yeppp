from peachpy import *
from peachpy.x86_64 import *
from peachpy.x86_64.registers import *

arg_x = Argument(ptr(const_Yep32f), name="xPointer")
arg_y = Argument(ptr(const_Yep32f), name="yPointer")
arg_z = Argument(ptr(Yep32f), name="zPointer")
arg_n = Argument(YepSize, name="length")
with Function("yepCore_Add_V32fV32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t, target=uarch.default + isa.avx512f + isa.avx512bw) as yepCore_Add_V32fV32f_V32f:

    ret_ok = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()

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
    TEST(reg_z_addr, ZMMRegister.size - 1)
    JNZ(ret_misaligned_pointer)

    reg_length = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_ok)

    align_loop = Loop()
    vector_loop = Loop()
    scalar_loop = Loop()

    scalar_x = XMMRegister()
    scalar_y = XMMRegister()

    TEST(reg_z_addr, ZMMRegister.size - 1)
    JZ(align_loop.end)
    with align_loop:
        VMOVSS(scalar_x, [reg_x_addr])
        VMOVSS(scalar_y, [reg_y_addr])
        VADDSS(scalar_x, scalar_x, scalar_y)
        VMOVSS([reg_z_addr], scalar_x)
        ADD(reg_x_addr, 4)
        ADD(reg_y_addr, 4)
        ADD(reg_z_addr, 4)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_z_addr, ZMMRegister.size - 1)
        JNZ(align_loop.begin)

    vector_x = ZMMRegister()
    vector_y = ZMMRegister()
    k = k1

    with vector_loop:
        VMOVUPS(vector_x(k), [reg_x_addr])
        VMOVUPS(vector_y(k), [reg_y_addr])
        VADDPS(vector_x(k), vector_x, vector_y)
        VMOVAPS([reg_z_addr], vector_x)
        ADD(reg_x_addr, ZMMRegister.size)
        ADD(reg_y_addr, ZMMRegister.size)
        ADD(reg_z_addr, ZMMRegister.size)
        SUB(reg_length, 16)
        JZ(ret_ok)
        CMP(reg_length, 16)
        JNC(vector_loop.begin)

    with scalar_loop:
        VMOVSS(scalar_x, [reg_x_addr])
        VMOVSS(scalar_y, [reg_y_addr])
        VADDSS(scalar_x, scalar_x, scalar_y)
        VMOVSS([reg_z_addr], scalar_x)
        ADD(reg_x_addr, 4)
        ADD(reg_y_addr, 4)
        ADD(reg_z_addr, 4)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(0)

    with LABEL(ret_null_pointer):
        RETURN(1)

    with LABEL(ret_misaligned_pointer):
        RETURN(2)


# if __name__ == "__main__":
#     yepCore_Add_V32fV32f_V32f = yepCore_Add_V32fV32f_V32f.finalize(peachpy.x86_64.abi.detect()).encode().load()

#     import numpy
#     import ctypes

#     n = 1024*1024*64
#     reps = 10
#     a = numpy.random.random([n]).astype(numpy.float32)
#     b = numpy.random.random([n]).astype(numpy.float32)
#     c = numpy.empty([n]).astype(numpy.float32)
#     a_ptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
#     b_ptr = b.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
#     c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
#     yepCore_Add_V32fV32f_V32f(a_ptr, b_ptr, c_ptr, n)

#     print "Addition finished, checking for correctness"
#     is_correct = True
#     for i in range(n):
#         if a[i] + b[i] != c[i]:
#             is_correct = False
#             print i
#     if is_correct:
#         print "Output is correct"
#     else:
#         print "There was an error"




