set(CMAKE_SYSTEM_NAME "Android")
set(CMAKE_SYSTEM_PROCESSOR "x86")

set(YEPPP_TARGET_NAME "android-x86")

if("$ENV{ANDROID_NDK_ROOT}" STREQUAL "")
	message(FATAL_ERROR "Could not find Android NDK")
endif()

include(CMakeForceCompiler)
CMAKE_FORCE_C_COMPILER(i686-linux-android-gcc GNU)
CMAKE_FORCE_CXX_COMPILER(i686-linux-android-g++ GNU)
set(CMAKE_ASM-ATT_COMPILER i686-linux-android-as)

set(ANDROID_SYSROOT "$ENV{ANDROID_NDK_ROOT}/platforms/android-9/arch-x86")
# Headers
set(CMAKE_C_FLAGS "-I${ANDROID_SYSROOT}/usr/include --sysroot=${ANDROID_SYSROOT}")
# Target-specific options
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -m32 -msse3 -mtune=atom")
# Code-generation options
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -nostdlib -fPIC -Wno-psabi -fno-unwind-tables -Wa,--noexecstack")
# Optimization options
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffunction-sections -fdata-sections -O3 -fomit-frame-pointer" CACHE STRING "")
# C++-specific options
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -fno-rtti -fno-exceptions" CACHE STRING "")

# Target-specific options
set(CMAKE_ASM-ATT_FLAGS "-march=mips32")
# Code-generation options
set(CMAKE_ASM-ATT_FLAGS "${CMAKE_ASM_FLAGS} --noexecstack" CACHE STRING "")

# Linker options
set(CMAKE_SHARED_LINKER_FLAGS "-fPIC -nostdlib --sysroot=${ANDROID_SYSROOT} -Wl,-z,noexecstack -Wl,--no-undefined -Wl,--gc-sections" CACHE STRING "")
