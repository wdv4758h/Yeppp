/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * MIPS-specific ISA extensions.
 *
 * @see	Library#isSupported(CpuIsaFeature)
 */
public class MipsCpuIsaFeature extends CpuIsaFeature {

	/**
	 * MIPS I instructions.
	 */
	public static final MipsCpuIsaFeature MIPS_I    = new MipsCpuIsaFeature(0);
	/**
	 * MIPS II instructions.
	 */
	public static final MipsCpuIsaFeature MIPS_II   = new MipsCpuIsaFeature(1);
	/**
	 * MIPS III instructions.
	 */
	public static final MipsCpuIsaFeature MIPS_III  = new MipsCpuIsaFeature(2);
	/**
	 * MIPS IV instructions.
	 */
	public static final MipsCpuIsaFeature MIPS_IV   = new MipsCpuIsaFeature(3);
	/**
	 * MIPS V instructions.
	 */
	public static final MipsCpuIsaFeature MIPS_V    = new MipsCpuIsaFeature(4);
	/**
	 * MIPS32/MIPS64 Release 1 instructions.
	 */
	public static final MipsCpuIsaFeature R1        = new MipsCpuIsaFeature(5);
	/**
	 * MIPS32/MIPS64 Release 2 instructions.
	 */
	public static final MipsCpuIsaFeature R2        = new MipsCpuIsaFeature(6);
	/**
	 * FPU with S, D, and W formats and instructions.
	 */
	public static final MipsCpuIsaFeature FPU       = new MipsCpuIsaFeature(24);
	/**
	 * MIPS16 extension.
	 */
	public static final MipsCpuIsaFeature MIPS16    = new MipsCpuIsaFeature(25);
	/**
	 * SmartMIPS extension.
	 */
	public static final MipsCpuIsaFeature SmartMIPS = new MipsCpuIsaFeature(26);
	/**
	 * Multi-threading extension.
	 */
	public static final MipsCpuIsaFeature MT        = new MipsCpuIsaFeature(27);
	/**
	 * MicroMIPS extension.
	 */
	public static final MipsCpuIsaFeature MicroMIPS = new MipsCpuIsaFeature(28);
	/**
	 * MIPS virtualization extension.
	 */
	public static final MipsCpuIsaFeature VZ        = new MipsCpuIsaFeature(29);

	protected MipsCpuIsaFeature(int id) {
		super(id, CpuArchitecture.MIPS.getId());
	}

};
