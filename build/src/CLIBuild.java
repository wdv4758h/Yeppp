/*
 *                      Yeppp! library build framework
 *
 * This file is part of Yeppp! library infrastructure and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

import info.yeppp.ebuilda.*;
import info.yeppp.ebuilda.filesystem.*;
import info.yeppp.ebuilda.sdk.AndroidNDK;
import info.yeppp.ebuilda.sdk.AndroidToolchain;
import info.yeppp.ebuilda.sdk.WindowsSDK;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class CLIBuild {

	public static void main(String[] args) throws Exception {
		final AbsoluteDirectoryPath yepppRoot = Machine.getLocal().getWorkingDirectory();

		for (final String abiName : args) {
			final ABI abi = ABI.parse(abiName);
			final Toolchain toolchain = getToolchain(abi);
			setup(toolchain.cppCompiler, toolchain.assembler, toolchain.linker, toolchain.microsoftResourceCompiler, toolchain.gnuStrip, toolchain.gnuObjCopy, yepppRoot);
			build(toolchain.cppCompiler, toolchain.assembler, toolchain.linker, toolchain.microsoftResourceCompiler, toolchain.gnuStrip, toolchain.gnuObjCopy, yepppRoot);
		}
	}

	static class Toolchain {
		public Toolchain(CppCompiler cppCompiler, Assembler assembler, Linker linker) {
			this.cppCompiler = cppCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.microsoftResourceCompiler = null;
			this.gnuStrip = null;
			this.gnuObjCopy = null;
		}

		public Toolchain(CppCompiler cppCompiler, Assembler assembler, Linker linker, MicrosoftResourceCompiler microsoftResourceCompiler) {
			this.cppCompiler = cppCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.microsoftResourceCompiler = microsoftResourceCompiler;
			this.gnuStrip = null;
			this.gnuObjCopy = null;
		}

		public Toolchain(CppCompiler cppCompiler, Assembler assembler, Linker linker, GnuStrip gnuStrip, GnuObjCopy gnuObjCopy) {
			this.cppCompiler = cppCompiler;
			this.assembler = assembler;
			this.linker = linker;
			this.microsoftResourceCompiler = null;
			this.gnuStrip = gnuStrip;
			this.gnuObjCopy = gnuObjCopy;
		}

		final CppCompiler cppCompiler;
		final Assembler assembler;
		final Linker linker;
		final MicrosoftResourceCompiler microsoftResourceCompiler;
		final GnuStrip gnuStrip;
		final GnuObjCopy gnuObjCopy;
	}

	public static void setup(CppCompiler cppCompiler, Assembler assembler, Linker linker, MicrosoftResourceCompiler microsoftResourceCompiler, GnuStrip gnuStrip, GnuObjCopy gnuObjCopy, AbsoluteDirectoryPath yepppRoot) {
		final ABI abi = cppCompiler.getABI();

		final AbsoluteDirectoryPath sourceDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/sources"));
		final AbsoluteDirectoryPath objectDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/binaries/" + abi.toString()));
		final AbsoluteDirectoryPath runtimeBinariesDirectory = new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("runtime/binaries/" + abi.toString()));

		cppCompiler.setSourceDirectory(sourceDirectory);
		cppCompiler.setObjectDirectory(objectDirectory);
		cppCompiler.addDefaultGlobalIncludeDirectories();
		cppCompiler.setVerboseBuild(true);
		cppCompiler.addMacro("YEP_BUILD_LIBRARY");
		if (!abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			GnuCppCompiler gnuCppCompiler = (GnuCppCompiler)cppCompiler;
			gnuCppCompiler.setPositionIndependentCodeGeneration(GnuCppCompiler.PositionIndependentCodeGeneration.UnlimitedLibraryPIC);
		}
		cppCompiler.setRttiEnabled(false);
		cppCompiler.setExceptionsSupport(CppCompiler.Exceptions.NoExceptions);
		cppCompiler.setRuntimeLibrary(CppCompiler.RuntimeLibrary.NoRuntimeLibrary);
		cppCompiler.setOptimization(CppCompiler.Optimization.MaxSpeedOptimization);
		cppCompiler.addIncludeDirectory(cppCompiler.getSourceDirectory());
		cppCompiler.addIncludeDirectory(new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/headers")));

		if (microsoftResourceCompiler != null) {
			microsoftResourceCompiler.setSourceDirectory(sourceDirectory);
			microsoftResourceCompiler.setObjectDirectory(objectDirectory);
			microsoftResourceCompiler.addDefaultGlobalIncludeDirectories();
			microsoftResourceCompiler.setVerboseBuild(true);
			microsoftResourceCompiler.addIncludeDirectory(sourceDirectory);
			microsoftResourceCompiler.addIncludeDirectory(new AbsoluteDirectoryPath(yepppRoot, new RelativeDirectoryPath("library/headers")));
		}

		if (assembler != null) {
			assembler.setSourceDirectory(sourceDirectory);
			assembler.setObjectDirectory(objectDirectory);
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

		linker.setObjectDirectory(objectDirectory);
		linker.setBinariesDirectory(objectDirectory);
		linker.addDefaultGlobalLibraryDirectories();
		if (!abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			GnuCppCompilerLinker gnuLinker = (GnuCppCompilerLinker)linker;
			gnuLinker.setPIC(GnuCppCompilerLinker.PositionIndependentCode.Unlimited);
		}
		linker.setVerboseBuild(true);
		linker.setRuntimeLibraryUse(false);
		linker.addLibraryDirectory(runtimeBinariesDirectory);
		linker.addStaticLibraryDependence("yeprt");
		if (abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			linker.addDynamicLibraryDependence("kernel32");
		}
	}

	public static Pattern getAssemblyPattern(ABI abi) {
		switch (abi.getLowLevelABI()) {
			case X86_Pic:
				return Pattern.compile(".+\\.x86\\-pic\\.asm");
			case X86_NonPic:
				return Pattern.compile(".+\\.x86\\-nonpic\\.asm");
			case X64_Microsoft:
				return Pattern.compile(".+\\.x64\\-ms\\.asm");
			case X64_SystemV:
				return Pattern.compile(".+\\.x64\\-sysv\\.asm");
			case ARM_SoftEABI:
				return Pattern.compile(".+\\.arm(?:\\-softeabi)?\\.asm");
			case ARM_HardEABI:
				return Pattern.compile(".+\\.arm(?:\\-hardeabi)?\\.asm");
			case MIPS_O32:
				return Pattern.compile(".+\\.mips\\.asm");
			default:
				throw new Error(String.format("Unknown low-level ABI %s", abi.getLowLevelABI().toString()));
		}
	}

	public static void build(CppCompiler cppCompiler, Assembler assembler, Linker linker, MicrosoftResourceCompiler microsoftResourceCompiler, GnuStrip gnuStrip, GnuObjCopy gnuObjCopy, AbsoluteDirectoryPath yepppRoot) throws IOException {
		final ABI abi = cppCompiler.getABI();
		final Architecture architecture = abi.getArchitecture();
		final OperatingSystem operatingSystem = abi.getOperatingSystem();
		final AbsoluteFilePath libraryBinaryPath = new AbsoluteFilePath(linker.getBinariesDirectory(), new RelativeFilePath("yeppp"));
		final BuildMessages buildMessages = new BuildMessages();
		final List<AbsoluteFilePath> cppSources = cppCompiler.getSourceDirectory().getFiles(Pattern.compile(".+\\.cpp"), true);
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
		buildMessages.add(linker.linkDynamicLibrary(libraryBinaryPath, objects));
		if ((gnuStrip != null) && (gnuObjCopy != null)) {
			final AbsoluteFilePath libraryBinary = new AbsoluteFilePath(linker.getBinariesDirectory(), new RelativeFilePath("libyeppp.so"));
			final AbsoluteFilePath debugBinary = new AbsoluteFilePath(linker.getBinariesDirectory(), new RelativeFilePath("libyeppp.dbg"));
			buildMessages.add(gnuStrip.extractDebugInformation(libraryBinary, debugBinary));
			buildMessages.add(gnuStrip.strip(libraryBinary));
			buildMessages.add(gnuObjCopy.addGnuDebugLink(libraryBinary, debugBinary));
			final AbsoluteFilePath finalLibraryBinary = new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), new RelativeFilePath("libyeppp.so"));
			final AbsoluteFilePath finalDebugBinary = new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), new RelativeFilePath("libyeppp.dbg"));
			try {
				getBinariesDirectory(yepppRoot, abi).create();
				FileSystem.copyFile(finalLibraryBinary, libraryBinary);
				FileSystem.copyFile(finalDebugBinary, debugBinary);
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
			try {
				getBinariesDirectory(yepppRoot, abi).create();
				FileSystem.copyFile(new AbsoluteFilePath(getBinariesDirectory(yepppRoot, abi), libraryBinary), new AbsoluteFilePath(linker.getBinariesDirectory(), libraryBinary));
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
				return new Toolchain(visualStudio.getCppCompiler(), nasm, visualStudio.getLinker(), resourceCompiler);
			}
			case ARM_Linux_SoftEABI_Android:
			case ARM_Linux_SoftEABI_AndroidV7A:
			case X86_Linux_Pic_Android:
			case MIPS_Linux_O32_Android:
			{
				final AndroidNDK androidNDK = AndroidNDK.enumerate(Machine.getLocal()).getNewest();
				final AndroidToolchain androidToolchain = androidNDK.enumerateToolchains(abi, AndroidToolchain.Type.GNU).getNewest();
				return new Toolchain(androidToolchain.getCppCompiler(), androidToolchain.getAssembler(), androidToolchain.getLinker(), androidToolchain.getStrip(), androidToolchain.getObjCopy());
			}
			case X64_Linux_SystemV_Default:
			case X86_Linux_Pic_i586:
			{
				final GnuToolchain gnuToolchain = GnuToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), abi).getNewest();
				return new Toolchain(gnuToolchain.getCppCompiler(), nasm, gnuToolchain.getLinker(), gnuToolchain.getStrip(), gnuToolchain.getObjCopy());
			}
			case X64_Linux_KNC_Default:
			case ARM_Linux_HardEABI_V7A:
			case ARM_Linux_SoftEABI_V5T:
			{
				final GnuToolchain gnuToolchain = GnuToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				return new Toolchain(gnuToolchain.getCppCompiler(), gnuToolchain.getAssembler(), gnuToolchain.getLinker(), gnuToolchain.getStrip(), gnuToolchain.getObjCopy());
			}
			default:
				return null;
		}
	}

}
