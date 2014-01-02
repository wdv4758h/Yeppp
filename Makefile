.PHONY: help clean config-linux-x86 linux-x86 config-linux-x86_64 linux-x86_64 config-linux-k1om linux-k1om config-linux-armel linux-armel config-linux-armhf linux-armhf config-linux-ppc64 linux-ppc64 config-linux-bgq linux-bgq config-android-armeabi android-armeabi config-android-armeabiv7a android-armeabiv7a config-android-x86 android-x86 config-android-mips android-mips config-macosx-x86 macosx-x86 config-macosx-x86_64 macosx-x86_64 config-windows-x86 windows-x86 config-windows-x86_64 windows-x86_64 generate generate-core generate-math

help:
	@echo "Linux targets:"
	@echo "    linux-x86          : build for GNU/Linux on x86 (i586)"
	@echo "    linux-x86_64       : build for GNU/Linux on x86-64"
	@echo "    linux-armel        : build for GNU/Linux on ARM (armel)"
	@echo "    linux-armhf        : build for GNU/Linux on ARM (armhf)"
	@echo "    linux-ppc64        : build for GNU/Linux on PowerPC64"
	@echo "    linux-k1om         : build for Xeon Phi"
	@echo "    linux-bgq          : build for Blue Gene/Q"
	@echo "Android targets:"
	@echo "    android-armeabi    : build for Android ARMEABI ABI"
	@echo "    android-armeabiv7a : build for Android ARMEABI-V7A ABI"
	@echo "    android-x86        : build for Android x86 ABI"
	@echo "    anrdoid-mips       : build for Android MIPS ABI"
	@echo "Mac OS X targets:"
	@echo "    macosx-x86         : build for Mac OS X on x86"
	@echo "    macosx-x86_64      : build for Mac OS X on x86-64"
	@echo "Windows targets:"
	@echo "    windows-x86        : build for Windows on x86"
	@echo "    windows-x86_64     : build for Windows on x86-64"
	@echo "Service targets:"
	@echo "    generate           : generate code for auto-generated modules"
	@echo "    clean              : delete all binaries"

config-linux-x86: build/linux-x86/rules.ninja
config-linux-x86_64: build/linux-x86_64/rules.ninja
config-linux-k1om: build/linux-k1om/rules.ninja
config-linux-armel: build/linux-armel/rules.ninja
config-linux-armhf: build/linux-armhf/rules.ninja
config-linux-ppc64: build/linux-ppc64/rules.ninja
config-linux-bgq: build/linux-bgq/rules.ninja
config-android-armeabi: build/android-armeabi/rules.ninja
config-android-armeabiv7a: build/android-armeabiv7/rules.ninja
config-android-x86: build/android-x86/rules.ninja
config-android-mips: build/android-mips/rules.ninja
config-macosx-x86: build/macosx-x86/rules.ninja
config-macosx-x86_64: build/macosx-x86_64/rules.ninja
config-windows-x86: build/windows-x86/rules.ninja
config-windows-x86_64: build/windows-x86_64/rules.ninja

build/linux-x86/rules.ninja:
	-mkdir -p build/linux-x86
	cd build/linux-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-x86.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/linux-x86_64/rules.ninja:
	-mkdir -p build/linux-x86_64
	cd build/linux-x86_64 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-x86_64.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/linux-k1om/rules.ninja:
	-mkdir -p build/linux-k1om
	cd build/linux-k1om && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-k1om.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/linux-armel/rules.ninja:
	-mkdir -p build/linux-armel
	cd build/linux-armel && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-armel.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/linux-armhf/rules.ninja:
	-mkdir -p build/linux-armhf
	cd build/linux-armhf && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-armhf.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/linux-ppc64/rules.ninja:
	-mkdir -p build/linux-ppc64
	cd build/linux-ppc64 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-ppc64.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/linux-bgq/rules.ninja:
	-mkdir -p build/linux-bgq
	cd build/linux-bgq && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/linux-bgq.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/android-armeabi/rules.ninja:
	-mkdir -p build/android-armeabi
	cd build/android-armeabi && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/android-armeabi.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/android-armeabiv7a/rules.ninja:
	-mkdir -p build/android-armeabiv7a
	cd build/android-armeabiv7a && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/android-armeabiv7a.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/android-x86/rules.ninja:
	-mkdir -p build/android-x86
	cd build/android-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/android-x86.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/android-mips/rules.ninja:
	-mkdir -p build/android-mips
	cd build/android-mips && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/android-mips.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/macosx-x86/rules.ninja:
	-mkdir -p build/macosx-x86
	cd build/macosx-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/macosx-x86.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/macosx-x86_64/rules.ninja:
	-mkdir -p build/macosx-x86_64
	cd build/macosx-x86_64 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/macosx-x86_64.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/cmake -G Ninja ../..

build/windows-x86/rules.ninja:
	-mkdir build
	-mkdir build\windows-x86
	cd build && cd windows-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/windows-x86.toolchain.cmake -G Ninja ../..

build/windows-x86_64/rules.ninja:
	-mkdir build
	-mkdir build\windows-x86_64
	cd build && cd windows-x86_64 && cmake -DCMAKE_TOOLCHAIN_FILE=../../cmake/windows-x86_64.toolchain.cmake -G Ninja ../..

linux-x86: config-linux-x86
	cmake --build build/linux-x86

linux-x86_64: config-linux-x86_64
	cmake --build build/linux-x86_64

linux-k1om: config-linux-k1om
	cmake --build build/linux-k1om

linux-armel: config-linux-armel
	cmake --build build/linux-armel

linux-armhf: config-linux-armhf
	cmake --build build/linux-armhf

linux-ppc64: config-linux-ppc64
	cmake --build build/linux-ppc64

linux-bgq: config-linux-bgq
	cmake --build build/linux-bgq

android-armeabi: config-android-armeabi
	cmake --build build/android-armeabi

android-armeabiv7a: config-android-armeabiv7a
	cmake --build build/android-armeabiv7a

android-x86: config-android-x86
	cmake --build build/android-x86

android-mips: config-android-mips
	cmake --build build/android-mips

macosx-x86: config-macosx-x86
	cmake --build build/macosx-x86

macosx-x86_64: config-macosx-x86_64
	cmake --build build/macosx-x86_64

windows-x86: config-windows-x86
	cmake --build build/windows-x86

windows-x86_64: config-windows-x86_64
	cmake --build build/windows-x86_64

generate: generate-core generate-math

generate-core: codegen/core.py
	python codegen/core.py

generate-math: codegen/math.py
	python codegen/math.py

clean:
	-rm -rf build/linux-x86
	-rm -rf build/linux-x86_64
	-rm -rf build/linux-k1om
	-rm -rf build/linux-armel
	-rm -rf build/linux-armhf
	-rm -rf build/linux-ppc64
	-rm -rf build/linux-bgq
	-rm -rf build/android-armeabi
	-rm -rf build/android-armeabiv7a
	-rm -rf build/android-x86
	-rm -rf build/android-mips
	-rm -rf build/macosx-x86
	-rm -rf build/macosx-x86_64
	-rm -rf build/windows-x86
	-rm -rf build/windows-x86_64
