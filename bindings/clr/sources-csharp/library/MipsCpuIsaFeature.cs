/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

namespace Yeppp
{

	/// <summary>MIPS-specific ISA extensions.</summary>
	/// <seealso cref="Library.IsSupported(CpuIsaFeature)" />
	public sealed class MipsCpuIsaFeature : CpuIsaFeature
	{

		/// <summary>MIPS32/MIPS64 Release 2 architecture.</summary>
		public static readonly MipsCpuIsaFeature R2        = new MipsCpuIsaFeature(0);
		/// <summary>MicroMIPS extension.</summary>
		public static readonly MipsCpuIsaFeature MicroMIPS = new MipsCpuIsaFeature(1);
		/// <summary>FPU with S, D, and W formats and instructions.</summary>
		public static readonly MipsCpuIsaFeature FPU       = new MipsCpuIsaFeature(2);
		/// <summary>Multi-threading extension.</summary>
		public static readonly MipsCpuIsaFeature MT        = new MipsCpuIsaFeature(3);
		/// <summary>MIPS16 extension.</summary>
		public static readonly MipsCpuIsaFeature MIPS16    = new MipsCpuIsaFeature(4);
		/// <summary>SmartMIPS extension.</summary>
		public static readonly MipsCpuIsaFeature SmartMIPS = new MipsCpuIsaFeature(5);

		internal MipsCpuIsaFeature(uint id) : base(id, CpuArchitecture.MIPS.Id)
		{
		}

	}

}
