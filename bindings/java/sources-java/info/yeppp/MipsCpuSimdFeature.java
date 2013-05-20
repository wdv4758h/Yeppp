/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	MIPS-specific SIMD extensions.
 * @see	Library#isSupported(CpuSimdFeature)
 */
public class MipsCpuSimdFeature extends CpuSimdFeature {
	
	/** @brief MDMX instruction set. */
	public static final MipsCpuSimdFeature MDMX         = new MipsCpuSimdFeature(0);
	/** @brief MIPS3D instruction set. */
	public static final MipsCpuSimdFeature MIPS3D       = new MipsCpuSimdFeature(1);
	/** @brief Paired-single instructions. */
	public static final MipsCpuSimdFeature PairedSingle = new MipsCpuSimdFeature(2);
	/** @brief MIPS DSP extension. */
	public static final MipsCpuSimdFeature DSP          = new MipsCpuSimdFeature(3);
	/** @brief MIPS DSP Release 2 extension. */
	public static final MipsCpuSimdFeature DSP2         = new MipsCpuSimdFeature(4);
	/** @brief Loongson (Godson) MMX instruction set. */
	public static final MipsCpuSimdFeature GodsonMMX    = new MipsCpuSimdFeature(5);
	/** @brief Ingenic Media Extension. */
	public static final MipsCpuSimdFeature IMX          = new MipsCpuSimdFeature(6);

	protected MipsCpuSimdFeature(int id) {
		super(id, CpuArchitecture.MIPS.getId());
	}

};
