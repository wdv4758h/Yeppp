from peachpy import *
from peachpy.x86_64 import *
import ctypes

arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V16sV16s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as yepCore_Multiply_V16sV16s_V32s:

    ret_ok = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()

    reg_length = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_ok) # There are no elements to process

##
# Load arguments and test for null pointers / misalignment
##
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
    TEST(reg_z_addr, arg_z.ctype.base.size * 8 - 1)
    JZ(ret_misaligned_pointer)

    vector_loop = Loop()
    scalar_loop = Loop()

    vector_x_reg = XMMRegister()
    vector_y_reg = XMMRegister()
    vector_low_res = XMMRegister()
    vector_high_res = XMMRegister()

    CMP(reg_length, XMMRegister.size / arg_x.ctype.base.size) # Not enough elements to use SIMD instructions
    JB(vector_loop.end)
    with vector_loop:
        VMOVDQU(vector_x_reg, [reg_x_addr])
        VMOVDQU(vector_y_reg, [reg_y_addr])
        VPMULLW(vector_low_res, vector_x_reg, vector_y_reg)
        VPMULHW(vector_high_res, vector_x_reg, vector_y_reg)
        VPUNPCKHWD(vector_x_reg, vector_low_res, vector_high_res)
        VPUNPCKLWD(vector_y_reg, vector_low_res, vector_high_res)
        VMOVDQU([reg_z_addr], vector_x_reg)
        VMOVDQU([reg_z_addr + XMMRegister.size], vector_y_reg)
        ADD(reg_x_addr, XMMRegister.size)
        ADD(reg_y_addr, XMMRegister.size)
        ADD(reg_z_addr, 2 * XMMRegister.size)
        SUB(reg_length, XMMRegister.size / arg_x.ctype.base.size)
        CMP(reg_length, XMMRegister.size / arg_x.ctype.base.size)
        JAE(vector_loop.begin)

    TEST(reg_length, reg_length)
    JZ(ret_ok)
    scalar_x_reg = GeneralPurposeRegister32()
    scalar_y_reg = GeneralPurposeRegister32()
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
        RETURN(0)

    with LABEL(ret_null_pointer):
        RETURN(1)

    with LABEL(ret_misaligned_pointer):
        RETURN(2)

if __name__ == "__main__":
    pyfunc = yepCore_Multiply_V16sV16s_V32s.finalize(peachpy.x86_64.abi.detect()).encode().load()
    import numpy
    n = 1024
    a = numpy.random.random_integers(1,10,n).astype(numpy.int16)
    b = numpy.random.random_integers(1,10,n).astype(numpy.int16)
    c = numpy.empty([n]).astype(numpy.int32)
    a_ptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
    b_ptr = b.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
    c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

    pyfunc(a_ptr, b_ptr, c_ptr, n)

    for i in range(n):
        print "Output val", c[i]
        print "Actual val", a[i] * b[i]
        if a[i] * b[i] != c[i]:
            print i
