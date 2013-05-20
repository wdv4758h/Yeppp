/*
 *                      Yeppp! library build framework
 *
 * This file is part of Yeppp! library infrastructure and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

import info.yeppp.ebuilda.*;
import info.yeppp.ebuilda.filesystem.AbsoluteDirectoryPath;
import info.yeppp.ebuilda.filesystem.AbsoluteFilePath;
import info.yeppp.ebuilda.filesystem.RelativeDirectoryPath;
import info.yeppp.ebuilda.filesystem.RelativeFilePath;
import info.yeppp.ebuilda.sdk.AndroidNDK;
import info.yeppp.ebuilda.sdk.AndroidToolchain;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class CLIBuild {

	public static void main(String[] args) throws Exception {
		final AbsoluteDirectoryPath yepppRoot = Machine.getLocal().getWorkingDirectory();

		for (final String abiName : args) {
			final ABI abi = ABI.parse(abiName);
			final Toolchain toolchain = getToolchain(abi);
			setup(toolchain.cppCompiler, toolchain.assembler, toolchain.linker, yepppRoot);
			build(toolchain.cppCompiler, toolchain.assembler, toolchain.linker, yepppRoot);
		}
	}

	static class Toolchain {
		public Toolchain(CppCompiler cppCompiler, Assembler assembler, Linker linker) {
			this.cppCompiler = cppCompiler;
			this.assembler = assembler;
			this.linker = linker;
		}

		final CppCompiler cppCompiler;
		final Assembler assembler;
		final Linker linker;
	}

	public static void setup(CppCompiler cppCompiler, Assembler assembler, Linker linker, AbsoluteDirectoryPath yepppRoot) {
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

		if (assembler != null) {
			assembler.setSourceDirectory(sourceDirectory);
			assembler.setObjectDirectory(objectDirectory);
			if (assembler instanceof NASM) {
				final NASM nasm = (NASM)assembler;
				nasm.setOptimization(NASM.Optimization.Multipass);
			}
		}

		linker.setObjectDirectory(objectDirectory);
		linker.setBinariesDirectory(objectDirectory);
		linker.addDefaultGlobalLibraryDirectories();
		if (!abi.getOperatingSystem().equals(OperatingSystem.Windows)) {
			GnuLinker gnuLinker = (GnuLinker)linker;
			gnuLinker.setPIC(GnuLinker.PositionIndependentCode.Unlimited);
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
			case ARM_HardEABI:
				return Pattern.compile(".+\\.arm\\.asm");
			case MIPS_O32:
				return Pattern.compile(".+\\.mips\\.asm");
			default:
				throw new Error(String.format("Unknown low-level ABI %s", abi.getLowLevelABI().toString()));
		}
	}

	public static void build(CppCompiler cppCompiler, Assembler assembler, Linker linker, AbsoluteDirectoryPath yepppRoot) {
		final ABI abi = cppCompiler.getABI();
		final Architecture architecture = abi.getArchitecture();
		final OperatingSystem operatingSystem = abi.getOperatingSystem();
		final AbsoluteFilePath libraryBinaryPath = new AbsoluteFilePath(linker.getBinariesDirectory(), new RelativeFilePath("yeppp"));
		final BuildMessages buildMessages = new BuildMessages();
		final List<AbsoluteFilePath> cppSources = cppCompiler.getSourceDirectory().getFiles(Pattern.compile(".+\\.cpp"), true);
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
			if (sourcePath.equals("library/Unsafe.cpp") && !operatingSystem.equals(OperatingSystem.Linux)) {
				continue;
			}
			buildMessages.add(cppCompiler.compile(source));
			objects.add(cppCompiler.getObjectPath(source));
		}
		for (final AbsoluteFilePath source : asmSources) {
			buildMessages.add(assembler.assemble(source));
			objects.add(assembler.getObjectPath(source));
		}
		buildMessages.add(linker.linkDynamicLibrary(libraryBinaryPath, objects));
		for (BuildMessage buildMessage : buildMessages.iterable()) {
			System.out.println(buildMessage.toString());
		}
	}

	public static Toolchain getToolchain(ABI abi) {
		switch (abi) {
			case X64_Windows_Microsoft_Default:
			case X86_Windows_Default_i586:
			{
				final VisualStudio visualStudio = VisualStudio.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), abi).getNewest();
				return new Toolchain(visualStudio.getCppCompiler(), nasm, visualStudio.getLinker());
			}
			case IA64_Windows_Microsoft_Default:
			{
				final VisualStudio visualStudio = VisualStudio.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), ABI.X86_Windows_Default_i586).getNewest();
				return new Toolchain(visualStudio.getCppCompiler(), nasm, visualStudio.getLinker());
			}
			case ARM_Linux_SoftEABI_Android:
			case ARM_Linux_SoftEABI_AndroidV7A:
			case X86_Linux_Pic_Android:
			case MIPS_Linux_O32_Android:
			{
				final AndroidNDK androidNDK = AndroidNDK.enumerate(Machine.getLocal()).getNewest();
				final AndroidToolchain androidToolchain = androidNDK.enumerateToolchains(abi, AndroidToolchain.Type.GNU).getNewest();
				return new Toolchain(androidToolchain.getCppCompiler(), androidToolchain.getAssembler(), androidToolchain.getLinker());
			}
			case X64_Linux_SystemV_Default:
			case X86_Linux_Pic_i586:
			{
				final GnuToolchain gnuToolchain = GnuToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				final NASM nasm = NASM.enumerate(Machine.getLocal(), abi).getNewest();
				return new Toolchain(gnuToolchain.getCppCompiler(), nasm, gnuToolchain.getLinker());
			}
			case X64_Linux_KNC_Default:
			case ARM_Linux_HardEABI_V7A:
			case ARM_Linux_SoftEABI_V5T:
			{
				final GnuToolchain gnuToolchain = GnuToolchain.enumerate(Machine.getLocal(), abi).getNewest();
				return new Toolchain(gnuToolchain.getCppCompiler(), gnuToolchain.getAssembler(), gnuToolchain.getLinker());
			}
			default:
				return null;
		}
	}

}
