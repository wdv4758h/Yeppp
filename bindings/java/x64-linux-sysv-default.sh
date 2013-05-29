#!/bin/bash
CC=gcc
CFLAGS="-m64 -nostdlib -fPIC -ffunction-sections -Wno-psabi -mtune=corei7 -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -I/usr/lib/jvm/default-java/include -Wa,--noexecstack -c"
CP=cp
CPFLAGS=-r
RM=rm
RMFLAGS="-rf"
MKDIR=mkdir
MKDIRFLAGS=
IMPORT_LIBRARIES="-L../../runtime/binaries/x64-linux-sysv-default/ -L../../library/binaries/x64-linux-sysv-default/ -lyeppp"

$RM $RMFLAGS "binaries/x64-linux-sysv-default"
$MKDIR $MKDIRFLAGS "binaries/x64-linux-sysv-default/"
$MKDIR $MKDIRFLAGS "binaries/x64-linux-sysv-default/library/"
$MKDIR $MKDIRFLAGS "binaries/x64-linux-sysv-default/core/"
$MKDIR $MKDIRFLAGS "binaries/x64-linux-sysv-default/math/"

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/core/Add.o sources-jni/core/Add.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/core/Subtract.o sources-jni/core/Subtract.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/core/Multiply.o sources-jni/core/Multiply.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/core/DotProduct.o sources-jni/core/DotProduct.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/core/SumSquares.o sources-jni/core/SumSquares.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/math/Log.o sources-jni/math/Log.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/math/Exp.o sources-jni/math/Exp.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/math/Sin.o sources-jni/math/Sin.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/math/Cos.o sources-jni/math/Cos.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/math/Tan.o sources-jni/math/Tan.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/library/Init.o sources-jni/library/Init.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/library/Timer.o sources-jni/library/Timer.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/library/Cpu.o sources-jni/library/Cpu.c

$CC -Os $CFLAGS -o binaries/x64-linux-sysv-default/library/String.o sources-jni/library/String.c

$CC -nostdlib -Wl,-soname,libyeppp-jni.so -shared -Wl,--gc-sections binaries/x64-linux-sysv-default/core/*.o binaries/x64-linux-sysv-default/math/*.o binaries/x64-linux-sysv-default/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/x64-linux-sysv-default/libyeppp-jni.so $IMPORT_LIBRARIES

strip binaries/x64-linux-sysv-default/libyeppp-jni.so
strip -R .comment -R .note.gnu.build-id binaries/x64-linux-sysv-default/libyeppp-jni.so

$CP $CPFLAGS binaries/x64-linux-sysv-default/libyeppp-jni.so ../../binaries/linux/x86_64/libyeppp-jni.so
