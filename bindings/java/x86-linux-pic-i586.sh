#!/bin/bash
CC=gcc
CFLAGS="-m32 -nostdlib -fPIC -ffunction-sections -Wno-psabi -mtune=corei7 -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -I/usr/lib/jvm/default-java/include -Wa,--noexecstack -c"
CP=cp
CPFLAGS=-r
RM=rm
RMFLAGS="-rf"
MKDIR=mkdir
MKDIRFLAGS=
IMPORT_LIBRARIES="-L../../runtime/binaries/x86-linux-pic-i586/ -L../../library/binaries/x86-linux-pic-i586/ -lyeppp"

$RM $RMFLAGS "binaries/x86-linux-pic-i586"
$MKDIR $MKDIRFLAGS "binaries/x86-linux-pic-i586/"
$MKDIR $MKDIRFLAGS "binaries/x86-linux-pic-i586/library/"
$MKDIR $MKDIRFLAGS "binaries/x86-linux-pic-i586/core/"
$MKDIR $MKDIRFLAGS "binaries/x86-linux-pic-i586/math/"

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/core/Add.o sources-jni/core/Add.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/core/Subtract.o sources-jni/core/Subtract.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/core/Multiply.o sources-jni/core/Multiply.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/core/DotProduct.o sources-jni/core/DotProduct.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/core/SumSquares.o sources-jni/core/SumSquares.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/math/Log.o sources-jni/math/Log.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/math/Exp.o sources-jni/math/Exp.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/math/Sin.o sources-jni/math/Sin.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/math/Cos.o sources-jni/math/Cos.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/math/Tan.o sources-jni/math/Tan.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/library/Init.o sources-jni/library/Init.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/library/Timer.o sources-jni/library/Timer.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/library/Cpu.o sources-jni/library/Cpu.c

$CC -Os $CFLAGS -o binaries/x86-linux-pic-i586/library/String.o sources-jni/library/String.c

$CC -m32 -nostdlib -Wl,-soname,libyeppp-jni.so -shared -Wl,--gc-sections binaries/x86-linux-pic-i586/core/*.o binaries/x86-linux-pic-i586/math/*.o binaries/x86-linux-pic-i586/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/x86-linux-pic-i586/libyeppp-jni.so $IMPORT_LIBRARIES

strip binaries/x86-linux-pic-i586/libyeppp-jni.so
strip -R .comment -R .note.gnu.build-id binaries/x86-linux-pic-i586/libyeppp-jni.so

$CP $CPFLAGS binaries/x86-linux-pic-i586/libyeppp-jni.so ../../binaries/linux/i586/libyeppp-jni.so
