/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

namespace Yeppp
{

	/// <summary>ARM-specific non-ISA processor or system features.</summary>
	/// <seealso cref="Library.IsSupported(CpuSystemFeature)" />
	public sealed class ArmCpuSystemFeature : CpuSystemFeature {

		/// <summary>VFP vector mode is supported in hardware.</summary>
		public static readonly ArmCpuSystemFeature VFPVectorMode = new ArmCpuSystemFeature(32);

		internal ArmCpuSystemFeature(uint id) : base(id, CpuArchitecture.ARM.Id)
		{
		}

	}

}
