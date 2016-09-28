import peachpy.x86_64.uarch as uarch
import peachpy.x86_64.isa as isa
from peachpy.x86_64.function import Function
from peachpy.function import Argument
from peachpy.c.types import ptr
import peachpy.c.types as ctypes
from kernels.binop.binop_VV_V import binop_VV_V
from kernels.binop.binop_VS_V import binop_VS_V
from kernels.binop.binop_IVV_IV import binop_IVV_IV
from kernels.binop.binop_IVS_IV import binop_IVS_IV
from common.YepStatus import YepStatus

# =======================================================================
# =======================================================================
# VECTOR/VECTOR MIN
# =======================================================================
# =======================================================================

# arg_x = Argument(ptr(ctypes.const_Yep8s), name="xPointer")
# arg_y = Argument(ptr(ctypes.const_Yep8s), name="yPointer")
# arg_z = Argument(ptr(ctypes.Yep8s), name="zPointer")
# arg_n = Argument(ctypes.YepSize, name="length")

# with Function("yepCore_Min_V8sV8s_V8s",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V8sV8s_V8s:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


# arg_x = Argument(ptr(ctypes.const_Yep8u), name="xPointer")
# arg_y = Argument(ptr(ctypes.const_Yep8u), name="yPointer")
# arg_z = Argument(ptr(ctypes.Yep8u), name="zPointer")
# arg_n = Argument(ctypes.YepSize, name="length")

# with Function("yepCore_Min_V8uV8u_V8u",
#         (arg_x, arg_y, arg_z, arg_n),
#         YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V8uV8u_V8u:
#     binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


arg_x = Argument(ptr(ctypes.const_Yep16s), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep16s), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep16s), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Min_V16sV16s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V16sV16s_V16s:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


arg_x = Argument(ptr(ctypes.const_Yep16u), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep16u), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep16u), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Min_V16uV16u_V16u",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V16uV16u_V16u:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


arg_x = Argument(ptr(ctypes.const_Yep32s), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep32s), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep32s), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Min_V32sV32s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V32sV32s_V32s:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


arg_x = Argument(ptr(ctypes.const_Yep32u), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep32u), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep32u), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Min_V32uV32u_V32u",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V32uV32u_V32u:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


arg_x = Argument(ptr(ctypes.const_Yep32f), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep32f), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep32f), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Min_V32fV32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V32fV32f_V32f:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")


arg_x = Argument(ptr(ctypes.const_Yep64f), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep64f), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep64f), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Min_V64fV64f_V64f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.nehalem + isa.sse2) as yepCore_Min_V64fV64f_V64f:
    binop_VV_V(arg_x, arg_y, arg_z, arg_n, "min", "SSE")
