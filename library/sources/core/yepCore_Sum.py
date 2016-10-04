import peachpy.x86_64.uarch as uarch
import peachpy.x86_64.isa as isa
from peachpy.x86_64.function import Function
from peachpy.function import Argument
from peachpy.c.types import ptr
import peachpy.c.types as ctypes
from common.YepStatus import YepStatus
from kernels.sum_reduction import sum_Haswell, sum_squared_Haswell

arg_x = Argument(ptr(ctypes.const_Yep32f), name="xPointer")
arg_z = Argument(ptr(ctypes.Yep32f), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Sum_V32f_S32f",
        (arg_x, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as yepCore_Sum_V32f_S32f:
    sum_Haswell(arg_x, arg_z, arg_n)

with Function("yepCore_SumSquares_V32f_S32f",
        (arg_x, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as yepCore_SumSquares_V32f_S32f:
    sum_squared_Haswell(arg_x, arg_z, arg_n)


arg_x = Argument(ptr(ctypes.const_Yep64f), name="xPointer")
arg_z = Argument(ptr(ctypes.Yep64f), name="zPointer")
arg_n = Argument(ctypes.YepSize, name="length")

with Function("yepCore_Sum_V64f_S64f",
        (arg_x, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as yepCore_Sum_V64f_S64f:
    sum_Haswell(arg_x, arg_z, arg_n)

with Function("yepCore_SumSquares_V64f_S64f",
        (arg_x, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as yepCore_SumSquares_V64f_S64f:
    sum_squared_Haswell(arg_x, arg_z, arg_n)
