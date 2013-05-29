set CC=i686-linux-android-gcc
set CFLAGS=-nostdlib -fPIC -ffunction-sections -Wno-psabi -msse3 -mtune=atom -fno-exceptions -fno-unwind-tables -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -Wa,--noexecstack -I%ANDROID_NDK_ROOT%/platforms/android-9/arch-x86/usr/include -c
set STRIP=i686-linux-android-strip
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q

set IMPORT_LIBRARIES=-L../../runtime/binaries/x86-linux-pic-android -L../../library/binaries/x86-linux-pic-android -lyeppp

%RM% %RMFLAGS% "binaries/x86-linux-pic-android" >NUL 2>NUL
mkdir "binaries/x86-linux-pic-android/" >NUL 2>NUL
mkdir "binaries/x86-linux-pic-android/core" >NUL 2>NUL
mkdir "binaries/x86-linux-pic-android/library" >NUL 2>NUL
mkdir "binaries/x86-linux-pic-android/math" >NUL 2>NUL

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/core/Add.o sources-jni/core/Add.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/core/Subtract.o sources-jni/core/Subtract.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/core/Multiply.o sources-jni/core/Multiply.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/core/DotProduct.o sources-jni/core/DotProduct.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/core/SumSquares.o sources-jni/core/SumSquares.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/math/Log.o sources-jni/math/Log.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/math/Exp.o sources-jni/math/Exp.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/math/Sin.o sources-jni/math/Sin.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/math/Cos.o sources-jni/math/Cos.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/math/Tan.o sources-jni/math/Tan.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/library/Init.o sources-jni/library/Init.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/library/Timer.o sources-jni/library/Timer.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/library/Cpu.o sources-jni/library/Cpu.c

%CC% -Os %CFLAGS% -o binaries/x86-linux-pic-android/library/String.o sources-jni/library/String.c

%CC% -nostdlib -Wl,-soname,libyeppp-jni.so -Wl,--version-script=libyeppp-jni.so.map -shared -Wl,--gc-sections --sysroot=%ANDROID_NDK_ROOT%/platforms/android-9/arch-x86 binaries/x86-linux-pic-android/core/*.o binaries/x86-linux-pic-android/math/*.o binaries/x86-linux-pic-android/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/x86-linux-pic-android/libyeppp-jni.so %IMPORT_LIBRARIES%

%STRIP% binaries/x86-linux-pic-android/libyeppp-jni.so
%STRIP% -R .comment binaries/x86-linux-pic-android/libyeppp-jni.so

%CP% %CPFLAGS% "binaries\x86-linux-pic-android\libyeppp-jni.so" "..\..\binaries\android\x86\libyeppp-jni.so" >NUL 2>NUL
