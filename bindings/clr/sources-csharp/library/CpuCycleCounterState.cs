/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

namespace Yeppp
{

	/// <summary>The state of the processor cycle counter.</summary>
	/// <remarks>This class is intended for use only through <see cref="Library.AcquireCycleCounter" /> and <see cref="Library.ReleaseCycleCounter" /> methods.</remarks>
	/// <seealso cref="Library.AcquireCycleCounter" />
	/// <seealso cref="Library.ReleaseCycleCounter" />
	public sealed class CpuCycleCounterState
	{

		internal CpuCycleCounterState(ulong state)
		{
			this.state = state;
		}

		~CpuCycleCounterState()
		{
			if (this.IsValid)
			{
				Library.ReleaseCycleCounter(this);
			}
		}

		public bool IsValid
		{
			get
			{
				return this.state != 0;
			}
		}

		internal ulong state;

	}

}
