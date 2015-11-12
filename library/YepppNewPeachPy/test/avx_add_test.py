import unittest2
import numpy
from peachpy.x86_64 import *
from peachpy import *
import ctypes

sys.path.append("..")
import avx

##
# Tests the correctness of YepCore integer addition kernels
##
class TestAddIntegers(unittest2.TestCase):

    def setUp(self):
        self.n = 1024*64
        self.a = numpy.random.random_integers(1,10,self.n)
        self.b = numpy.random.random_integers(1,10,self.n)

    def test_add_V8sV8s_V8s(self):
        a_tmp = self.a.astype(numpy.int8)
        b_tmp = self.b.astype(numpy.int8)
        c = numpy.empty([self.n]).astype(numpy.int8)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_byte))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_byte))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_byte))

        func = avx.add.yepCore_Add.yepCore_Add_V8sV8s_V8s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V8sV8s_V16s(self):
        a_tmp = self.a.astype(numpy.int8)
        b_tmp = self.b.astype(numpy.int8)
        c = numpy.empty([self.n]).astype(numpy.int16)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int8))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int8))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))

        func = avx.add.yepCore_Add.yepCore_Add_V8sV8s_V16s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V8uV8u_V16u(self):
        a_tmp = self.a.astype(numpy.uint8)
        b_tmp = self.b.astype(numpy.uint8)
        c = numpy.empty([self.n]).astype(numpy.uint16)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

        func = avx.add.yepCore_Add.yepCore_Add_V8uV8u_V16u.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V16sV16s_V16s(self):
        a_tmp = self.a.astype(numpy.int16)
        b_tmp = self.b.astype(numpy.int16)
        c = numpy.empty([self.n]).astype(numpy.int16)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))

        func = avx.add.yepCore_Add.yepCore_Add_V16sV16s_V16s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V16sV16s_V32s(self):
        a_tmp = self.a.astype(numpy.int16)
        b_tmp = self.b.astype(numpy.int16)
        c = numpy.empty([self.n]).astype(numpy.int32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

        func = avx.add.yepCore_Add.yepCore_Add_V16sV16s_V32s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V16uV16u_V32u(self):
        a_tmp = self.a.astype(numpy.uint16)
        b_tmp = self.b.astype(numpy.uint16)
        c = numpy.empty([self.n]).astype(numpy.uint32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))

        func = avx.add.yepCore_Add.yepCore_Add_V16uV16u_V32u.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V32sV32s_V32s(self):
        a_tmp = self.a.astype(numpy.int32)
        b_tmp = self.b.astype(numpy.int32)
        c = numpy.empty([self.n]).astype(numpy.int32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

        func = avx.add.yepCore_Add.yepCore_Add_V32sV32s_V32s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V32sV32s_V64s(self):
        a_tmp = self.a.astype(numpy.int32)
        b_tmp = self.b.astype(numpy.int32)
        c = numpy.empty([self.n]).astype(numpy.int64)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int64))

        func = avx.add.yepCore_Add.yepCore_Add_V32sV32s_V64s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V32uV32u_V64u(self):
        a_tmp = self.a.astype(numpy.uint32)
        b_tmp = self.b.astype(numpy.uint32)
        c = numpy.empty([self.n]).astype(numpy.uint64)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_uint64))

        func = avx.add.yepCore_Add.yepCore_Add_V32uV32u_V64u.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V64sV64s_V64s(self):
        a_tmp = self.a.astype(numpy.int64)
        b_tmp = self.b.astype(numpy.int64)
        c = numpy.empty([self.n]).astype(numpy.int64)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int64))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_int64))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_int64))

        func = avx.add.yepCore_Add.yepCore_Add_V64sV64s_V64s.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

##
# Test correctness of YepCore float addition kernels
##
class TestAddFloats(unittest2.TestCase):

    def setUp(self):
        self.n = 1024*64
        self.a = numpy.random.random([self.n])
        self.b = numpy.random.random([self.n])

    def test_add_V32fV32f_V32f(self):
        a_tmp = self.a.astype(numpy.float32)
        b_tmp = self.b.astype(numpy.float32)
        c = numpy.empty([self.n]).astype(numpy.float32)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        func = avx.add.yepCore_Add.yepCore_Add_V32fV32f_V32f.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])

    def test_add_V64fV64f_V64f(self):
        a_tmp = self.a.astype(numpy.float64)
        b_tmp = self.b.astype(numpy.float64)
        c = numpy.empty([self.n]).astype(numpy.float64)
        a_ptr = a_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        b_ptr = b_tmp.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_ptr = c.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        func = avx.add.yepCore_Add.yepCore_Add_V64fV64f_V64f.load()
        self.assertEqual(func(a_ptr, b_ptr, c_ptr, self.n), 0)

        for i in range(self.n):
            self.assertEqual(a_tmp[i] + b_tmp[i], c[i])



if __name__ == "__main__":
    unittest2.main()
