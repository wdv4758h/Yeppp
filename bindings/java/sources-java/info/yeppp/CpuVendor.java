/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * The company which designed the processor microarchitecture.
 *
 * @see	Library#getCpuVendor
 */
public final class CpuVendor {
	static {
		Library.load();
	}

	/**
	 * Processor vendor is not known to the library, or the library failed to get vendor information from the OS.
	 */
	public static final CpuVendor Unknown            = new CpuVendor(0);

	/* x86/x86-64 CPUs */

	/**
	 * Intel Corporation. Vendor of x86, x86-64, IA64, and ARM processor microarchitectures.
	 * <p>
	 * Sold its ARM design subsidiary in 2006. The last ARM processor design was released in 2004.
	 */
	public static final CpuVendor Intel              = new CpuVendor(1);
	/**
	 * Advanced Micro Devices, Inc. Vendor of x86 and x86-64 processor microarchitectures.
	 */
	public static final CpuVendor AMD                = new CpuVendor(2);
	/**
	 * VIA Technologies, Inc. Vendor of x86 and x86-64 processor microarchitectures.
	 * <p>
	 * Processors are designed by Centaur Technology, a subsidiary of VIA Technologies.
	 */
	public static final CpuVendor VIA                = new CpuVendor(3);
	/**
	 * Transmeta Corporation. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Now defunct. The last processor design was released in 2004.
	 * <p>
	 * Transmeta processors implemented VLIW ISA and used binary translation to execute x86 code.
	 */
	public static final CpuVendor Transmeta          = new CpuVendor(4);
	/**
	 * Cyrix Corporation. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Now defunct. The last processor design was released in 1996.
	 */
	public static final CpuVendor Cyrix              = new CpuVendor(5);
	/**
	 * Rise Technology. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Now defunct. The last processor design was released in 1999.
	 */
	public static final CpuVendor Rise               = new CpuVendor(6);
	/**
	 * National Semiconductor. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Sold its x86 design subsidiary in 1999. The last processor design was released in 1998.
	 */
	public static final CpuVendor NSC                = new CpuVendor(7);
	/**
	 * Silicon Integrated Systems. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Sold its x86 design subsidiary in 2001. The last processor design was released in 2001.
	 */
	public static final CpuVendor SiS                = new CpuVendor(8);
	/**
	 * NexGen. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Now defunct. The last processor design was released in 1994.
	 * <p>
	 * NexGen designed the first x86 microarchitecture which decomposed x86 instructions into simple microoperations.
	 */
	public static final CpuVendor NexGen             = new CpuVendor(9);
	/**
	 * United Microelectronics Corporation. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Ceased x86 in the early 1990s. The last processor design was released in 1991.
	 * <p>
	 * Designed U5C and U5D processors. Both are 486 level.
	 */
	public static final CpuVendor UMC                = new CpuVendor(10);
	/**
	 * RDC Semiconductor Co., Ltd. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Designes embedded x86 CPUs.
	 */
	public static final CpuVendor RDC                = new CpuVendor(11);
	/**
	 * DM&P Electronics Inc. Vendor of x86 processor microarchitectures.
	 * <p>
	 * Mostly embedded x86 designs.
	 */
	public static final CpuVendor DMP                = new CpuVendor(12);

	/* ARM CPUs */

	/**
	 * ARM Holdings plc. Vendor of ARM processor microarchitectures.
	 */
	public static final CpuVendor ARM                = new CpuVendor(20);
	/**
	 * Marvell Technology Group Ltd. Vendor of ARM processor microarchitectures.
	 */
	public static final CpuVendor Marvell            = new CpuVendor(21);
	/**
	 * Qualcomm Incorporated. Vendor of ARM processor microarchitectures.
	 */
	public static final CpuVendor Qualcomm           = new CpuVendor(22);
	/**
	 * Digital Equipment Corporation. Vendor of ARM processor microarchitecture.
	 * <p>
	 * Sold its ARM designs in 1997. The last processor design was released in 1997.
	 */
	public static final CpuVendor DEC                = new CpuVendor(23);
	/**
	 * Texas Instruments Inc. Vendor of ARM processor microarchitectures.
	 */
	public static final CpuVendor TI                 = new CpuVendor(24);
	/**
	 * Apple Inc. Vendor of ARM processor microarchitectures.
	 */
	public static final CpuVendor Apple              = new CpuVendor(25);

	/* MIPS CPUs */

	/**
	 * Ingenic Semiconductor. Vendor of MIPS processor microarchitectures.
	 */
	public static final CpuVendor Ingenic            = new CpuVendor(40);
	/**
	 * Institute of Computing Technology of the Chinese Academy of Sciences. Vendor of MIPS processor microarchitectures.
	 */
	public static final CpuVendor ICT                = new CpuVendor(41);
	/**
	 * MIPS Technologies, Inc. Vendor of MIPS processor microarchitectures.
	 */
	public static final CpuVendor MIPS               = new CpuVendor(42);

	/* PowerPC CPUs */

	/**
	 * International Business Machines Corporation. Vendor of PowerPC processor microarchitectures.
	 */
	public static final CpuVendor IBM                = new CpuVendor(50);
	/**
	 * Motorola, Inc. Vendor of PowerPC and ARM processor microarchitectures.
	 */
	public static final CpuVendor Motorola           = new CpuVendor(51);
	/**
	 * P.A.Semi. Vendor of PowerPC processor microarchitectures.
	 * <p>
	 * Now defunct. The last processor design was released in 2007.
	 */
	public static final CpuVendor PASemi             = new CpuVendor(52);

	/* SPARC CPUs */

	/**
	 * Sun Microsystems, Inc. Vendor of SPARC processor microarchitectures.
	 * <p>
	 * Now defunct. The last processor design was released in 2008.
	 */
	public static final CpuVendor Sun                = new CpuVendor(60);
	/**
	 * Oracle Corporation. Vendor of SPARC processor microarchitectures.
	 */
	public static final CpuVendor Oracle             = new CpuVendor(61);
	/**
	 * Fujitsu Limited. Vendor of SPARC processor microarchitectures.
	 */
	public static final CpuVendor Fujitsu            = new CpuVendor(62);
	/**
	 * Moscow Center of SPARC Technologies CJSC. Vendor of SPARC processor microarchitectures.
	 */
	public static final CpuVendor MCST               = new CpuVendor(63);

	private final int id;

	protected CpuVendor(int id) {
		this.id = id;
	}

	protected int getId() {
		return this.id;
	}

	private static native String toString(int id);
	private static native String getDescription(int id);

	public final boolean equals(CpuVendor other) {
		if (other == null) {
			return false;
		} else {
			return this.id == other.id;
		}
	}

	@Override
	public final boolean equals(Object other) {
		if (other instanceof CpuVendor) {
			return this.equals((CpuVendor)other);
		} else {
			return false;
		}
	}

	@Override
	public final int hashCode() {
		return this.id;
	}

	/**
	 * Provides a string ID for this CPU vendor.
	 *
	 * @return	A string which starts with a Latin letter and contains only Latin letters, digits, and underscore symbol.
	 *
	 * @see	#getDescription()
	 */
	@Override
	public final String toString() {
		return CpuVendor.toString(this.id);
	}

	/**
	 * Provides a text description for this CPU vendor.
	 *
	 * @return	A string description which can contain spaces and non-ASCII characters.
	 *
	 * @see	#toString()
	 */
	public final String getDescription() {
		return CpuVendor.getDescription(this.id);
	}
};
