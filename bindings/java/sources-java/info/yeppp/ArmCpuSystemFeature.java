/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * ARM-specific non-ISA processor or system features.
 *
 * @see	Library#isSupported(CpuSystemFeature)
 */
public class ArmCpuSystemFeature extends CpuSystemFeature {

	/**
	 * VFP vector mode is supported in hardware.
	 */
	public static final ArmCpuSystemFeature VFPVectorMode = new ArmCpuSystemFeature(32);
	/**
	 * The CPU has FPA registers (f0-f7), and the operating system preserves them during context switch.
	 */
	public static final ArmCpuSystemFeature FPA           = new ArmCpuSystemFeature(56);
	/**
	 * The CPU has WMMX registers (wr0-wr15), and the operating system preserves them during context switch.
	 */
	public static final ArmCpuSystemFeature WMMX          = new ArmCpuSystemFeature(57);
	/**
	 * The CPU has s0-s31 VFP registers, and the operating system preserves them during context switch.
	 */
	public static final ArmCpuSystemFeature S32           = new ArmCpuSystemFeature(58);
	/**
	 * The CPU has d0-d31 VFP registers, and the operating system preserves them during context switch.
	 */
	public static final ArmCpuSystemFeature D32           = new ArmCpuSystemFeature(59);

	protected ArmCpuSystemFeature(int id) {
		super(id, CpuArchitecture.ARM.getId());
	}

};
