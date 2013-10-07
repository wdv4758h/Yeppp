/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * PowerPC-specific SIMD extensions.
 *
 * @see	Library#isSupported(CpuSimdFeature)
 */
public class PowerPCCpuSimdFeature extends CpuSimdFeature {

	/**
	 * Vector Media eXtension (aka AltiVec and Velocity Engine).
	 */
	public static final PowerPCCpuSimdFeature VMX           = new PowerPCCpuSimdFeature(0);
	/**
	 * VMX VPERMXOR instruction from Power ISA 2.07.
	 */
	public static final PowerPCCpuSimdFeature VMXRAID       = new PowerPCCpuSimdFeature(1);
	/**
	 * Additional VMX instructions from Power ISA 2.07.
	 */
	public static final PowerPCCpuSimdFeature VMX207        = new PowerPCCpuSimdFeature(2);
	/**
	 * VSX instructions (Vector-Scalar eXtensions).
	 */
	public static final PowerPCCpuSimdFeature VSX           = new PowerPCCpuSimdFeature(8);
	/**
	 * Additional VSX instructions from Power ISA 2.07.
	 */
	public static final PowerPCCpuSimdFeature VSX207        = new PowerPCCpuSimdFeature(9);
	/**
	 * SPE (Signal Processing Engine).
	 */
	public static final PowerPCCpuSimdFeature SPE           = new PowerPCCpuSimdFeature(24);
	/**
	 * Embedded Floating-Point Vector instructions.
	 */
	public static final PowerPCCpuSimdFeature EFPV          = new PowerPCCpuSimdFeature(25);
	/**
	 * Double Hummer instruction set.
	 *
	 * 2-wide double precision floating-point SIMD for Blue Gene/L and Blue Gene/P supercomputers.
	 */
	public static final PowerPCCpuSimdFeature DoubleHummer  = new PowerPCCpuSimdFeature(48);
	/**
	 * Quad Processing eXtension.
	 *
	 * 4-wide double precision floating-point SIMD for Blue Gene/Q supercomputers.
	 */
	public static final PowerPCCpuSimdFeature QPX           = new PowerPCCpuSimdFeature(49);

	protected PowerPCCpuSimdFeature(int id) {
		super(id, CpuArchitecture.PowerPC.getId());
	}

};
