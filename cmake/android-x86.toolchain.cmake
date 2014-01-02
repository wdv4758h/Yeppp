SET(CMAKE_SYSTEM_NAME "Android")
SET(CMAKE_SYSTEM_PROCESSOR "x86")

SET(YEPPP_TARGET_NAME "android-x86")

SET(CMAKE_C_COMPILER i686-linux-android-gcc)

# Target-specific options
SET(CMAKE_C_FLAGS "-m32 -march=pentium -mtune=corei7")
# Code-generation options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -nostdlib -fPIC -Wno-psabi -fno-unwind-tables -Wa,--noexecstack")
# Optimization options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffunction-sections -fdata-sections -O3 -fomit-frame-pointer" CACHE STRING "linux-x86")
