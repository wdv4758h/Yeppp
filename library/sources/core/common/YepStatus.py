from peachpy import *
from peachpy.x86_64 import *

YepStatus = Type("YepStatus", size=4, is_signed_integer=True, header="yepTypes.h")

YepStatusOk = 0
YepStatusNullPointer = 1
YepStatusMisalignedPointer = 2
