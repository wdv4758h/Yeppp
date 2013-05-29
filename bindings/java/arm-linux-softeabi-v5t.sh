#!/bin/bash
CC=arm-linux-gnueabi-gcc
CFLAGS="-nostdlib -mthumb-interwork -march=armv5t -mtune=arm1136j-s -mfloat-abi=soft -fPIC -ffunction-sections -Wno-psabi -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -I/usr/lib/jvm/default-java/include -Wa,--noexecstack -c"
CP=cp
CPFLAGS=-r
RM=rm
RMFLAGS="-rf"
MKDIR=mkdir
MKDIRFLAGS=
IMPORT_LIBRARIES="-L../../runtime/binaries/arm-linux-softeabi-v5t/ -L../../library/binaries/arm-linux-softeabi-v5t/ -lyeppp -lyeprt"

$RM $RMFLAGS "binaries/arm-linux-softeabi-v5t"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-softeabi-v5t/"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-softeabi-v5t/library/"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-softeabi-v5t/core/"
$MKDIR $MKDIRFLAGS "binaries/arm-linux-softeabi-v5t/math/"

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/core/Add.o sources-jni/core/Add.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/core/Subtract.o sources-jni/core/Subtract.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/core/Multiply.o sources-jni/core/Multiply.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/core/DotProduct.o sources-jni/core/DotProduct.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/core/SumSquares.o sources-jni/core/SumSquares.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/math/Log.o sources-jni/math/Log.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/math/Exp.o sources-jni/math/Exp.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/math/Sin.o sources-jni/math/Sin.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/math/Cos.o sources-jni/math/Cos.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/math/Tan.o sources-jni/math/Tan.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/library/Init.o sources-jni/library/Init.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/library/Timer.o sources-jni/library/Timer.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/library/Cpu.o sources-jni/library/Cpu.c

$CC -Os $CFLAGS -o binaries/arm-linux-softeabi-v5t/library/String.o sources-jni/library/String.c

$CC -nostdlib -Wl,-soname,libyeppp-jni.so -shared -Wl,--gc-sections binaries/arm-linux-softeabi-v5t/core/*.o binaries/arm-linux-softeabi-v5t/math/*.o binaries/arm-linux-softeabi-v5t/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/arm-linux-softeabi-v5t/libyeppp-jni.so $IMPORT_LIBRARIES

arm-linux-gnueabi-strip binaries/arm-linux-softeabi-v5t/libyeppp-jni.so
arm-linux-gnueabi-strip -R .comment -R .note.gnu.build-id binaries/arm-linux-softeabi-v5t/libyeppp-jni.so

$CP $CPFLAGS binaries/arm-linux-softeabi-v5t/libyeppp-jni.so ../../binaries/linux/armel/libyeppp-jni.so
