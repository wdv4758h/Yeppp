import unittest2
import numpy
from peachpy.x86_64 import *
from peachpy import *
import ctypes

sys.path.append("..")
import avx

##
# Tests for YepCore Multiplication kernels
##
class TestMultiplyIntegers(unittest2.TestCase):

    def setUp(self):
        self.n = 1024 * 64
        self.a = numpy.random.random_integers(-10,10,self.n)
        self.b = numpy.random.random_integers(-10,10,self.n)

    def test_multiply_V16sV16s_V16s(self):
        a_tmp = self.a.astype(numpy.int16)
        b_tmp = self.b.astype(numpy.int16)
        c = numpy.empty([self.n]).astype(numpy.int16)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))

        func = avx.multiply.yepCore_Multiply.yepCore_Multiply_V16sV16s_V16s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] * b_tmp[i], c[i], "Mismatch at index %d" % i)

    def test_multiply_V16sV16s_V32s(self):
        a_tmp = self.a.astype(numpy.int16)
        b_tmp = self.b.astype(numpy.int16)
        c = numpy.empty([self.n]).astype(numpy.int32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

        func = avx.multiply.yepCore_Multiply.yepCore_Multiply_V16sV16s_V32s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] * b_tmp[i], c[i], "Mismatch at index %d" % i)

    def test_multiply_V32sV32s_V32s(self):
        a_tmp = self.a.astype(numpy.int32)
        b_tmp = self.b.astype(numpy.int32)
        c = numpy.empty([self.n]).astype(numpy.int32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

        func = avx.multiply.yepCore_Multiply.yepCore_Multiply_V32sV32s_V32s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] * b_tmp[i], c[i], "Mismatch at index %d" % i)

    def test_multiply_V32sV32s_V64s(self):
        a_tmp = self.a.astype(numpy.int32)
        b_tmp = self.b.astype(numpy.int32)
        c = numpy.empty([self.n]).astype(numpy.int64)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int64))

        func = avx.multiply.yepCore_Multiply.yepCore_Multiply_V32sV32s_V64s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] * b_tmp[i], c[i], "Mismatch at index %d" % i)

class TestMultiplyFloats(unittest2.TestCase):

    def setUp(self):
        self.n = 1024*64
        self.a = numpy.random.random([self.n])
        self.b = numpy.random.random([self.n])

    def test_multiply_V32fV32f_V32f(self):
        a_tmp = self.a.astype(numpy.float32)
        b_tmp = self.b.astype(numpy.float32)
        c = numpy.empty([self.n]).astype(numpy.float32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        func = avx.multiply.yepCore_Multiply.yepCore_Multiply_V32fV32f_V32f.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] * b_tmp[i], c[i])

    def test_multiply_V64fV64f_V64f(self):
        a_tmp = self.a.astype(numpy.float64)
        b_tmp = self.b.astype(numpy.float64)
        c = numpy.empty([self.n]).astype(numpy.float64)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        func = avx.multiply.yepCore_Multiply.yepCore_Multiply_V64fV64f_V64f.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] * b_tmp[i], c[i])



if __name__ == "__main__":
    unittest2.main()
