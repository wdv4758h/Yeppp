from peachpy import *
from peachpy.x86_64 import *
from kernels.binop.binop_VV_V import binop_VV_V
from kernels.binop.binop_VS_V import binop_VS_V
from kernels.binop.binop_IVV_IV import binop_IVV_IV
from kernels.binop.binop_IVS_IV import binop_IVS_IV
from common.YepStatus import *

# =======================================================================
# =======================================================================
# MULTIPLY VECTOR WITH VECTOR
# =======================================================================
# =======================================================================
arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep16s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V16sV16s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V16sV16s_V16s:
    multiply_VV_V(arg_x, arg_y, arg_z, arg_n, "AVX2")

yepCore_Multiply_V16sV16s_V16s_Haswell = Multiply_V16sV16s_V16s.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V32sV32s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V32sV32s_V32s:
    multiply_VV_V(arg_x, arg_y, arg_z, arg_n, "AVX2")

yepCore_Multiply_V32sV32s_V32s = Multiply_V32sV32s_V32s.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep32f), name="xPointer")
arg_y = Argument(ptr(const_Yep32f), name="yPointer")
arg_z = Argument(ptr(Yep32f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V32fV32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V32fV32f_V32f:
    multiply_VV_V(arg_x, arg_y, arg_z, arg_n, "AVX2")

yepCore_Multiply_V32fV32f_V32f_Haswell = Multiply_V32fV32f_V32f.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep64f), name="xPointer")
arg_y = Argument(ptr(const_Yep64f), name="yPointer")
arg_z = Argument(ptr(Yep64f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V64fV64f_V64f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V64fV64f_V64f:
    multiply_VV_V(arg_x, arg_y, arg_z, arg_n, "AVX2")

yepCore_Multiply_V64fV64f_V64f_Haswell = Multiply_V64fV64f_V64f.finalize(peachpy.x86_64.abi.detect()).encode()


# =======================================================================
# =======================================================================
# MULTIPLY SCALAR WITH VECTOR
# =======================================================================
# =======================================================================
arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(Yep16s, name="y")
arg_z = Argument(ptr(Yep16s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V16sS16s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V16sS16s_V16s:
    binop_VS_V(arg_x, arg_y, arg_z, arg_n, "multiply", "AVX2")

yepCore_Multiply_V16sS16s_V16s_Haswell = Multiply_V16sS16s_V16s.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(Yep32s, name="y")
arg_z = Argument(ptr(Yep32s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V32sS32s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V32sS32s_V32s:
    binop_VS_V(arg_x, arg_y, arg_z, arg_n, "multiply", "AVX2")

yepCore_Multiply_V32sS32s_V32s = Multiply_V32sS32s_V32s.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep32f), name="xPointer")
arg_y = Argument(Yep32f, name="y")
arg_z = Argument(ptr(Yep32f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V32fS32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V32fS32f_V32f:
    binop_VS_V(arg_x, arg_y, arg_z, arg_n, "multiply", "AVX2")

yepCore_Multiply_V32fS32f_V32f_Haswell = Multiply_V32fS32f_V32f.finalize(peachpy.x86_64.abi.detect()).encode()


arg_x = Argument(ptr(const_Yep64f), name="xPointer")
arg_y = Argument(Yep64f, name="y")
arg_z = Argument(ptr(Yep64f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_V64fS64f_V64f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_V64fS64f_V64f:
    binop_VS_V(arg_x, arg_y, arg_z, arg_n, "multiply", "AVX2")

yepCore_Multiply_V64fS64f_V64f_Haswell = Multiply_V64fS64f_V64f.finalize(peachpy.x86_64.abi.detect()).encode()


# =======================================================================
# =======================================================================
# MULTIPLY VECTOR INPLACE
# =======================================================================
# =======================================================================
arg_x = Argument(ptr(Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV16sV16s_IV16s",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV16sV16s_IV16s:
    binop_IVV_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


arg_x = Argument(ptr(Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV32sV32s_IV32s",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV32sV32s_IV32s:
    binop_IVV_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


arg_x = Argument(ptr(Yep32f), name="xPointer")
arg_y = Argument(ptr(const_Yep32f), name="yPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV32fV32f_IV32f",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV32fV32f_IV32f:
    binop_IVV_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


arg_x = Argument(ptr(Yep64f), name="xPointer")
arg_y = Argument(ptr(const_Yep64f), name="yPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV64fV64f_IV64f",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV64fV64f_IV64f:
    binop_IVV_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


# =======================================================================
# =======================================================================
# MULTIPLY VECTOR WITH SCALAR INPLACE
# =======================================================================
# =======================================================================
arg_x = Argument(ptr(Yep16s), name="xPointer")
arg_y = Argument(Yep16s, name="y")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV16sS16s_IV16s",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV16sS16s_IV16s:
    binop_IVS_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


arg_x = Argument(ptr(Yep32s), name="xPointer")
arg_y = Argument(Yep32s, name="y")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV32sS32s_IV32s",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV32sS32s_IV32s:
    binop_IVS_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


arg_x = Argument(ptr(Yep32f), name="xPointer")
arg_y = Argument(Yep32f, name="y")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV32fS32f_IV32f",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV32fS32f_IV32f:
    binop_IVS_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")


arg_x = Argument(ptr(Yep64f), name="xPointer")
arg_y = Argument(Yep64f, name="y")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Multiply_IV64fS64f_IV64f",
        (arg_x, arg_y, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Multiply_IV64fS64f_IV64f:
    binop_IVS_IV(arg_x, arg_y, arg_n, "multiply", "AVX2")
