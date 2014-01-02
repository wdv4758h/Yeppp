windows-x86:
	-mkdir binaries
	-mkdir binaries\windows-x86
	cd binaries && cd windows-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=../../../cmake/windows-x86.toolchain.cmake -G Ninja ../..
	cmake --build binaries/windows-x86

windows-x86_64:
	-mkdir binaries
	-mkdir binaries\windows-x86_64
	cd binaries && cd windows-x86_64 && cmake -DCMAKE_TOOLCHAIN_FILE=../../../cmake/windows-x86_64.toolchain.cmake -G Ninja ../..
	cmake --build binaries/windows-x86_64

linux-x86_64:
	-mkdir -p binaries/linux-x86_64
	cd binaries/linux-x86_64 && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/linux-x86_64.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/linux-x86_64

linux-x86:
	-mkdir -p binaries/linux-x86
	cd binaries/linux-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/linux-x86.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/linux-x86

linux-armhf:
	-mkdir -p binaries/linux-armhf
	cd binaries/linux-armhf && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/linux-armhf.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/linux-armhf

linux-armel:
	-mkdir -p binaries/linux-armel
	cd binaries/linux-armel && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/linux-armel.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/linux-armel

android-armeabi:
	-mkdir -p binaries/android-armeabi
	cd binaries/android-armeabi && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/android-armeabi.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/android-armeabi

android-armeabiv7a:
	-mkdir -p binaries/android-armeabiv7a
	cd binaries/android-armeabiv7a && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/android-armeabiv7a.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/android-armeabiv7a

android-x86:
	-mkdir -p binaries/android-x86
	cd binaries/android-x86 && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/android-x86.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/android-x86

android-mips:
	-mkdir -p binaries/android-mips
	cd binaries/android-mips && cmake -DCMAKE_TOOLCHAIN_FILE=$(PWD)/../cmake/android-mips.toolchain.cmake -DCMAKE_MODULE_PATH=$(PWD)/../cmake -G Ninja ../..
	cmake --build binaries/android-mips

clean:
	-rm -rf binaries/linux-x86
	-rm -rf binaries/linux-x86_64
	-rm -rf binaries/linux-k1om
	-rm -rf binaries/linux-armel
	-rm -rf binaries/linux-armhf
	-rm -rf binaries/linux-ppc64
	-rm -rf binaries/linux-bgq
	-rm -rf binaries/android-armeabi
	-rm -rf binaries/android-armeabiv7a
	-rm -rf binaries/android-x86
	-rm -rf binaries/android-mips
	-rm -rf binaries/macosx-x86
	-rm -rf binaries/macosx-x86_64
	-rm -rf binaries/windows-x86
	-rm -rf binaries/windows-x86_64
