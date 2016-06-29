from peachpy.x86_64 import *
from peachpy import *
from kernels.add_generic import add_vector_to_vector_generic, add_vector_to_scalar_generic
from common.YepStatus import *


arg_x = Argument(ptr(const_Yep8s), name="xPointer")
arg_y = Argument(ptr(const_Yep8s), name="yPointer")
arg_z = Argument(ptr(Yep8s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V8sV8s_V8s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V8sV8s_V8s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep8s), name="xPointer")
arg_y = Argument(ptr(const_Yep8s), name="yPointer")
arg_z = Argument(ptr(Yep16s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V8sV8s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V8sV8s_V16s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep8u), name="xPointer")
arg_y = Argument(ptr(const_Yep8u), name="yPointer")
arg_z = Argument(ptr(Yep16u), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V8uV8u_V16u",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V8uV8u_V16u:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep16s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V16sV16s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V16sV16s_V16s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V16sV16s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V16sV16s_V32s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep16u), name="xPointer")
arg_y = Argument(ptr(const_Yep16u), name="yPointer")
arg_z = Argument(ptr(Yep32u), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V16uV16u_V32u",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V16uV16u_V32u:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32sV32s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V32sV32s_V32s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_z = Argument(ptr(Yep64s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32sV32s_V64s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V32sV32s_V64s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep32u), name="xPointer")
arg_y = Argument(ptr(const_Yep32u), name="yPointer")
arg_z = Argument(ptr(Yep64u), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32uV32u_V64u",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V32uV32u_V64u:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep64s), name="xPointer")
arg_y = Argument(ptr(const_Yep64s), name="yPointer")
arg_z = Argument(ptr(Yep64s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V64sV64s_V64s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V64sV64s_V64s:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep32f), name="xPointer")
arg_y = Argument(ptr(const_Yep32f), name="yPointer")
arg_z = Argument(ptr(Yep32f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32fV32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V32fV32f_V32f:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep64f), name="xPointer")
arg_y = Argument(ptr(const_Yep64f), name="yPointer")
arg_z = Argument(ptr(Yep64f), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V64fV64f_V64f",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V64fV64f_V64f:
    add_vector_to_vector_generic(arg_x, arg_y, arg_z, arg_n, "avx")


arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(Yep32s, name="y")
arg_z = Argument(ptr(Yep64s), name="zPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32sS32s_V64s",
        (arg_x, arg_y, arg_z, arg_n),
        YepStatus, target=uarch.haswell + isa.avx2) as Add_V32sS32s_V64s:
    add_vector_to_scalar_generic(arg_x, arg_y, arg_z, arg_n, "avx")
