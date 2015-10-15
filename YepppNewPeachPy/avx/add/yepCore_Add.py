from peachpy.x86_64 import *
from peachpy import *
from add_generic import add_generic
# Load functions in the unit test not here  TODO


##
# Adds vectors of 8-bit signed integers
# and stores them as 8-bit signed integers
##
arg_x = Argument(ptr(const_Yep8s), name="xPointer")
arg_y = Argument(ptr(const_Yep8s), name="yPointer")
arg_z = Argument(ptr(Yep8s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V8sV8s_V8s",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V8sV8s_V8s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V8sV8s_V8s = Add_V8sV8s_V8s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 8-bit signed integers
# and store as 16-bit signed integers
#
arg_x = Argument(ptr(const_Yep8s), name="xPointer")
arg_y = Argument(ptr(const_Yep8s), name="yPointer")
arg_z = Argument(ptr(Yep16s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V8sV8s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V8sV8s_V16s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V8sV8s_V16s = Add_V8sV8s_V16s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 8-bit unsigned ints
# and store as 16-bit unsigned ints
##
arg_x = Argument(ptr(const_Yep8u), name="xPointer")
arg_y = Argument(ptr(const_Yep8u), name="yPointer")
arg_z = Argument(ptr(Yep16u), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V8uV8u_V16u",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V8uV8u_V16u:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V8uV8u_V16u = Add_V8uV8u_V16u.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 16-bit signed ints
# and stores them as 16-bit signed ints
##
arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep16s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V16sV16s_V16s",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V16sV16s_V16s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V16sV16s_V16s = Add_V16sV16s_V16s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 16-bit signed ints
# and stores them as 32-bit signed ints
##
arg_x = Argument(ptr(const_Yep16s), name="xPointer")
arg_y = Argument(ptr(const_Yep16s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V16sV16s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V16sV16s_V32s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V16sV16s_V32s = Add_V16sV16s_V32s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 16-bit unsigned ints
# and stores them as 32-bit unsigned ints
##
arg_x = Argument(ptr(const_Yep16u), name="xPointer")
arg_y = Argument(ptr(const_Yep16u), name="yPointer")
arg_z = Argument(ptr(Yep32u), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V16uV16u_V32u",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V16uV16u_V32u:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V16uV16u_V32u = Add_V16uV16u_V32u.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 32-bit signed integers
# and stores them as 32-bit signed integers
##
arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_z = Argument(ptr(Yep32s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32sV32s_V32s",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V32sV32s_V32s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V32sV32s_V32s = Add_V32sV32s_V32s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 32-bit signed integers
# and stores them as 64-bit signed integers
##
arg_x = Argument(ptr(const_Yep32s), name="xPointer")
arg_y = Argument(ptr(const_Yep32s), name="yPointer")
arg_z = Argument(ptr(Yep64s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32sV32s_V64s",
        (arg_x, arg_y, arg_z, arg_n),
        int64_t) as Add_V32sV32s_V64s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V32sV32s_V64s = Add_V32sV32s_V64s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 32-bit unsigned ints
# and stores them as 64-bit unsigned ints
##
arg_x = Argument(ptr(const_Yep32u), name="xPointer")
arg_y = Argument(ptr(const_Yep32u), name="yPointer")
arg_z = Argument(ptr(Yep64u), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32uV32u_V64u",
        (arg_x, arg_y, arg_z, arg_n),
        int64_t) as Add_V32uV32u_V64u:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V32uV32u_V64u = Add_V32uV32u_V64u.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 64-bit signed ints
# and stores them as 64-bit signed ints
##
arg_x = Argument(ptr(const_Yep64s), name="xPointer")
arg_y = Argument(ptr(const_Yep64s), name="yPointer")
arg_z = Argument(ptr(Yep64s), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V64sV64s_V64s",
        (arg_x, arg_y, arg_z, arg_n),
        int64_t) as Add_V64sV64s_V64s:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V64sV64s_V64s = Add_V64sV64s_V64s.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 32-bit floats
# and stores them as 32-bit floats
##
arg_x = Argument(ptr(const_Yep32f), name="xPointer")
arg_y = Argument(ptr(const_Yep32f), name="yPointer")
arg_z = Argument(ptr(Yep32f), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V32fV32f_V32f",
        (arg_x, arg_y, arg_z, arg_n),
        int32_t) as Add_V32fV32f_V32f:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V32fV32f_V32f = Add_V32fV32f_V32f.finalize(peachpy.x86_64.abi.detect()).encode()


##
# Adds vectors of 64-bit floats
# and stores them as 64-bit floats
##
arg_x = Argument(ptr(const_Yep64f), name="xPointer")
arg_y = Argument(ptr(const_Yep64f), name="yPointer")
arg_z = Argument(ptr(Yep64f), name="sumPointer")
arg_n = Argument(YepSize, name="length")

with Function("yepCore_Add_V64fV64f_V64f",
        (arg_x, arg_y, arg_z, arg_n),
        int64_t) as Add_V64fV64f_V64f:
    add_generic(arg_x, arg_y, arg_z, arg_n)

yepCore_Add_V64fV64f_V64f = Add_V64fV64f_V64f.finalize(peachpy.x86_64.abi.detect()).encode()

