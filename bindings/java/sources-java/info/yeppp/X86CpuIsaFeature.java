/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * x86-specific ISA extensions.
 *
 * @see	Library#isSupported(CpuIsaFeature)
 */
public class X86CpuIsaFeature extends CpuIsaFeature {

	/**
	 * x87 FPU integrated on chip.
	 */
	public static final X86CpuIsaFeature FPU        = new X86CpuIsaFeature(0);
	/**
	 * CPUID instruction.
	 */
	public static final X86CpuIsaFeature Cpuid      = new X86CpuIsaFeature(1);
	/**
	 * RDTSC instruction.
	 */
	public static final X86CpuIsaFeature Rdtsc      = new X86CpuIsaFeature(2);
	/**
	 * CMOV, FCMOV, and FCOMI/FUCOMI instructions.
	 */
	public static final X86CpuIsaFeature CMOV       = new X86CpuIsaFeature(3);
	/**
	 * SYSENTER and SYSEXIT instructions.
	 */
	public static final X86CpuIsaFeature SYSENTER   = new X86CpuIsaFeature(4);
	/**
	 * SYSCALL and SYSRET instructions.
	 */
	public static final X86CpuIsaFeature SYSCALL    = new X86CpuIsaFeature(5);
	/**
	 * RDMSR and WRMSR instructions.
	 */
	public static final X86CpuIsaFeature MSR        = new X86CpuIsaFeature(6);
	/**
	 * CLFLUSH instruction.
	 */
	public static final X86CpuIsaFeature Clflush    = new X86CpuIsaFeature(7);
	/**
	 * MONITOR and MWAIT instructions.
	 */
	public static final X86CpuIsaFeature MONITOR    = new X86CpuIsaFeature(8);
	/**
	 * FXSAVE and FXRSTOR instructions.
	 */
	public static final X86CpuIsaFeature FXSAVE     = new X86CpuIsaFeature(9);
	/**
	 * XSAVE, XRSTOR, XGETBV, and XSETBV instructions.
	 */
	public static final X86CpuIsaFeature XSAVE      = new X86CpuIsaFeature(10);
	/**
	 * CMPXCHG8B instruction.
	 */
	public static final X86CpuIsaFeature Cmpxchg8b  = new X86CpuIsaFeature(11);
	/**
	 * CMPXCHG16B instruction.
	 */
	public static final X86CpuIsaFeature Cmpxchg16b = new X86CpuIsaFeature(12);
	/**
	 * Support for 64-bit mode.
	 */
	public static final X86CpuIsaFeature X64        = new X86CpuIsaFeature(13);
	/**
	 * Support for LAHF and SAHF instructions in 64-bit mode.
	 */
	public static final X86CpuIsaFeature LahfSahf64 = new X86CpuIsaFeature(14);
	/**
	 * RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions.
	 */
	public static final X86CpuIsaFeature FsGsBase   = new X86CpuIsaFeature(15);
	/**
	 * MOVBE instruction.
	 */
	public static final X86CpuIsaFeature Movbe      = new X86CpuIsaFeature(16);
	/**
	 * POPCNT instruction.
	 */
	public static final X86CpuIsaFeature Popcnt     = new X86CpuIsaFeature(17);
	/**
	 * LZCNT instruction.
	 */
	public static final X86CpuIsaFeature Lzcnt      = new X86CpuIsaFeature(18);
	/**
	 * BMI instruction set.
	 */
	public static final X86CpuIsaFeature BMI        = new X86CpuIsaFeature(19);
	/**
	 * BMI 2 instruction set.
	 */
	public static final X86CpuIsaFeature BMI2       = new X86CpuIsaFeature(20);
	/**
	 * TBM instruction set.
	 */
	public static final X86CpuIsaFeature TBM        = new X86CpuIsaFeature(21);
	/**
	 * RDRAND instruction.
	 */
	public static final X86CpuIsaFeature Rdrand     = new X86CpuIsaFeature(22);
	/**
	 * Padlock Advanced Cryptography Engine on chip.
	 */
	public static final X86CpuIsaFeature ACE        = new X86CpuIsaFeature(23);
	/**
	 * Padlock Advanced Cryptography Engine 2 on chip.
	 */
	public static final X86CpuIsaFeature ACE2       = new X86CpuIsaFeature(24);
	/**
	 * Padlock Random Number Generator on chip.
	 */
	public static final X86CpuIsaFeature RNG        = new X86CpuIsaFeature(25);
	/**
	 * Padlock Hash Engine on chip.
	 */
	public static final X86CpuIsaFeature PHE        = new X86CpuIsaFeature(26);
	/**
	 * Padlock Montgomery Multiplier on chip.
	 */
	public static final X86CpuIsaFeature PMM        = new X86CpuIsaFeature(27);
	/**
	 * AES instruction set.
	 */
	public static final X86CpuIsaFeature AES        = new X86CpuIsaFeature(28);
	/**
	 * PCLMULQDQ instruction.
	 */
	public static final X86CpuIsaFeature Pclmulqdq  = new X86CpuIsaFeature(29);
	/**
	 * RDTSCP instruction.
	 */
	public static final X86CpuIsaFeature Rdtscp     = new X86CpuIsaFeature(30);
	/**
	 * Lightweight Profiling extension.
	 */
	public static final X86CpuIsaFeature LPW        = new X86CpuIsaFeature(31);
	/**
	 * Hardware Lock Elision extension.
	 */
	public static final X86CpuIsaFeature HLE        = new X86CpuIsaFeature(32);
	/**
	 * Restricted Transactional Memory extension.
	 */
	public static final X86CpuIsaFeature RTM        = new X86CpuIsaFeature(33);
	/**
	 * XTEST instruction.
	 */
	public static final X86CpuIsaFeature Xtest      = new X86CpuIsaFeature(34);
	/**
	 * RDSEED instruction.
	 */
	public static final X86CpuIsaFeature Rdseed     = new X86CpuIsaFeature(35);
	/**
	 * ADCX and ADOX instructions.
	 */
	public static final X86CpuIsaFeature ADX        = new X86CpuIsaFeature(36);
	/**
	 * SHA instruction set.
	 */
	public static final X86CpuIsaFeature SHA        = new X86CpuIsaFeature(37);
	/**
	 * Memory Protection Extension.
	 */
	public static final X86CpuIsaFeature MPX        = new X86CpuIsaFeature(38);

	protected X86CpuIsaFeature(int id) {
		super(id, CpuArchitecture.X86.getId());
	}

};
