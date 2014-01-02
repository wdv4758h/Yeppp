How to build Yeppp!
=====================

Do you need to build Yeppp?
------------------------------

**For 99% of cases, no!** Yeppp! releases include pre-built binaries for all supported platforms, and for most users we recommend using these pre-built binaries. Unlike most other Unix libraries, Yeppp! maintains binary compatibility with nearly all Linux distributions, so there is no need to rebuild it yourself. Moreover, **BUILDING YEPPP! WITH OUTDATED TOOLCHAIN CAN PRODUCE BINARIES WHICH CRASH ON SOME SYSTEMS, BUT NOT OTHERS** (and by Murphy's law it will crash on all systems but the ones you tested on). This guide is provided for those who want to participate in development of Yeppp! or otherwise modify the library, all others will be better off using pre-built binaries.

Prerequisites
----------

You will need the following tools to build Yeppp!

*   CMake 2.8 or later and [Ninja](http://martine.github.io/ninja/) build system.
*   Python 2.7 to regenerate auto-generated parts of Yeppp! If you use sources from Yeppp! release, you can skip this requirement as Yeppp! releases already include all auto-generated files. 
*   Java Development Kit version 1.6 or later. You can use either Open JDK or Oracle JDK. JDK is required even if you don't plan to develop with Yeppp! in Java.
*   Microsoft Visual Studio 2008, 2010, or 2012 to build Windows binaries.
*   Intel C/C++ Compilers to build Linux/Xeon Phi binaries. We use 13.1.3 version.
*   GNU C/C++ Compilers to build Linux binaries (except Xeon Phi). We use 4.8 version.
*   Clang C/C++ Compilers to build Mac OS X binaries. We use trunk 3.4 version.
*   Android NDK to build Android binaries. Use the latest Android NDK. Also specify the root of Android NDK directory in *ANDROID_NDK_ROOT* environment variable.
*   NASM to build any x86/x86-64 binaries (except Xeon Phi). **Use the trunk version of NASM.** Yeppp! widely uses new CPU instructions, and old (pre-trunk) versions of NASM may have bugs in handling these instructions. **NASM from your Linux repo almost certainly has such bugs.**
*   GNU Binutils to build Linux binaries.
*   Apple utilities (strip and dsymutil) to build Mac OS X binaries.
*   Apache Ant to build Java bindings.
*   MSBuild (part of Visual Studio) and [InjectModuleInitializer.exe](http://einaregilsson.com/module-initializers-in-csharp/) to build CLR bindings.
*   Doxygen to build documentation.
*   WiX Toolkit to build MSI installer for Windows.
   
Generating auto-generated parts
-------------------------------

**This step is needed only if you use sources from a Yeppp! repository.** Yeppp! release distributions already include auto-generated files.

Install [Peach-Py](https://bitbucket.org/MDukhan/peachpy) from Python Package Index (run this command as Administrator/root):
```
pip install PeachPy
```

Change directory to Yeppp! root and run `make generate-core` to generate yepCore module. This will generate the files:

*    library/headers/yepCore.h
*    library/sources/core/*
*    bindings/java/sources-jni/core/*.c
*    bindings/java/sources-java/info/yeppp/Core.java
*    bindings/clr/sources-csharp/core/*.cs
*    bindings/fortran/sources/yepCore.f90
*    unit-tests/sources/core/*.cpp

Similarly generate yepMath module by executing `make generate-math`. There is also `generate` target to generate both modules.

Building the runtime library
----------------------------

In order to maintain high degree of binary compatibility across target platforms, Yeppp! uses its own runtime library (in part based on compiler-rt from Clang project).

Open the command prompt or terminal and navigate to *runtime* directory in Yeppp! tree. To build the runtime library, run
```
make <platform>
```
where platform can be:

*    **windows-x86** to build runtime library for Windows/x86
*    **windows-x86_64** to build runtime library for Windows/x86-64
*    **linux-x86** to build runtime library for Linux/x86
*    **linux-x86_64** to build runtime library for Linux/x86-64
*    **linux-k1om** to build runtime library for Linux/k1om (Xeon Phi)
*    **linux-armel** to build runtime library for Linux/armel
*    **linux-armhf** to build runtime library for Linux/armhf
*    **android-x86** to build runtime library for Android/x86 (x86 ABI)
*    **android-armeabi** to build runtime library for Android/ARM (ARMEABI ABI)
*    **android-armeabiv7a** to build runtime library for Android/ARM (ARMEABI-V7A ABI)
*    **android-mips** to build runtime library for Android/MIPS (MIPS ABI)

On Mac OS X Yeppp! uses the default runtime library, so nothing needs to be built.

Building Yeppp!
---------------

To build Yeppp! navigate to the root of Yeppp! tree and execute
```
make <platform>
```
where platform is

*    **windows-x86** to build Yeppp! for Windows/x86
*    **windows-x86_64** to build runtime library for Windows/x86-64
*    **macosx-x86** to build Yeppp! for Mac OS X/x86
*    **macosx-x86_64** to build Yeppp! for Mac OS X/x86-64
*    **linux-x86** to build Yeppp! for Linux/x86
*    **linux-x86_64** to build Yeppp! for Linux/x86-64
*    **linux-k1om** to build Yeppp! for Linux/k1om (Xeon Phi)
*    **linux-armel** to build Yeppp! for Linux/armel
*    **linux-armhf** to build Yeppp! for Linux/armhf
*    **linux-ppc64** to build Yeppp! for Linux/ppc64
*    **linux-bgq** to build Yeppp! for Blue Gene/Q
*    **android-x86** to build Yeppp! for Android (x86 ABI)
*    **android-armeabi** to build Yeppp! for Android (ARMEABI ABI)
*    **android-armeabiv7a** to build Yeppp! for Android (ARMEABI-V7A ABI)
*    **android-mips** to build Yeppp! for Android (MIPS ABI)

The build system will put the compiled binaries into *binaries* directory in Yeppp! tree.

Buliding Java Bindings
----------------------

Java bindings consist of two parts: glue functions in C which implement the JNI interface and Java classes which describe the functionality implemented by native library. The C functions are compiled as a part of Yeppp! and linked into the library binary. The Java classes need to be build separately.

Open a terminal or Command Prompt, navigate to *bindings/java* directory in Yeppp! and run
```
ant package
```

Ant will put the compiled JARs into *binaries/java-1.5* directory in Yeppp! tree.

Building CLR Bindings
---------------------

To build CLR bindings open the Visual Studio Command Prompt, navigate to directory *bindings/clr* in Yeppp! tree and run
```
msbuild /t:Package
```

MSBuild will put the compiled platform-independent managed DLL into *binaries/clr-2.0* directory in Yeppp! tree.

Building the documentation
--------------------------

Yeppp! uses Doxygen for auto-documenting the library from comments in the code.
You will find Doxyfile files at the following paths:

*    *library/sources/Doxyfile* for C/C++ documentation
*    *bindings/java/Doxyfile* for Java documentation
*    *bindings/clr/Doxyfile* for C# documentation
*    *bindings/fortran/Doxyfile* for FORTRAN documentation

To build the documentation navigate to the directories with about Doxyfile files and run `doxygen`.

The documentation will be generated in the *docs* directory in Yeppp! tree.

Building the MSI installer
--------------------------

To make an MSI installer for Yeppp! SDK, open Visual Studio Command Prompt, navigate to root Yeppp! directory and execute `SetVars.bat`. Then switch to directory *installer/windows* in Yeppp! tree, and run
```
nmake /A
```.

The generated MSI installer will be placed in *installer/windows* directory in the Yeppp! tree.
