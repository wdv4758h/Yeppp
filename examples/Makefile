CFLAGS += -O3 -I../library/headers
LDFLAGS += -L../library/binaries/$(TARGET)
ifeq ($(TARGET),x64-linux-sysv-default)
    CFLAGS += -m64
    LDFLAGS += -L../binaries/linux/x86_64
    LDFLAGS += -Wl,-rpath,"$(PWD)/../library/binaries/$(TARGET)"
    LDFLAGS += -Wl,-rpath,"$(PWD)/../binaries/linux/x86_64"
else ifeq ($(TARGET),x64-linux-k1om-default)
    ifeq ($(CC),icc)
        CFLAGS += -mmic
    endif
    LDFLAGS += -L../binaries/linux/k1om
    LDFLAGS += -Wl,-rpath,'$$ORIGIN'
else ifeq ($(TARGET),x86-linux-pic-i586)
    CFLAGS += -m32
    LDFLAGS += -L../binaries/linux/i586
    LDFLAGS += -Wl,-rpath,"$(PWD)/../library/binaries/$(TARGET)"
    LDFLAGS += -Wl,-rpath,"$(PWD)/../binaries/linux/i586"
else ifeq ($(TARGET),arm-linux-softeabi-v5t)
    LDFLAGS += -L../binaries/linux/armel
    LDFLAGS += -Wl,-rpath,"$(PWD)/../library/binaries/$(TARGET)"
    LDFLAGS += -Wl,-rpath,"$(PWD)/../binaries/linux/armel"
else ifeq ($(TARGET),arm-linux-hardeabi-v7a)
    LDFLAGS += -L../binaries/linux/armhf
    LDFLAGS += -Wl,-rpath,"$(PWD)/../library/binaries/$(TARGET)"
    LDFLAGS += -Wl,-rpath,"$(PWD)/../binaries/linux/armhf"
else ifeq ($(TARGET),arm-linux-softeabi-android)
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm/usr/include
    LDFLAGS += -L../binaries/android/armeabi
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm
else ifeq ($(TARGET),arm-linux-softeabi-androidv7a)
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm/usr/include
    LDFLAGS += -L../binaries/android/armeabiv7a
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-3/arch-arm
else ifeq ($(TARGET),x86-linux-pic-android)
    CFLAGS += -m32
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-9/arch-x86/usr/include
    LDFLAGS += -L../binaries/android/x86
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-9/arch-x86
else ifeq ($(TARGET),mips-linux-o32-android)
    CFLAGS += -I$(ANDROID_NDK_ROOT)/platforms/android-9/arch-mips/usr/include
    LDFLAGS += -L../binaries/android/mips
    LDFLAGS += --sysroot=$(ANDROID_NDK_ROOT)/platforms/android-9/arch-mips
else
    $(error TARGET variable is not defined or contains unsupported value)
endif
LDFLAGS += -lyeppp

all : Entropy CpuInfo CpuInfoEx CpuCycles Polynomial PolynomialF SystemTimer EnergyCounter

Entropy : binaries/$(TARGET)/Entropy
CpuInfo : binaries/$(TARGET)/CpuInfo
CpuInfoEx : binaries/$(TARGET)/CpuInfoEx
CpuCycles: binaries/$(TARGET)/CpuCycles
Polynomial : binaries/$(TARGET)/Polynomial
PolynomialF : binaries/$(TARGET)/PolynomialF
SystemTimer: binaries/$(TARGET)/SystemTimer
EnergyCounter: binaries/$(TARGET)/EnergyCounter

binaries/$(TARGET):
	-mkdir -p binaries
	-mkdir -p binaries/$(TARGET)

binaries/$(TARGET)/Entropy: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/Entropy sources/Entropy.c $(LDFLAGS) -lm

binaries/$(TARGET)/CpuInfo: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/CpuInfo sources/CpuInfo.c $(LDFLAGS)

binaries/$(TARGET)/CpuInfoEx: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/CpuInfoEx sources/CpuInfoEx.c $(LDFLAGS)

binaries/$(TARGET)/CpuCycles: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/CpuCycles sources/CpuCycles.c $(LDFLAGS)

binaries/$(TARGET)/Polynomial: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/Polynomial sources/Polynomial.c $(LDFLAGS)

binaries/$(TARGET)/PolynomialF: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/PolynomialF sources/PolynomialF.c $(LDFLAGS)

binaries/$(TARGET)/SystemTimer: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/SystemTimer sources/SystemTimer.c $(LDFLAGS)

binaries/$(TARGET)/EnergyCounter: binaries/$(TARGET)
	$(CC) $(CFLAGS) -o binaries/$(TARGET)/EnergyCounter sources/EnergyCounter.c $(LDFLAGS)

clean:
	-rm -rf binaries/$(TARGET)
