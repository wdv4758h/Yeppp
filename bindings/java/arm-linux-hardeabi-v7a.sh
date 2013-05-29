#!/bin/bash
CC=arm-linux-gnueabihf-gcc
CFLAGS="-nostdlib -mthumb-interwork -march=armv7-a -mtune=cortex-a9 -mfloat-abi=hard -mfpu=vfpv3-d16 -fPIC -ffunction-sections -Wno-psabi -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -I/usr/lib/jvm/default-java/include -Wa,--noexecstack -c"
CP=cp
CPFLAGS=-r
RM=rm
RMFLAGS="-rf"
MKDIR=mkdir
MKDIRFLAGS=
IMPORT_LIBRARIES="-L../../runtime/binaries/arm-linux-hardeabi-v7a/ -L../../library/binaries/arm-linux-hardeabi-v7a/ -lyeppp -lyeprt"

$RM $RMFLAGS "binaries/arm-linux-hardeabi-v7a"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-hardeabi-v7a/"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-hardeabi-v7a/library/"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-hardeabi-v7a/core/"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-hardeabi-v7a/math/"

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/core/Add.o sources-jni/core/Add.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/core/Subtract.o sources-jni/core/Subtract.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/core/Multiply.o sources-jni/core/Multiply.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/core/DotProduct.o sources-jni/core/DotProduct.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/core/SumSquares.o sources-jni/core/SumSquares.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/math/Log.o sources-jni/math/Log.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/math/Exp.o sources-jni/math/Exp.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/math/Sin.o sources-jni/math/Sin.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/math/Cos.o sources-jni/math/Cos.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/math/Tan.o sources-jni/math/Tan.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/library/Init.o sources-jni/library/Init.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/library/Timer.o sources-jni/library/Timer.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/library/Cpu.o sources-jni/library/Cpu.c

$CC -Os $CFLAGS -o binaries/arm-linux-hardeabi-v7a/library/String.o sources-jni/library/String.c

$CC -nostdlib -Wl,-soname,libyeppp-jni.so -shared -Wl,--gc-sections binaries/arm-linux-hardeabi-v7a/core/*.o binaries/arm-linux-hardeabi-v7a/math/*.o binaries/arm-linux-hardeabi-v7a/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/arm-linux-hardeabi-v7a/libyeppp-jni.so $IMPORT_LIBRARIES

arm-linux-gnueabihf-strip binaries/arm-linux-hardeabi-v7a/libyeppp-jni.so
arm-linux-gnueabihf-strip -R .comment -R .note.gnu.build-id binaries/arm-linux-hardeabi-v7a/libyeppp-jni.so

$CP $CPFLAGS binaries/arm-linux-hardeabi-v7a/libyeppp-jni.so ../../binaries/linux/armhf/libyeppp-jni.so
