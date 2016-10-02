import peachpy.x86_64.uarch as uarch
import peachpy.x86_64.isa as isa
from peachpy.x86_64.function import Function
from peachpy.function import Argument
from peachpy.c.types import ptr
import peachpy.c.types as ctypes
from common.YepStatus import YepStatus
from kernels.dot_product import dot_product_V32fV32f_S32f_Haswell

arg_x = Argument(ptr(ctypes.const_Yep32f), name="xPointer")
arg_y = Argument(ptr(ctypes.const_Yep32f), name="yPointer")
arg_z = Argument(ptr(ctypes.Yep32f), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_DotProduct_V32fV32f_S32f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as yepCore_DotProduct_V32fV32f_S32f:
    dot_product_V32fV32f_S32f_Haswell(arg_x, arg_y, arg_z, arg_n)
