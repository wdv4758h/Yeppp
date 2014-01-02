SET(CMAKE_SYSTEM_NAME "Android")
SET(CMAKE_SYSTEM_PROCESSOR "arm")

SET(YEPPP_TARGET_NAME "android-armeabiv7a")

SET(CMAKE_C_COMPILER arm-linux-androideabi-gcc)
SET(CMAKE_ASM_COMPILER arm-linux-androideabi-gcc)

SET(ANDROID_SYSROOT "$ENV{ANDROID_NDK_ROOT}/platforms/android-3/arch-arm")
# Headers
SET(CMAKE_C_FLAGS "-I${ANDROID_SYSROOT}/usr/include")
# Target-specific options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -marm -march=armv7-a -mtune=cortex-a9 -mfloat-abi=softfp")
# Code-generation options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -nostdlib -fPIC -Wno-psabi -fno-unwind-tables -Wa,--noexecstack")
# Optimization options
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -ffunction-sections -fdata-sections -O3 -fomit-frame-pointer" CACHE STRING "android-armeabiv7a")

# Target-specific options
SET(CMAKE_ASM_FLAGS "-I${CMAKE_SOURCE_DIR}/sources/arm -march=armv7-a")
# Code-generation options
SET(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} -Wa,--noexecstack" CACHE STRING "android-armeabiv7a")
