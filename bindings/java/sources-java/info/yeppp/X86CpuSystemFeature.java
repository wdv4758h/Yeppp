/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	x86-specific non-ISA processor or system features.
 * @see	Library#isSupported(CpuSystemFeature)
 */
public class X86CpuSystemFeature extends CpuSystemFeature {

	/** @brief The CPU has x87 registers, and the operating systems preserves them during context switch. */
	public static final X86CpuSystemFeature FPU           = new X86CpuSystemFeature(32);
	/** @brief The CPU has SSE registers, and the operating systems preserves them during context switch. */
	public static final X86CpuSystemFeature SSE           = new X86CpuSystemFeature(33);
	/** @brief The CPU has AVX registers, and the operating systems preserves them during context switch. */
	public static final X86CpuSystemFeature AVX           = new X86CpuSystemFeature(34);
	/** @brief Processor allows to use misaligned memory operands in SSE instructions other than loads and stores. */
	public static final X86CpuSystemFeature MisalignedSSE = new X86CpuSystemFeature(35);
	/** @brief Processor and the operating system support the Padlock Advanced Cryptography Engine. */
	public static final X86CpuSystemFeature ACE           = new X86CpuSystemFeature(36);
	/** @brief Processor and the operating system support the Padlock Advanced Cryptography Engine 2. */
	public static final X86CpuSystemFeature ACE2          = new X86CpuSystemFeature(37);
	/** @brief Processor and the operating system support the Padlock Random Number Generator. */
	public static final X86CpuSystemFeature RNG           = new X86CpuSystemFeature(38);
	/** @brief Processor and the operating system support the Padlock Hash Engine. */
	public static final X86CpuSystemFeature PHE           = new X86CpuSystemFeature(39);
	/** @brief Processor and the operating system support the Padlock Montgomery Multiplier. */
	public static final X86CpuSystemFeature PMM           = new X86CpuSystemFeature(40);
	/** @brief The CPU has MIC registers, and the operating system preserves them during context switch. */
	public static final X86CpuSystemFeature MIC           = new X86CpuSystemFeature(41);

	protected X86CpuSystemFeature(int id) {
		super(id, CpuArchitecture.X86.getId());
	}

};
