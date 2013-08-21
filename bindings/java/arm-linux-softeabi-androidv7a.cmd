set CC=arm-linux-androideabi-gcc
set CFLAGS=-nostdlib -mthumb -mthumb-interwork -fPIC -ffunction-sections -Wno-psabi -march=armv7-a -mtune=cortex-a9 -mfloat-abi=softfp -mfpu=vfpv3-d16 -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -Wa,--noexecstack -I%ANDROID_NDK_ROOT%/platforms/android-3/arch-arm/usr/include -c
set STRIP=arm-linux-androideabi-strip
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q

set IMPORT_LIBRARIES=-L../../runtime/binaries/arm-linux-softeabi-androidv7a -L../../library/binaries/arm-linux-softeabi-androidv7a -lyeppp -lyeprt

%RM% %RMFLAGS% "binaries/arm-linux-softeabi-androidv7a" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-androidv7a/" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-androidv7a/core" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-androidv7a/library" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-androidv7a/math" >NUL 2>NUL

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/core/Add.o sources-jni/core/Add.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/core/Subtract.o sources-jni/core/Subtract.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/core/Multiply.o sources-jni/core/Multiply.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/core/DotProduct.o sources-jni/core/DotProduct.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/core/SumSquares.o sources-jni/core/SumSquares.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/math/Log.o sources-jni/math/Log.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/math/Exp.o sources-jni/math/Exp.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/math/Sin.o sources-jni/math/Sin.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/math/Cos.o sources-jni/math/Cos.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/math/Tan.o sources-jni/math/Tan.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/library/Init.o sources-jni/library/Init.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/library/Timer.o sources-jni/library/Timer.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/library/Cpu.o sources-jni/library/Cpu.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-androidv7a/library/String.o sources-jni/library/String.c

%CC% -nostdlib -Wl,-soname,libyeppp-jni.so -Wl,--version-script=libyeppp-jni.so.map -shared -Wl,--gc-sections --sysroot=%ANDROID_NDK_ROOT%/platforms/android-9/arch-x86 binaries/arm-linux-softeabi-androidv7a/core/*.o binaries/arm-linux-softeabi-androidv7a/math/*.o binaries/arm-linux-softeabi-androidv7a/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/arm-linux-softeabi-androidv7a/libyeppp-jni.so %IMPORT_LIBRARIES%

%STRIP% binaries/arm-linux-softeabi-androidv7a/libyeppp-jni.so
%STRIP% -R .comment binaries/arm-linux-softeabi-androidv7a/libyeppp-jni.so

%CP% %CPFLAGS% "binaries\arm-linux-softeabi-androidv7a\libyeppp-jni.so" "..\..\binaries\android\armeabi-v7a\libyeppp-jni.so" >NUL 2>NUL
