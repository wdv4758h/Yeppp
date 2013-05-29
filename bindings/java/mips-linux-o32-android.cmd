set CC=mipsel-linux-android-gcc
set CFLAGS=-nostdlib -march=mips32 -fPIC -ffunction-sections -Wno-psabi -fno-exceptions -fno-unwind-tables -fno-inline-functions-called-once -fgcse-after-reload -frerun-cse-after-loop -frename-registers -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -I../../library/headers -Isources-jni -Wa,--noexecstack -I%ANDROID_NDK_ROOT%/platforms/android-3/arch-arm/usr/include -c
set STRIP=mipsel-linux-android-strip
set CP=copy
set CPFLAGS=/Y
set RM=del
set RMFLAGS=/f /s /q

set IMPORT_LIBRARIES=-L../../runtime/binaries/mips-linux-o32-android -L../../library/binaries/mips-linux-o32-android -lyeppp -lyeprt

%RM% %RMFLAGS% "binaries/mips-linux-o32-android" >NUL 2>NUL
mkdir "binaries/mips-linux-o32-android/" >NUL 2>NUL
mkdir "binaries/mips-linux-o32-android/core" >NUL 2>NUL
mkdir "binaries/mips-linux-o32-android/library" >NUL 2>NUL
mkdir "binaries/mips-linux-o32-android/math" >NUL 2>NUL

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/core/Add.o sources-jni/core/Add.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/core/Subtract.o sources-jni/core/Subtract.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/core/Multiply.o sources-jni/core/Multiply.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/core/DotProduct.o sources-jni/core/DotProduct.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/core/SumSquares.o sources-jni/core/SumSquares.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/math/Log.o sources-jni/math/Log.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/math/Exp.o sources-jni/math/Exp.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/math/Sin.o sources-jni/math/Sin.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/math/Cos.o sources-jni/math/Cos.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/math/Tan.o sources-jni/math/Tan.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/library/Init.o sources-jni/library/Init.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/library/Timer.o sources-jni/library/Timer.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/library/Cpu.o sources-jni/library/Cpu.c

%CC% -Os %CFLAGS% -o binaries/mips-linux-o32-android/library/String.o sources-jni/library/String.c

%CC% -nostdlib -Wl,-soname,libyeppp-jni.so -Wl,--version-script=libyeppp-jni.so.map -shared -Wl,--gc-sections --sysroot=%ANDROID_NDK_ROOT%/platforms/android-9/arch-mips binaries/mips-linux-o32-android/core/*.o binaries/mips-linux-o32-android/math/*.o binaries/mips-linux-o32-android/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack -o binaries/mips-linux-o32-android/libyeppp-jni.so %IMPORT_LIBRARIES%

%STRIP% binaries/mips-linux-o32-android/libyeppp-jni.so
%STRIP% -R .comment binaries/mips-linux-o32-android/libyeppp-jni.so

%CP% %CPFLAGS% "binaries\mips-linux-o32-android\libyeppp-jni.so" "..\..\binaries\android\mips\libyeppp-jni.so" >NUL 2>NUL
