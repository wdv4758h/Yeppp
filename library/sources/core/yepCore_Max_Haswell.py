from peachpy.x86_64 import *
from peachpy import *
from kernels.binop.binop_VV_V import binop_VV_V
from common.YepStatus import *

# =======================================================================
# =======================================================================
# VECTOR/VECTOR MAX
# =======================================================================
# =======================================================================
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
