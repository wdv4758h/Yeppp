/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

namespace Yeppp
{

	/// <summary>x86-specific non-ISA processor or system features.</summary>
	/// <seealso cref="Library.IsSupported(CpuSystemFeature)" />
	public sealed class X86CpuSystemFeature : CpuSystemFeature
	{

		/// <summary>The CPU has x87 registers, and the operating systems preserves them during context switch.</summary>
		public static readonly X86CpuSystemFeature FPU           = new X86CpuSystemFeature(32);
		/// <summary>The CPU has xmm (SSE) registers, and the operating systems preserves them during context switch.</summary>
		public static readonly X86CpuSystemFeature XMM           = new X86CpuSystemFeature(33);
		/// <summary>The CPU has ymm (AVX) registers, and the operating systems preserves them during context switch.</summary>
		public static readonly X86CpuSystemFeature YMM           = new X86CpuSystemFeature(34);
		/// <summary>Processor allows to use misaligned memory operands in SSE instructions other than loads and stores.</summary>
		public static readonly X86CpuSystemFeature MisalignedSSE = new X86CpuSystemFeature(35);
		/// <summary>Processor and the operating system support the Padlock Advanced Cryptography Engine.</summary>
		public static readonly X86CpuSystemFeature ACE           = new X86CpuSystemFeature(36);
		/// <summary>Processor and the operating system support the Padlock Advanced Cryptography Engine 2.</summary>
		public static readonly X86CpuSystemFeature ACE2          = new X86CpuSystemFeature(37);
		/// <summary>Processor and the operating system support the Padlock Random Number Generator.</summary>
		public static readonly X86CpuSystemFeature RNG           = new X86CpuSystemFeature(38);
		/// <summary>Processor and the operating system support the Padlock Hash Engine.</summary>
		public static readonly X86CpuSystemFeature PHE           = new X86CpuSystemFeature(39);
		/// <summary>Processor and the operating system support the Padlock Montgomery Multiplier.</summary>
		public static readonly X86CpuSystemFeature PMM           = new X86CpuSystemFeature(40);
		/// <summary>The CPU has zmm (MIC or AVX-512) registers, and the operating system preserves them during context switch.</summary>
		public static readonly X86CpuSystemFeature ZMM           = new X86CpuSystemFeature(41);
		/// <summary>The CPU has bnd (MPX) registers, and the operating system preserved them during context switch.</summary>
		public static readonly X86CpuSystemFeature BND           = new X86CpuSystemFeature(42);

		internal X86CpuSystemFeature(uint id) : base(id, CpuArchitecture.X86.Id)
		{
		}

	}

}
