CFLAGS = -Os
CFLAGS += -I../../library/headers
CFLAGS += -Isources-jni
CFLAGS += -nostdlib
CFLAGS += -fPIC
CFLAGS += -ffunction-sections
CFLAGS += -fdata-sections
CFLAGS += -Wno-psabi
CFLAGS += -fno-exceptions
CFLAGS += -fno-unwind-tables
CFLAGS += -fstrict-aliasing
CFLAGS += -funswitch-loops
CFLAGS += -Wa,--noexecstack
LDFLAGS = -L../../library/binaries/$(TARGET)
LDFLAGS += -L../../runtime/binaries/$(TARGET)
ifeq ($(TARGET),x64-linux-sysv-default)
    CFLAGS += -m64
    CFLAGS += -mtune=corei7
    CFLAGS += -fomit-frame-pointer
    CFLAGS += -I/usr/lib/jvm/default-java/include
    LDFLAGS += -m64
    LDFLAGS += -Wl,-rpath,'$$ORIGIN'
    TARGETDIR = linux/x86_64
else ifeq ($(TARGET),x86-linux-pic-i586)
    CFLAGS += -m32
    CFLAGS += -mtune=corei7
    CFLAGS += -fomit-frame-pointer
    CFLAGS += -I/usr/lib/jvm/default-java/include
    LDFLAGS += -m32
    LDFLAGS += -Wl,-rpath,'$$ORIGIN'
    TARGETDIR = linux/i586
else ifeq ($(TARGET),arm-linux-softeabi-v5t)
    CFLAGS += -I/usr/lib/jvm/default-java/include
    LDFLAGS += -Wl,-rpath,'$$ORIGIN'
    TARGETDIR = linux/armel
else ifeq ($(TARGET),arm-linux-hardeabi-v7a)
    CFLAGS += -I/usr/lib/jvm/default-java/include
    LDFLAGS += -Wl,-rpath,'$$ORIGIN'
    TARGETDIR = linux/armhf
else ifeq ($(TARGET),arm-linux-softeabi-android)
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm/usr/include
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm
    TARGETDIR = android/armeabi
else ifeq ($(TARGET),arm-linux-softeabi-androidv7a)
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm/usr/include
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm
    TARGETDIR = android/armeabiv7a
else ifeq ($(TARGET),x86-linux-pic-android)
    CFLAGS += -m32
    CFLAGS += -msse3
    CFLAGS += -mtune=atom
    CFLAGS += -fomit-frame-pointer
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-9/arch-x86/usr/include
    LDFLAGS += -m32
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-9/arch-x86
    TARGETDIR = android/x86
else ifeq ($(TARGET),mips-linux-o32-android)
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-9/arch-mips/usr/include
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-9/arch-mips
    TARGETDIR = android/mips
else
    $(error TARGET variable is not defined or contains unsupported value)
endif
CFLAGS += -c
LDFLAGS += -lyeppp

all : binaries/$(TARGET)/libyeppp-jni.so

binaries/$(TARGET):
	-mkdir -p binaries
	-mkdir -p binaries/$(TARGET)

binaries/$(TARGET)/core: binaries/$(TARGET)
	-rm -rf binaries/$(TARGET)/core
	-mkdir -p binaries/$(TARGET)/core
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/Add.o sources-jni/core/Add.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/Subtract.o sources-jni/core/Subtract.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/Multiply.o sources-jni/core/Multiply.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/Min.o sources-jni/core/Min.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/Max.o sources-jni/core/Max.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/Sum.o sources-jni/core/Sum.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/SumAbs.o sources-jni/core/SumAbs.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/SumSquares.o sources-jni/core/SumSquares.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/core/DotProduct.o sources-jni/core/DotProduct.c

binaries/$(TARGET)/math: binaries/$(TARGET)
	-rm -rf binaries/$(TARGET)/math
	-mkdir -p binaries/$(TARGET)/math
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/math/Log.o sources-jni/math/Log.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/math/Exp.o sources-jni/math/Exp.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/math/Sin.o sources-jni/math/Sin.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/math/Cos.o sources-jni/math/Cos.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/math/Tan.o sources-jni/math/Tan.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/math/EvaluatePolynomial.o sources-jni/math/EvaluatePolynomial.c

binaries/$(TARGET)/library: binaries/$(TARGET)
	-rm -rf binaries/$(TARGET)/library
	-mkdir -p binaries/$(TARGET)/library
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/library/Init.o sources-jni/library/Init.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/library/Timer.o sources-jni/library/Timer.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/library/Cpu.o sources-jni/library/Cpu.c
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/library/String.o sources-jni/library/String.c

binaries/$(TARGET)/libyeppp-jni.so: binaries/$(TARGET)/core binaries/$(TARGET)/math binaries/$(TARGET)/library
	$(CC) -nostdlib -Wl,-soname,libyeppp-jni.so -shared -Wl,--gc-sections -o binaries/$(TARGET)/libyeppp-jni.so binaries/$(TARGET)/core/*.o binaries/$(TARGET)/math/*.o binaries/$(TARGET)/library/*.o -Wl,--no-undefined -Wl,-z,noexecstack $(LDFLAGS)
	-cp binaries/$(TARGET)/libyeppp-jni.so ../../binaries/$(TARGETDIR)/libyeppp-jni.so


clean:
	-rm -rf binaries/$(TARGET)
