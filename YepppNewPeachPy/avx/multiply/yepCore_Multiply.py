from peachpy import *
from peachpy.x86_64 import *
from multiply_generic import multiply_generic

arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V16sV16s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        int64_t, target=uarch.default + isa.avx2) as Multiply_V16sV16s_V32s:
    multiply_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Multiply_V16sV16s_V32s = Multiply_V16sV16s_V32s.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_z = Argument(ptr(Yep64s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V32sV32s_V64s",
        (arg_x, arg_y, arg_z, arg_n),
        int64_t, target=uarch.default + isa.avx2) as Multiply_V32sV32s_V64s:
    multiply_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Multiply_V32sV32s_V64s = Multiply_V32sV32s_V64s.finalize(peachpy.x86_64.abi.detect()).encode()

