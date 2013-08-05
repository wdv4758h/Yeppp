override CFLAGS += -O3
ifeq (${YEPPLATFORM},x64-linux-sysv-default)
    override CFLAGS += -m64
else ifeq (${YEPPLATFORM},x64-macosx-sysv-default)
    override CFLAGS += -m64
else ifeq (${YEPPLATFORM},x64-linux-k1om-default)
    ifeq ($(CC),icc)
        override CFLAGS += -mmic
    endif
    override LDFLAGS += -Wl,-rpath,'$$ORIGIN'
else ifeq (${YEPPLATFORM},x86-linux-pic-i586)
    override CFLAGS += -m32
else ifeq (${YEPPLATFORM},x86-macosx-pic-default)
    override CFLAGS += -m32
else ifeq (${YEPPLATFORM},arm-linux-softeabi-v5t)
    
else ifeq (${YEPPLATFORM},arm-linux-hardeabi-v7a)
    
else ifeq (${YEPPLATFORM},arm-linux-softeabi-android)
    override CFLAGS += -I${ANDROID_NDK_ROOT}/platforms/android-3/arch-arm/usr/include
    override CFLAGS += -I${YEPROOT}/library/headers
    override LDFLAGS += -L"${YEPROOT}/binaries/android/armeabi"
    override LDFLAGS += --sysroot=${ANDROID_NDK_ROOT}/platforms/android-3/arch-arm
else ifeq (${YEPPLATFORM},arm-linux-softeabi-androidv7a)
    override CFLAGS += -I${ANDROID_NDK_ROOT}/platforms/android-3/arch-arm/usr/include
    override CFLAGS += -I${YEPROOT}/library/headers
    override LDFLAGS += -L"${YEPROOT}/binaries/android/armeabiv7a"
    override LDFLAGS += --sysroot=${ANDROID_NDK_ROOT}/platforms/android-3/arch-arm
else ifeq (${YEPPLATFORM},x86-linux-pic-android)
    override CFLAGS += -m32
    override CFLAGS += -I${ANDROID_NDK_ROOT}/platforms/android-9/arch-x86/usr/include
    override CFLAGS += -I${YEPROOT}/library/headers
    override LDFLAGS += -L"${YEPROOT}/binaries/android/x86"
    override LDFLAGS += --sysroot=${ANDROID_NDK_ROOT}/platforms/android-9/arch-x86
else ifeq (${YEPPLATFORM},mips-linux-o32-android)
    override CFLAGS += -I${ANDROID_NDK_ROOT}/platforms/android-9/arch-mips/usr/include
    override CFLAGS += -I${YEPROOT}/library/headers
    override LDFLAGS += -L"${YEPROOT}/binaries/android/mips"
    override LDFLAGS += --sysroot=${ANDROID_NDK_ROOT}/platforms/android-9/arch-mips
else
    $(error YEPPLATFORM variable is not defined or contains unsupported value)
endif
override LDFLAGS += -lyeppp

all : Entropy CpuInfo CpuInfoEx CpuCycles Polynomial PolynomialF SystemTimer EnergyCounter

Entropy : binaries/${YEPPLATFORM}/Entropy
CpuInfo : binaries/${YEPPLATFORM}/CpuInfo
CpuInfoEx : binaries/${YEPPLATFORM}/CpuInfoEx
CpuCycles: binaries/${YEPPLATFORM}/CpuCycles
Polynomial : binaries/${YEPPLATFORM}/Polynomial
PolynomialF : binaries/${YEPPLATFORM}/PolynomialF
SystemTimer: binaries/${YEPPLATFORM}/SystemTimer
EnergyCounter: binaries/${YEPPLATFORM}/EnergyCounter

binaries/${YEPPLATFORM}:
	-mkdir -p binaries
	-mkdir -p binaries/${YEPPLATFORM}

binaries/${YEPPLATFORM}/Entropy: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/Entropy sources/Entropy.c $(LDFLAGS) -lm

binaries/${YEPPLATFORM}/CpuInfo: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/CpuInfo sources/CpuInfo.c $(LDFLAGS)

binaries/${YEPPLATFORM}/CpuInfoEx: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/CpuInfoEx sources/CpuInfoEx.c $(LDFLAGS)

binaries/${YEPPLATFORM}/CpuCycles: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/CpuCycles sources/CpuCycles.c $(LDFLAGS)

binaries/${YEPPLATFORM}/Polynomial: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/Polynomial sources/Polynomial.c $(LDFLAGS)

binaries/${YEPPLATFORM}/PolynomialF: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/PolynomialF sources/PolynomialF.c $(LDFLAGS)

binaries/${YEPPLATFORM}/SystemTimer: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/SystemTimer sources/SystemTimer.c $(LDFLAGS)

binaries/${YEPPLATFORM}/EnergyCounter: binaries/${YEPPLATFORM}
	$(CC) $(CFLAGS) -o binaries/${YEPPLATFORM}/EnergyCounter sources/EnergyCounter.c $(LDFLAGS)

clean:
	-rm -rf binaries/${YEPPLATFORM}
