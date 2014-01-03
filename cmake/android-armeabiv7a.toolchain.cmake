SET(CMAKE_SYSTEM_NAME "Android")
SET(CMAKE_SYSTEM_PROCESSOR "arm")

SET(YEPPP_TARGET_NAME "android-armeabiv7a")

if("$ENV{ANDROID_NDK_ROOT}" STREQUAL "")
	message(FATAL_ERROR "Could not find Android NDK")
endif()

include(CMakeForceCompiler)
CMAKE_FORCE_C_COMPILER(arm-linux-androideabi-gcc GNU)
CMAKE_FORCE_CXX_COMPILER(arm-linux-androideabi-g++ GNU)
set(CMAKE_ASM-ATT_COMPILER arm-linux-androideabi-as)

SET(ANDROID_SYSROOT "$ENV{ANDROID_NDK_ROOT}/platforms/android-3/arch-arm")
# Headers
SET(CMAKE_C_FLAGS "-I${ANDROID_SYSROOT}/usr/include --sysroot=${ANDROID_SYSROOT}")
# Target-specific options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -marm -march=armv7-a -mtune=cortex-a9 -mfloat-abi=softfp")
# Code-generation options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -nostdlib -fPIC -Wno-psabi -fno-unwind-tables -Wa,--noexecstack")
# Optimization options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffunction-sections -fdata-sections -O3 -fomit-frame-pointer" CACHE STRING "")

# Target-specific options
SET(CMAKE_ASM_FLAGS "-I${CMAKE_SOURCE_DIR}/sources/arm -march=armv7-a")
# Code-generation options
SET(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} -Wa,--noexecstack" CACHE STRING "")
# C++-specific options
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -fno-rtti -fno-exceptions" CACHE STRING "")

# Linker options
set(CMAKE_SHARED_LINKER_FLAGS "-fPIC -nostdlib --sysroot=${ANDROID_SYSROOT} -Wl,-z,noexecstack -Wl,--no-undefined -Wl,--gc-sections" CACHE STRING "")
