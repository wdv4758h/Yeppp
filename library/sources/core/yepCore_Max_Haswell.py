from peachpy.x86_64 import *
from peachpy import *
from kernels.binop.binop_VV_V import binop_VV_V
from common.YepStatus import *

# =======================================================================
# =======================================================================
# VECTOR/VECTOR MAX
# =======================================================================
# =======================================================================

# arg_x = Argument(ptr(const_Yep8s), name="xPointer")
# arg_y = Argument(ptr(const_Yep8s), name="yPointer")
# arg_z = Argument(ptr(Yep8s), name="zPointer")
# arg_n = Argument(YepSize, name="length")

# with Function("yepCore_Max_V8sV8s_V8s",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.haswell + isa.avx2) as Max_V8sV8s_V8s:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


# arg_x = Argument(ptr(const_Yep8u), name="xPointer")
# arg_y = Argument(ptr(const_Yep8u), name="yPointer")
# arg_z = Argument(ptr(Yep8u), name="zPointer")
# arg_n = Argument(YepSize, name="length")

# with Function("yepCore_Max_V8uV8u_V8u",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.haswell + isa.avx2) as Max_V8uV8u_V8u:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


# arg_x = Argument(ptr(const_Yep16s), name="xPointer")
# arg_y = Argument(ptr(const_Yep16s), name="yPointer")
# arg_z = Argument(ptr(Yep16s), name="zPointer")
# arg_n = Argument(YepSize, name="length")

# with Function("yepCore_Max_V16sV16s_V16s",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.haswell + isa.avx2) as Max_V16sV16s_V16s:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


# arg_x = Argument(ptr(const_Yep16u), name="xPointer")
# arg_y = Argument(ptr(const_Yep16u), name="yPointer")
# arg_z = Argument(ptr(Yep16u), name="zPointer")
# arg_n = Argument(YepSize, name="length")

# with Function("yepCore_Max_V16uV16u_V16u",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.haswell + isa.avx2) as Max_V16uV16u_V16u:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


# arg_x = Argument(ptr(const_Yep32s), name="xPointer")
# arg_y = Argument(ptr(const_Yep32s), name="yPointer")
# arg_z = Argument(ptr(Yep32s), name="zPointer")
# arg_n = Argument(YepSize, name="length")

# with Function("yepCore_Max_V32sV32s_V32s",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.haswell + isa.avx2) as Max_V32sV32s_V32s:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


# arg_x = Argument(ptr(const_Yep32u), name="xPointer")
# arg_y = Argument(ptr(const_Yep32u), name="yPointer")
# arg_z = Argument(ptr(Yep32u), name="zPointer")
# arg_n = Argument(YepSize, name="length")

# with Function("yepCore_Max_V32uV32u_V32u",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.haswell + isa.avx2) as Max_V32uV32u_V32u:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


arg_x = Argument(ptr(const_Yep32f), name="xPointer")
arg_y = Argument(ptr(const_Yep32f), name="yPointer")
arg_z = Argument(ptr(Yep32f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Max_V32fV32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Max_V32fV32f_V32f:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")


arg_x = Argument(ptr(const_Yep64f), name="xPointer")
arg_y = Argument(ptr(const_Yep64f), name="yPointer")
arg_z = Argument(ptr(Yep64f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Max_V64fV64f_V64f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Max_V64fV64f_V64f:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "max", "AVX2")
