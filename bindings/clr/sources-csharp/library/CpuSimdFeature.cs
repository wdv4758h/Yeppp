/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

namespace Yeppp
{

	/// <summary>SIMD extensions.</summary>
	/// <seealso cref="CpuArchitecture.CpuSimdFeatures" />
	/// <seealso cref="Library.IsSupported(CpuSimdFeature)" />
	/// <seealso cref="X86CpuSimdFeature" />
	/// <seealso cref="ArmCpuSimdFeature" />
	/// <seealso cref="MipsCpuSimdFeature" />
	public class CpuSimdFeature {

		private readonly uint architectureId;
		private readonly uint id;

		internal CpuSimdFeature(uint id, uint architectureId) {
			this.id = id;
			this.architectureId = architectureId;
		}

		internal CpuSimdFeature(uint id) {
			this.id = id;
			this.architectureId = CpuArchitecture.Unknown.Id;
		}

		internal uint Id
		{
			get
			{
				return this.id;
			}
		}

		internal uint ArchitectureId
		{
			get
			{
				return this.architectureId;
			}
		}

		/// <summary>Compares for equality with another <see cref="CpuSimdFeature" /> object.</summary>
		/// <remarks>Comparison is performed by value.</remarks>
		public bool Equals(CpuSimdFeature other)
		{
			if (other == null)
				return false;

			return ((this.id ^ other.id) | (this.architectureId ^ other.architectureId)) == 0;
		}

		/// <summary>Compares for equality with another object.</summary>
		/// <remarks>Comparison is performed by value.</remarks>
		public override bool Equals(System.Object other)
		{
			if (other == null || GetType() != other.GetType())
				return false;

			return this.Equals((CpuSimdFeature)other);
		}

		/// <summary>Provides a hash for the object.</summary>
		/// <remarks>Non-equal <see cref="CpuSimdFeature" /> objects are guaranteed to have different hashes.</remarks>
		public override int GetHashCode()
		{
			return unchecked((int)(this.id ^ (this.architectureId << 16)));
		}

		/// <summary>Provides a string representation for the object.</summary>
		/// <remarks>The string representation is provided by the Yeppp! library (not Yeppp! .Net bindings).</remarks>
		public override string ToString()
		{
			Enumeration enumeration = unchecked((Enumeration)(0x200 + this.architectureId));
			return Library.GetString(enumeration, this.id);
		}

		internal static bool IsDefined(uint id, uint architectureId)
		{
			Enumeration enumeration = unchecked((Enumeration)(0x200 + architectureId));
			return Library.IsDefined(enumeration, id);
		}

	}

}
