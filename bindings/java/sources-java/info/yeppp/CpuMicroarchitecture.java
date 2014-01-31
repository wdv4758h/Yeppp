/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * Type of processor microarchitecture.
 * <p>
 * Low-level instruction performance characteristics, such as latency and throughput, are constant within microarchitecture.
 * <p>
 * Processors of the same microarchitecture can differ in supported instruction sets and other extensions.
 *
 * @see	Library#getCpuMicroarchitecture
 */
public final class CpuMicroarchitecture {
	static {
		Library.load();
	}

	/**
	 * Microarchitecture is unknown, or the library failed to get information about the microarchitecture from OS
	 */
	public static final CpuMicroarchitecture Unknown           = new CpuMicroarchitecture(0);

	/**
	 * Pentium and Pentium MMX microarchitecture.
	 */
	public static final CpuMicroarchitecture P5                = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0001);
	/**
	 * Pentium Pro, Pentium II, and Pentium III.
	 */
	public static final CpuMicroarchitecture P6                = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0002);
	/**
	 * Pentium 4 with Willamette, Northwood, or Foster cores.
	 */
	public static final CpuMicroarchitecture Willamette        = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0003);
	/**
	 * Pentium 4 with Prescott and later cores.
	 */
	public static final CpuMicroarchitecture Prescott          = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0004);
	/**
	 * Pentium M.
	 */
	public static final CpuMicroarchitecture Dothan            = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0005);
	/**
	 * Intel Core microarchitecture.
	 */
	public static final CpuMicroarchitecture Yonah             = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0006);
	/**
	 * Intel Core 2 microarchitecture on 65 nm process.
	 */
	public static final CpuMicroarchitecture Conroe            = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0007);
	/** 
	 * Intel Core 2 microarchitecture on 45 nm process.
	 */
	public static final CpuMicroarchitecture Penryn            = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0008);
	/**
	 * Intel Atom on 45 nm process.
	 */
	public static final CpuMicroarchitecture Bonnell           = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0009);
	/**
	 * Intel Nehalem and Westmere microarchitectures (Core i3/i5/i7 1st gen).
	 */
	public static final CpuMicroarchitecture Nehalem           = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x000A);
	/**
	 * Intel Sandy Bridge microarchitecture (Core i3/i5/i7 2nd gen).
	 */
	public static final CpuMicroarchitecture SandyBridge       = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x000B);
	/**
	 * Intel Atom on 32 nm process.
	 */
	public static final CpuMicroarchitecture Saltwell          = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x000C);
	/**
	 * Intel Ivy Bridge microarchitecture (Core i3/i5/i7 3rd gen).
	 */
	public static final CpuMicroarchitecture IvyBridge         = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x000D);
	/**
	 * Intel Haswell microarchitecture (Core i3/i5/i7 4th gen).
	 */
	public static final CpuMicroarchitecture Haswell           = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x000E);
	/**
	 * Intel Silvermont microarchitecture (22 nm out-of-order Atom).
	 */
	public static final CpuMicroarchitecture Silvermont        = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x000F);

	/**
	 * Intel Knights Ferry HPC boards.
	 */
	public static final CpuMicroarchitecture KnightsFerry      = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0100);
	/**
	 * Intel Knights Corner HPC boards (aka Xeon Phi).
	 */
	public static final CpuMicroarchitecture KnightsCorner     = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0101);

	/**
	 * AMD K5.
	 */
	public static final CpuMicroarchitecture K5                = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0001);
	/**
	 * AMD K6 and alike.
	 */
	public static final CpuMicroarchitecture K6                = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0002);
	/**
	 * AMD Athlon and Duron.
	 */
	public static final CpuMicroarchitecture K7                = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0003);
	/** 
	 * AMD Geode GX and LX.
	 */
	public static final CpuMicroarchitecture Geode             = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0004);
	/** 
	 * AMD Athlon 64, Opteron 64.
	 */
	public static final CpuMicroarchitecture K8                = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0005);
	/**
	 * AMD K10 (Barcelona, Istambul, Magny-Cours).
	 */
	public static final CpuMicroarchitecture K10               = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0006);
	/**
	 * AMD Bobcat mobile microarchitecture.
	 */
	public static final CpuMicroarchitecture Bobcat            = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0007);
	/**
	 * AMD Bulldozer microarchitecture (1st gen K15).
	 */
	public static final CpuMicroarchitecture Bulldozer         = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0008);
	/**
	 * AMD Piledriver microarchitecture (2nd gen K15).
	 */
	public static final CpuMicroarchitecture Piledriver        = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x0009);
	/**
	 * AMD Jaguar mobile microarchitecture.
	 */
	public static final CpuMicroarchitecture Jaguar            = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x000A);
	/**
	 * AMD Steamroller microarchitecture (3rd gen K15).
	 */
	public static final CpuMicroarchitecture Steamroller       = new CpuMicroarchitecture((CpuArchitecture.X86.getId() << 24) + (CpuVendor.AMD.getId()      << 16) + 0x000B);

	/**
	 * DEC/Intel StrongARM processors.
	 */
	public static final CpuMicroarchitecture StrongARM         = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0001);
	/**
	 * Intel/Marvell XScale processors.
	 */
	public static final CpuMicroarchitecture XScale            = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Intel.getId()    << 16) + 0x0002);

	/**
	 * ARM7 series.
	 */
	public static final CpuMicroarchitecture ARM7              = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0001);
	/**
	 * ARM9 series.
	 */
	public static final CpuMicroarchitecture ARM9              = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0002);
	/**
	 * ARM 1136, ARM 1156, ARM 1176, or ARM 11MPCore.
	 */
	public static final CpuMicroarchitecture ARM11             = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0003);
	/**
	 * ARM Cortex-A5.
	 */
	public static final CpuMicroarchitecture CortexA5          = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0004);
	/**
	 * ARM Cortex-A7.
	 */
	public static final CpuMicroarchitecture CortexA7          = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0005);
	/**
	 * ARM Cortex-A8.
	 */
	public static final CpuMicroarchitecture CortexA8          = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0006);
	/**
	 * ARM Cortex-A9.
	 */
	public static final CpuMicroarchitecture CortexA9          = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0007);
	/**
	 * ARM Cortex-A12.
	 */
	public static final CpuMicroarchitecture CortexA12         = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0009);
	/**
	 * ARM Cortex-A15.
	 */
	public static final CpuMicroarchitecture CortexA15         = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x0008);
	/**
	 * ARM Cortex-A53.
	 */
	public static final CpuMicroarchitecture CortexA53         = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x000A);
	/**
	 * ARM Cortex-A57.
	 */
	public static final CpuMicroarchitecture CortexA57         = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.ARM.getId()      << 16) + 0x000B);

	/**
	 * Qualcomm Scorpion.
	 */
	public static final CpuMicroarchitecture Scorpion          = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Qualcomm.getId() << 16) + 0x0001);
	/**
	 * Qualcomm Krait.
	 */
	public static final CpuMicroarchitecture Krait             = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Qualcomm.getId() << 16) + 0x0002);

	/**
	 * Marvell Sheeva PJ1.
	 */
	public static final CpuMicroarchitecture PJ1               = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Marvell.getId()  << 16) + 0x0001);
	/**
	 * Marvell Sheeva PJ4.
	 */
	public static final CpuMicroarchitecture PJ4               = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Marvell.getId()  << 16) + 0x0002);

	/**
	 * Apple A6 and A6X processors.
	 */
	public static final CpuMicroarchitecture Swift             = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Apple.getId()    << 16) + 0x0001);
	/**
	 * Apple A7 processor.
	 */
	public static final CpuMicroarchitecture Cyclone           = new CpuMicroarchitecture((CpuArchitecture.ARM.getId() << 24) + (CpuVendor.Apple.getId()    << 16) + 0x0002);

	/**
	 * Intel Itanium.
	 */
	public static final CpuMicroarchitecture Itanium           = new CpuMicroarchitecture((CpuArchitecture.IA64.getId() << 24) + (CpuVendor.Intel.getId()   << 16) + 0x0001);
	/**
	 * Intel Itanium 2.
	 */
	public static final CpuMicroarchitecture Itanium2          = new CpuMicroarchitecture((CpuArchitecture.IA64.getId() << 24) + (CpuVendor.Intel.getId()   << 16) + 0x0002);

	/**
	 * MIPS 24K.
	 */
	public static final CpuMicroarchitecture MIPS24K           = new CpuMicroarchitecture((CpuArchitecture.MIPS.getId() << 24) + (CpuVendor.MIPS.getId()    << 16) + 0x0001);
	/**
	 * MIPS 34K.
	 */
	public static final CpuMicroarchitecture MIPS34K           = new CpuMicroarchitecture((CpuArchitecture.MIPS.getId() << 24) + (CpuVendor.MIPS.getId()    << 16) + 0x0002);
	/**
	 * MIPS 74K.
	 */
	public static final CpuMicroarchitecture MIPS74K           = new CpuMicroarchitecture((CpuArchitecture.MIPS.getId() << 24) + (CpuVendor.MIPS.getId()    << 16) + 0x0003);

	/**
	 * Ingenic XBurst.
	 */
	public static final CpuMicroarchitecture XBurst            = new CpuMicroarchitecture((CpuArchitecture.MIPS.getId() << 24) + (CpuVendor.Ingenic.getId() << 16) + 0x0001);
	/**
	 * Ingenic XBurst 2.
	 */
	public static final CpuMicroarchitecture XBurst2           = new CpuMicroarchitecture((CpuArchitecture.MIPS.getId() << 24) + (CpuVendor.Ingenic.getId() << 16) + 0x0002);

	/**
	 * IBM PowerPC 970 (PowerPC G5).
	 */
	public static final CpuMicroarchitecture PowerPC970        = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0021);

	/**
	 * IBM POWER 4.
	 */
	public static final CpuMicroarchitecture POWER4            = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x011F);
	/**
	 * IBM POWER 5.
	 */
	public static final CpuMicroarchitecture POWER5            = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0120);
	/**
	 * IBM POWER 6.
	 */
	public static final CpuMicroarchitecture POWER6            = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0121);
	/**
	 * IBM POWER 7.
	 */
	public static final CpuMicroarchitecture POWER7            = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0122);
	/**
	 * IBM POWER 8.
	 */
	public static final CpuMicroarchitecture POWER8            = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0123);

	/**
	 * IBM PowerPC 440 (Blue Gene/L processor).
	 */
	public static final CpuMicroarchitecture PowerPC440        = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0200);
	/**
	 * IBM PowerPC 450 (Blue Gene/P processor).
	 */
	public static final CpuMicroarchitecture PowerPC450        = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0201);
	/**
	 * IBM PowerPC A2 (Blue Gene/Q processor).
	 */
	public static final CpuMicroarchitecture PowerPCA2         = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.IBM.getId() << 16) + 0x0202);

	/**
	 * P.A.Semi PWRficient.
	 */
	public static final CpuMicroarchitecture PWRficient        = new CpuMicroarchitecture((CpuArchitecture.PowerPC.getId() << 24) + (CpuVendor.PASemi.getId() << 16) + 0x0001);

	private final int id;

	protected CpuMicroarchitecture(int id) {
		this.id = id;
	}

	public int getId() {
		return this.id;
	}

	private static native String toString(int id);
	private static native String getDescription(int id);

	public final boolean equals(CpuMicroarchitecture other) {
		if (other == null) {
			return false;
		} else {
			return this.id == other.id;
		}
	}

	@Override
	public final boolean equals(Object other) {
		if (other instanceof CpuMicroarchitecture) {
			return this.equals((CpuMicroarchitecture)other);
		} else {
			return false;
		}
	}

	@Override
	public final int hashCode() {
		return this.id;
	}

	/**
	 * Provides a string ID for this CPU microarchitecture.
	 *
	 * @return	A string which starts with a Latin letter and contains only Latin letters, digits, and underscore symbol.
	 *
	 * @see	#getDescription()
	 */
	@Override
	public final String toString() {
		return CpuMicroarchitecture.toString(this.id);
	}

	/**
	 * Provides a text description for this CPU microarchitecture.
	 *
	 * @return	A string description which can contain spaces and non-ASCII characters.
	 *
	 * @see	#toString()
	 */
	public final String getDescription() {
		return CpuMicroarchitecture.getDescription(this.id);
	}
};
