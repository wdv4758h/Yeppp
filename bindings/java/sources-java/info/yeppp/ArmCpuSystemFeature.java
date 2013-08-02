/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * @brief	ARM-specific non-ISA processor or system features.
 * @see	Library#isSupported(CpuSystemFeature)
 */
public class ArmCpuSystemFeature extends CpuSystemFeature {
	
	/** @brief VFP vector mode is supported in hardware. */
	public static final ArmCpuSystemFeature VFPVectorMode = new ArmCpuSystemFeature(32);

	protected ArmCpuSystemFeature(int id) {
		super(id, CpuArchitecture.ARM.getId());
	}

};
