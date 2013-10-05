/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * ARM-specific SIMD extensions.
 *
 * @see	Library#isSupported(CpuSimdFeature)
 */
public class ArmCpuSimdFeature extends CpuSimdFeature {

	/**
	 * XScale instructions.
	 */
	public static final ArmCpuSimdFeature XScale     = new ArmCpuSimdFeature(0);
	/**
	 * Wireless MMX instruction set.
	 */
	public static final ArmCpuSimdFeature WMMX       = new ArmCpuSimdFeature(1);
	/**
	 * Wireless MMX 2 instruction set.
	 */
	public static final ArmCpuSimdFeature WMMX2      = new ArmCpuSimdFeature(2);
	/**
	 * NEON (Advanced SIMD) instruction set.
	 */
	public static final ArmCpuSimdFeature NEON       = new ArmCpuSimdFeature(3);
	/**
	 * NEON (Advanced SIMD) half-precision extension.
	 */
	public static final ArmCpuSimdFeature NEONHP     = new ArmCpuSimdFeature(4);
	/**
	 * NEON (Advanced SIMD) v2 instruction set.
	 */
	public static final ArmCpuSimdFeature NEON2      = new ArmCpuSimdFeature(5);

	protected ArmCpuSimdFeature(int id) {
		super(id, CpuArchitecture.ARM.getId());
	}

};
