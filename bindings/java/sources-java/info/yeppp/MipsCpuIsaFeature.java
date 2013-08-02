/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * @brief	MIPS-specific ISA extensions.
 * @see	Library#isSupported(CpuIsaFeature)
 */
public class MipsCpuIsaFeature extends CpuIsaFeature {
	
	/** @brief MIPS32/MIPS64 Release 2 architecture. */
	public static final MipsCpuIsaFeature R2        = new MipsCpuIsaFeature(0);
	/** @brief MicroMIPS extension. */
	public static final MipsCpuIsaFeature MicroMIPS = new MipsCpuIsaFeature(1);
	/** @brief FPU with S, D, and W formats and instructions. */
	public static final MipsCpuIsaFeature FPU       = new MipsCpuIsaFeature(2);
	/** @brief Multi-threading extension. */
	public static final MipsCpuIsaFeature MT        = new MipsCpuIsaFeature(3);
	/** @brief MIPS16 extension. */
	public static final MipsCpuIsaFeature MIPS16    = new MipsCpuIsaFeature(4);
	/** @brief SmartMIPS extension. */
	public static final MipsCpuIsaFeature SmartMIPS = new MipsCpuIsaFeature(5);

	protected MipsCpuIsaFeature(int id) {
		super(id, CpuArchitecture.MIPS.getId());
	}

};
