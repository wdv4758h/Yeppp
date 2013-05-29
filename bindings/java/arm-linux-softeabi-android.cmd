set CC=arm-linux-androideabi-gcc
set CFLAGS=-nostdlib -mthumb -mthumb-interwork -fPIC -ffunction-sections -Wno-psabi -march=armv5te -mtune=arm1136j-s -mfloat-abi=soft -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -Wa,--noexecstack -I%ANDROID_NDK_ROOT%/platforms/android-3/arch-arm/usr/include -c
set STRIP=arm-linux-androideabi-strip
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q

set IMPORT_LIBRARIES=-L../../runtime/binaries/arm-linux-softeabi-android -L../../library/binaries/arm-linux-softeabi-android -lyeppp -lyeprt

%RM% %RMFLAGS% "binaries/arm-linux-softeabi-android" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-android/" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-android/core" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-android/library" >NUL 2>NUL
mkdir "binaries/arm-linux-softeabi-android/math" >NUL 2>NUL

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/core/Add.o sources-jni/core/Add.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/core/Subtract.o sources-jni/core/Subtract.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/core/Multiply.o sources-jni/core/Multiply.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/core/DotProduct.o sources-jni/core/DotProduct.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/core/SumSquares.o sources-jni/core/SumSquares.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/math/Log.o sources-jni/math/Log.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/math/Exp.o sources-jni/math/Exp.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/math/Sin.o sources-jni/math/Sin.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/math/Cos.o sources-jni/math/Cos.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/math/Tan.o sources-jni/math/Tan.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/library/Init.o sources-jni/library/Init.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/library/Timer.o sources-jni/library/Timer.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/library/Cpu.o sources-jni/library/Cpu.c

%CC% -Os %CFLAGS% -o binaries/arm-linux-softeabi-android/library/String.o sources-jni/library/String.c

%CC% -nostdlib -Wl,-soname,libyeppp-jni.so -Wl,--version-script=libyeppp-jni.so.map -shared -Wl,--gc-sections --sysroot=%ANDROID_NDK_ROOT%/platforms/android-9/arch-x86 binaries/arm-linux-softeabi-android/core/*.o binaries/arm-linux-softeabi-android/math/*.o binaries/arm-linux-softeabi-android/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/arm-linux-softeabi-android/libyeppp-jni.so %IMPORT_LIBRARIES%

%STRIP% binaries/arm-linux-softeabi-android/libyeppp-jni.so
%STRIP% -R .comment binaries/arm-linux-softeabi-android/libyeppp-jni.so

%CP% %CPFLAGS% "binaries\arm-linux-softeabi-android\libyeppp-jni.so" "..\..\binaries\android\armeabi\libyeppp-jni.so" >NUL 2>NUL
