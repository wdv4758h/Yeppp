/*
 *                      Yeppp! library build framework
 *
 * This file is part of Yeppp! library infrastructure and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

import info.yeppp.ebuilda.*;
import info.yeppp.ebuilda.filesystem.*;
import info.yeppp.ebuilda.AndroidNDK;
import info.yeppp.ebuilda.AndroidToolchain;
import info.yeppp.ebuilda.WindowsSDK;
import info.yeppp.ebuilda.generic.Assembler;
import info.yeppp.ebuilda.generic.CCompiler;
import info.yeppp.ebuilda.generic.CppCompiler;
import info.yeppp.ebuilda.generic.Linker;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Pattern;

public class CLIBuild {

	public static void main(String[] args) throws Exception {
		final AbsoluteDirectoryPath yepppRoot = Machine.getLocal().getWorkingDirectory();

		for (final String abiName : args) {
			final ABI abi = ABI.parse(abiName);
			final Toolchain toolchain = getToolchain(abi);
			setup(toolchain.cppCompiler, toolchain.cCompiler, toolchain.assembler, toolchain.linker, toolchain.javaSDK, toolchain.microsoftResourceCompiler, toolchain.gnuStrip, toolchain.gnuObjCopy, toolchain.appleStrip, toolchain.appleDSymUtil, yepppRoot);
			build(toolchain.cppCompiler, toolchain.cCompiler, toolchain.assembler, toolchain.linker, toolchain.microsoftResourceCompiler, toolchain.gnuStrip, toolchain.gnuObjCopy, toolchain.appleStrip, toolchain.appleDSymUtil, yepppRoot);
		}
	}

	static class Toolchain {
		public Toolchain(CppCompiler cppCompiler, CCompiler cCompiler, Assembler assembler, Linker linker, JavaSDK javaSDK) {
			this.cppCompiler = cppCompiler;
			this.cCompiler = cCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.javaSDK = javaSDK;
			this.microsoftResourceCompiler = null;
			this.gnuStrip = null;
			this.gnuObjCopy = null;
			this.appleStrip = null;
			this.appleDSymUtil = null;
		}

		public Toolchain(CppCompiler cppCompiler, CCompiler cCompiler, Assembler assembler, Linker linker, JavaSDK javaSDK, MicrosoftResourceCompiler microsoftResourceCompiler) {
			this.cppCompiler = cppCompiler;
			this.cCompiler = cCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.javaSDK = javaSDK;
			this.microsoftResourceCompiler = microsoftResourceCompiler;
			this.gnuStrip = null;
			this.gnuObjCopy = null;
			this.appleStrip = null;
			this.appleDSymUtil = null;
		}

		public Toolchain(CppCompiler cppCompiler, CCompiler cCompiler, Assembler assembler, Linker linker, JavaSDK javaSDK, GnuStrip gnuStrip, GnuObjCopy gnuObjCopy) {
			this.cppCompiler = cppCompiler;
			this.cCompiler = cCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.javaSDK = javaSDK;
			this.microsoftResourceCompiler = null;
			this.gnuStrip = gnuStrip;
			this.gnuObjCopy = gnuObjCopy;
			this.appleStrip = null;
			this.appleDSymUtil = null;
		}

		public Toolchain(CppCompiler cppCompiler, CCompiler cCompiler, Assembler assembler, Linker linker, JavaSDK javaSDK, AppleStrip appleStrip, AppleDSymUtil appleDSymUtil) {
			this.cppCompiler = cppCompiler;
			this.cCompiler = cCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.javaSDK = javaSDK;
			this.microsoftResourceCompiler = null;
			this.gnuStrip = null;
			this.gnuObjCopy = null;
			this.appleStrip = appleStrip;
			this.appleDSymUtil = appleDSymUtil;
		}

		final CppCompiler cppCompiler;
		final CCompiler cCompiler;
		final Assembler assembler;
		final Linker linker;
		final MicrosoftResourceCompiler microsoftResourceCompiler;
		final GnuStrip gnuStrip;
		final GnuObjCopy gnuObjCopy;
		final AppleStrip appleStrip;
		final AppleDSymUtil appleDSymUtil;
		final JavaSDK javaSDK;
	}

	public static void setup(CppCompiler cppCompiler, CCompiler cCompiler, Assembler assembler, Linker linker, JavaSDK javaSDK, MicrosoftResourceCompiler microsoftResourceCompiler, GnuStrip gnuStrip, GnuObjCopy gnuObjCopy, AppleStrip appleStrip, AppleDSymUtil appleDSymUtil, AbsoluteDirectoryPath yepppRoot) {
		final ABI abi = cppCompiler.getABI();

		final AbsoluteDirectoryPath librarySourceDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/sources"));
		final AbsoluteDirectoryPath libraryHeaderDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/headers"));
		final AbsoluteDirectoryPath libraryObjectDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/binaries/" + abi.toString()));
		final AbsoluteDirectoryPath jniSourceDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("bindings/java/sources-jni"));
		final AbsoluteDirectoryPath jniObjectDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("bindings/java/binaries/" + abi.toString()));
		final AbsoluteDirectoryPath runtimeBinariesDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("runtime/binaries/" + abi.toString()));

		cppCompiler.setSourceDirectory(librarySourceDirectory);
		cppCompiler.setObjectDirectory(libraryObjectDirectory);
		cppCompiler.addDefaultGlobalIncludeDirectories();
		cppCompiler.setVerboseBuild(true);
		cppCompiler.addMacro("YEP_BUILD_LIBRARY");
		cppCompiler.setPositionIndependentCodeGeneration(PositionIndependentCodeGeneration.UnlimitedLibraryPIC);
		cppCompiler.setRttiEnabled(false);
		cppCompiler.setExceptionsSupport(CppCompiler.Exceptions.NoExceptions);
		if (abi.getOperatingSystem().equals(OperatingSystem.MacOSX)) {
			cppCompiler.setRuntimeLibrary(CCompiler.RuntimeLibrary.DynamicRuntimeLibrary);
		} else {
			cppCompiler.setRuntimeLibrary(CCompiler.RuntimeLibrary.NoRuntimeLibrary);
		}
		cppCompiler.setOptimization(CCompiler.Optimization.MaxSpeedOptimization);
		cppCompiler.addIncludeDirectory(librarySourceDirectory);
		cppCompiler.addIncludeDirectory(libraryHeaderDirectory);

		cCompiler.setSourceDirectory(jniSourceDirectory);
		cCompiler.setObjectDirectory(jniObjectDirectory);
		cCompiler.addDefaultGlobalIncludeDirectories();
		cCompiler.setVerboseBuild(true);
		cCompiler.addMacro("YEP_BUILD_LIBRARY");
		cCompiler.setPositionIndependentCodeGeneration(PositionIndependentCodeGeneration.UnlimitedLibraryPIC);
		if (abi.getOperatingSystem().equals(OperatingSystem.MacOSX)) {
			cCompiler.setRuntimeLibrary(CCompiler.RuntimeLibrary.DynamicRuntimeLibrary);
		} else {
			cCompiler.setRuntimeLibrary(CCompiler.RuntimeLibrary.NoRuntimeLibrary);
		}
		cCompiler.setOptimization(CCompiler.Optimization.MinSizeOptimization);
		cCompiler.addIncludeDirectory(jniSourceDirectory);
		cCompiler.addIncludeDirectory(libraryHeaderDirectory);
		if (javaSDK != null) {
			cCompiler.addGlobalIncludeDirectories(javaSDK.getIncludeDirectories());
		}

		if (microsoftResourceCompiler != null) {
			microsoftResourceCompiler.setSourceDirectory(librarySourceDirectory);
			microsoftResourceCompiler.setObjectDirectory(libraryObjectDirectory);
			microsoftResourceCompiler.addDefaultGlobalIncludeDirectories();
			microsoftResourceCompiler.setVerboseBuild(true);
			microsoftResourceCompiler.addIncludeDirectory(librarySourceDirectory);
			microsoftResourceCompiler.addIncludeDirectory(new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/headers")));
		}

		if (assembler != null) {
			assembler.setSourceDirectory(librarySourceDirectory);
			assembler.setObjectDirectory(libraryObjectDirectory);
			assembler.setVerboseBuild(true);
			if (assembler instanceof NASM) {
				final NASM nasm = (NASM)assembler;
				nasm.setOptimization(NASM.Optimization.Multipass);
			}
		}

		if (gnuObjCopy != null) {
			gnuObjCopy.setVerboseBuild(true);
		}

		if (gnuStrip != null) {
			gnuStrip.setVerboseBuild(true);
		}

		if (appleDSymUtil != null) {
			appleDSymUtil.setVerboseBuild(true);
		}

		if (appleStrip != null) {
			appleStrip.setVerboseBuild(true);
		}

		linker.setObjectDirectory(libraryObjectDirectory);
		linker.setBinariesDirectory(libraryObjectDirectory);
		linker.addDefaultGlobalLibraryDirectories();
		if (!abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			linker.setPIC(PositionIndependentCodeGeneration.UnlimitedLibraryPIC);
		}
		linker.setVerboseBuild(true);
		linker.setRuntimeLibraryUse(false);
		if (!abi.getOperatingSystem().equals(OperatingSystem.MacOSX)) {
			linker.addLibraryDirectory(runtimeBinariesDirectory);
		}
		if (abi.getOperatingSystem().equals(OperatingSystem.MacOSX)) {
			linker.addDynamicLibraryDependence("c");
		} else {
			linker.addStaticLibraryDependence("yeprt");
		}
		if (abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			linker.addDynamicLibraryDependence("kernel32");
		}
	}

	public static Pattern getAssemblyPattern(ABI abi) {
		switch (abi) {
			case X86_Linux_Pic_Android:
			case X86_Linux_Pic_i586:
			case X86_MacOSX_Pic_Default:
				return Pattern.compile(".+\\.x86\\-pic\\.asm");
			case X86_Windows_Default_i586:
				return Pattern.compile(".+\\.x86\\-nonpic\\.asm");
			case X64_Windows_Microsoft_Default:
				return Pattern.compile(".+\\.x64\\-ms\\.asm");
			case X64_Linux_SystemV_Default:
			case X64_MacOSX_SystemV_Default:
				return Pattern.compile(".+\\.x64\\-sysv\\.asm");
			case X64_Linux_KNC_Default:
				return Pattern.compile(".+\\.x64\\-k1om\\.asm");
			case ARM_Linux_SoftEABI_V5T:
			case ARM_Linux_SoftEABI_Android:
			case ARM_Linux_SoftEABI_AndroidV7A:
				return Pattern.compile(".+\\.arm(?:\\-softeabi)?\\.asm");
			case ARM_Linux_HardEABI_V7A:
				return Pattern.compile(".+\\.arm(?:\\-hardeabi)?\\.asm");
			case MIPS_Linux_O32_Android:
				return Pattern.compile(".+\\.mips\\.asm");
			default:
				throw new Error(String.format("Unknown ABI %s", abi.toString()));
		}
	}

	public static void build(CppCompiler cppCompiler, CCompiler cCompiler, Assembler assembler, Linker linker, MicrosoftResourceCompiler microsoftResourceCompiler, GnuStrip gnuStrip, GnuObjCopy gnuObjCopy, AppleStrip appleStrip, AppleDSymUtil appleDSymUtil, AbsoluteDirectoryPath yepppRoot) throws IOException {
		final ABI abi = cppCompiler.getABI();
		final Architecture architecture = abi.getArchitecture();
		final OperatingSystem operatingSystem = abi.getOperatingSystem();
		final AbsoluteFilePath libraryBinaryPath = new AbsoluteFilePath(linker.getBinariesDirectory(), new RelativeFilePath("yeppp"));
		final BuildMessages buildMessages = new BuildMessages();
		final List<AbsoluteFilePath> cppSources = cppCompiler.getSourceDirectory().getFiles(Pattern.compile(".+\\.cpp"), true);
		final List<AbsoluteFilePath> cSources = cCompiler.getSourceDirectory().getFiles(Pattern.compile(".+\\.c"), true);
		final List<AbsoluteFilePath> rcSources = cppCompiler.getSourceDirectory().getFiles(Pattern.compile(".+\\.rc"), true);
		final List<AbsoluteFilePath> asmSources = assembler.getSourceDirectory().getFiles(getAssemblyPattern(abi), true);
		final List<AbsoluteFilePath> objects = new ArrayList<AbsoluteFilePath>(cppSources.size());
		for (final AbsoluteFilePath source : cppSources) {
			final String sourcePath = source.getRelativePath(cppCompiler.getSourceDirectory()).toString();
			if (sourcePath.equals("library/CpuX86.cpp") && !(architecture.equals(Architecture.X86) || architecture.equals(Architecture.X64))) {
				continue;
			}
			if (sourcePath.equals("library/CpuArm.cpp") && !architecture.equals(Architecture.ARM)) {
				continue;
			}
			if (sourcePath.equals("library/CpuMips.cpp") && !architecture.equals(Architecture.MIPS)) {
				continue;
			}
			if (sourcePath.equals("library/CpuWindows.cpp") && !operatingSystem.equals(OperatingSystem.Windows)) {
				continue;
			}
			if (sourcePath.equals("library/CpuLinux.cpp") && !operatingSystem.equals(OperatingSystem.Linux)) {
				continue;
			}
			if (sourcePath.equals("library/CpuMacOSX.cpp") && !operatingSystem.equals(OperatingSystem.MacOSX)) {
				continue;

			}
			if (sourcePath.equals("library/Unsafe.cpp") && !operatingSystem.equals(OperatingSystem.Linux)) {
				continue;
			}
			buildMessages.add(cppCompiler.compile(source));
			objects.add(cppCompiler.getObjectPath(source));
		}
		if (abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			for (final AbsoluteFilePath source : rcSources) {
				buildMessages.add(microsoftResourceCompiler.compile(source));
				objects.add(microsoftResourceCompiler.getObjectPath(source));
			}
		}
		for (final AbsoluteFilePath source : asmSources) {
			buildMessages.add(assembler.assemble(source));
			objects.add(assembler.getObjectPath(source));
		}
		if (!abi.equals(ABI.X64_Linux_KNC_Default)) {
			for (final AbsoluteFilePath source : cSources) {
				buildMessages.add(cCompiler.compile(source));
				objects.add(cCompiler.getObjectPath(source));
			}
		}
		buildMessages.add(linker.linkDynamicLibrary(libraryBinaryPath, objects));
		if (abi.getOperatingSystem().equals(OperatingSystem.Linux)) {
			final RelativeFilePath libraryBinary = new RelativeFilePath("libyeppp.so");
			final RelativeFilePath debugBinary = new RelativeFilePath("libyeppp.dbg");
			try {
				getBinariesDirectory(yepppRoot, abi).create();
				buildMessages.add(gnuStrip.extractDebugInformation(
						new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary),
						new AbsoluteFilePath(linker.getBinariesDirectory(), debugBinary)));
				buildMessages.add(gnuStrip.strip(new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary)));
				buildMessages.add(gnuObjCopy.addGnuDebugLink(
						new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary),
						new AbsoluteFilePath(linker.getBinariesDirectory(), debugBinary)));
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), libraryBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary));
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), debugBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), debugBinary));
			} catch (IOException e) {
			}
		} else if (abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			final RelativeFilePath libraryBinary = new RelativeFilePath("yeppp.dll");
			final RelativeFilePath importBinary = new RelativeFilePath("yeppp.lib");
			final RelativeFilePath debugBinary = new RelativeFilePath("yeppp.pdb");
			try {
				getBinariesDirectory(yepppRoot, abi).create();
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), libraryBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary));
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), importBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), importBinary));
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), debugBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), debugBinary));
			} catch (IOException e) {
			}
		} else if (abi.getOperatingSystem().equals(OperatingSystem.MacOSX)) {
			final RelativeFilePath libraryBinary = new RelativeFilePath("libyeppp.dylib");
			final RelativeFilePath debugBinary = new RelativeFilePath("libyeppp.dylib.dSYM");
			try {
				getBinariesDirectory(yepppRoot, abi).create();
				buildMessages.add(appleDSymUtil.extractDebugInformation(
						new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary),
						new AbsoluteFilePath(linker.getBinariesDirectory(), debugBinary)));
				buildMessages.add(appleStrip.stripLocalSymbols(new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary)));
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), libraryBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary));
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), debugBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), debugBinary));
			} catch (IOException e) {
			}
		}
		for (BuildMessage buildMessage : buildMessages.iterable()) {
			System.out.println(buildMessage.toString());
		}
	}

	public static AbsoluteDirectoryPath getBinariesDirectory(AbsoluteDirectoryPath rootDirectory, ABI abi) {
		switch (abi) {
			case X86_Linux_Pic_i586:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/linux/i586"));
			case X64_Linux_SystemV_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/linux/x86_64"));
			case X64_Linux_KNC_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/linux/k1om"));
			case ARM_Linux_OABI_V4T:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/linux/arm"));
			case ARM_Linux_SoftEABI_V5T:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/linux/armel"));
			case ARM_Linux_HardEABI_V7A:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/linux/armhf"));
			case X86_Windows_Default_i586:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/windows/x86"));
			case X64_Windows_Microsoft_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/windows/amd64"));
			case IA64_Windows_Microsoft_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/windows/ia64"));
			case ARM_Linux_SoftEABI_Android:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/android/armeabi"));
			case ARM_Linux_SoftEABI_AndroidV7A:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/android/armeabi-v7a"));
			case X86_Linux_Pic_Android:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/android/x86"));
			case MIPS_Linux_O32_Android:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/android/mips"));
			case X86_MacOSX_Pic_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/macosx/x86"));
			case X64_MacOSX_SystemV_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/macosx/x86_64"));
			case X86_NaCl_NaCl_i686:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/nacl/x86"));
			case X64_NaCl_NaCl_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/nacl/x86_64"));
			case ARM_NaCl_NaCl_Default:
				return new AbsoluteDirectoryPath(rootDirectory, new RelativeDirectoryPath("binaries/nacl/arm"));
			default:
				throw new Error(String.format("Unknown ABI %s", abi));
		}
	}

	public static Toolchain getToolchain(ABI abi) {
		switch (abi) {
			case X64_Windows_Microsoft_Default:
			case X86_Windows_Default_i586:
			{
				final VisualStudio visualStudio = VisualStudio.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), abi).getNewest();
				final MicrosoftResourceCompiler resourceCompiler = visualStudio.getWindowsSDK().getResourceCompiler();
				final JavaSDK javaSDK = JavaSDK.enumerate(Machine.getLocal()).getNewest();
				return new Toolchain(visualStudio.getCppCompiler(), visualStudio.getCCompiler(), nasm, visualStudio.getLinker(), javaSDK, resourceCompiler);
			}
			case ARM_Linux_SoftEABI_Android:
			case ARM_Linux_SoftEABI_AndroidV7A:
			case X86_Linux_Pic_Android:
			case MIPS_Linux_O32_Android:
			{
				final AndroidNDK androidNDK = AndroidNDK.enumerate(Machine.getLocal()).getNewest();
				final AndroidToolchain androidToolchain = androidNDK.enumerateToolchains(abi, AndroidToolchain.Type.GNU).getNewest();
				return new Toolchain(androidToolchain.getCppCompiler(), androidToolchain.getCCompiler(), androidToolchain.getAssembler(), androidToolchain.getLinker(), null, androidToolchain.getStrip(), androidToolchain.getObjCopy());
			}
			case X64_Linux_SystemV_Default:
			case X86_Linux_Pic_i586:
			{
				final GccToolchain gccToolchain = GccToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				final GnuBinutils gnuBinutils = GnuBinutils.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), abi).getNewest();
				final JavaSDK javaSDK = JavaSDK.enumerate(Machine.getLocal()).getNewest();
				return new Toolchain(gccToolchain.getCppCompiler(), gccToolchain.getCCompiler(), nasm,
						gccToolchain.getCppCompiler().asLinker(new LinkedList<AbsoluteDirectoryPath>()), javaSDK,
						gnuBinutils.getStrip(), gnuBinutils.getObjCopy());
			}
			case ARM_Linux_HardEABI_V7A:
			case ARM_Linux_SoftEABI_V5T:
			{
				final GccToolchain gccToolchain = GccToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				final GnuBinutils gnuBinutils = GnuBinutils.enumerate(Machine.getLocal(), abi).getNewest();
				final JavaSDK javaSDK = JavaSDK.enumerate(Machine.getLocal()).getNewest();
				return new Toolchain(gccToolchain.getCppCompiler(), gccToolchain.getCCompiler(), gnuBinutils.getAssembler(),
						gccToolchain.getCppCompiler().asLinker(new LinkedList<AbsoluteDirectoryPath>()), javaSDK,
						gnuBinutils.getStrip(), gnuBinutils.getObjCopy());
			}
			case X64_Linux_KNC_Default:
			{
				final GnuBinutils gnuBinutils = GnuBinutils.enumerate(Machine.getLocal(), abi).getNewest();
				final IntelCppToolchain intelCppToolchain = IntelCppToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				return new Toolchain(intelCppToolchain.getCppCompiler(), intelCppToolchain.getCCompiler(), gnuBinutils.getAssembler(),
						intelCppToolchain.getCppCompiler().asLinker(new LinkedList<AbsoluteDirectoryPath>()), null,
						gnuBinutils.getStrip(), gnuBinutils.getObjCopy());
			}
			case X64_MacOSX_SystemV_Default:
			case X86_MacOSX_Pic_Default:
			{
				final ClangToolchain clangToolchain = ClangToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				final AppleStrip appleStrip = AppleStrip.enumerate(Machine.getLocal(), abi).getNewest();
				final AppleDSymUtil appleDSymUtil = AppleDSymUtil.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), abi).getNewest();
				final JavaSDK javaSDK = JavaSDK.enumerate(Machine.getLocal()).getNewest();
				return new Toolchain(clangToolchain.getCppCompiler(), clangToolchain.getCCompiler(), nasm,
						clangToolchain.getCppCompiler().asLinker(new LinkedList<AbsoluteDirectoryPath>()), javaSDK,
						appleStrip, appleDSymUtil);
			}
			default:
				return null;
		}
	}

}
