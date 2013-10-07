/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * PowerPC-specific ISA extensions.
 *
 * @see	Library#isSupported(CpuIsaFeature)
 */
public class PowerPCCpuIsaFeature extends CpuIsaFeature {

	/**
	 * FPU instructions.
	 */
	public static final PowerPCCpuIsaFeature FPU        = new PowerPCCpuIsaFeature(0);
	/**
	 * MTOCRF and MFOCRF instructions.
	 *
	 * MTOCRF and MFOCRF are new forms of MTCRF and MFCRF instructions. They were introduced in PowerPC ISA 2.00.
	 */
	public static final PowerPCCpuIsaFeature MCRF       = new PowerPCCpuIsaFeature(1);
	/**
	 * FSQRT and FSQRTS instructions.
	 *
	 * These optional general-purpose instructions are defined in PowerPC ISA 2.01.
	 */
	public static final PowerPCCpuIsaFeature GPOpt      = new PowerPCCpuIsaFeature(2);
	/**
	 * FRES, FRSQRTE, and FSEL instructions.
	 *
	 * These optional graphics instructions are defined in PowerPC ISA 2.01.
	 */
	public static final PowerPCCpuIsaFeature GfxOpt     = new PowerPCCpuIsaFeature(3);
	/**
	 * FRE and FRSQRTES instructions.
	 *
	 * These optional graphics instructions are defined in PowerPC ISA 2.02.
	 */
	public static final PowerPCCpuIsaFeature GfxOpt202  = new PowerPCCpuIsaFeature(4);
	/**
	 * Legacy integer multiply-accumulate instructions.
	 *
	 * These multiply-accumulate instructions were implemented in some 400 series processors.
	 */
	public static final PowerPCCpuIsaFeature MAC        = new PowerPCCpuIsaFeature(5);
	/**
	 * Embedded Floating-Point Single Precision instructions.
	 *
	 * These instructions are defined in POWER ISA 2.03 in SPE.Embedded Float Scalar Single category.
	 */
	public static final PowerPCCpuIsaFeature EFPS       = new PowerPCCpuIsaFeature(6);
	/**
	 * Embedded Floating-Point Double Precision instructions.
	 *
	 * These instructions are defined in POWER ISA 2.03 in SPE.Embedded Float Scalar Double category.
	 */
	public static final PowerPCCpuIsaFeature EFPD       = new PowerPCCpuIsaFeature(7);
	/**
	 * ISEL instruction.
	 *
	 * ISEL instruction is defined as optional (Phased-In) in Power ISA 2.03.
	 */
	public static final PowerPCCpuIsaFeature ISEL       = new PowerPCCpuIsaFeature(8);
	/**
	 * POPCNTB instruction.
	 *
	 * POPCNTB instruction is defined as optional (Phased-In) in Power ISA 2.03.
	 */
	public static final PowerPCCpuIsaFeature POPCNTB    = new PowerPCCpuIsaFeature(9);
	/**
	 * FRIN, FRIZ, FRIP, and FRIM instructions.
	 *
	 * Floating-point round-to-integer instructions are defined as optional (Phased-In) in Power ISA 2.03 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature FRI        = new PowerPCCpuIsaFeature(10);
	/**
	 * FPCPSGN and LFIWAX instructions.
	 *
	 * These instruction is defined in Power ISA 2.05 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature FPU205     = new PowerPCCpuIsaFeature(11);
	/**
	 * LFDP, STFDP, LFDPX, and STFDPX instructions.
	 *
	 * Floating-point load/store double pair instructions are defined as optional (Phased-Out) in Power ISA 2.05 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature LFDP       = new PowerPCCpuIsaFeature(12);
	/**
	 * Decimal Floating-Point instructions.
	 *
	 * These instructions are defined in POWER ISA 2.05 in Decimal Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature DFP        = new PowerPCCpuIsaFeature(13);
	/**
	 * CMPB, PRTYW, and PRTYD instructions.
	 *
	 * These instructions are defined in Power ISA 2.05.
	 */
	public static final PowerPCCpuIsaFeature ISA205     = new PowerPCCpuIsaFeature(14);
	/**
	 * BPERMD instruction.
	 *
	 * This instruction is defined as optional (Embedded.Phased-In, Server) in Power ISA 2.06.
	 */
	public static final PowerPCCpuIsaFeature BPERMD     = new PowerPCCpuIsaFeature(15);
	/**
	 * Extended division instructions (DIVWE, DIVWEO, DIVWEU, DIVWEUO, DIVDE, DIVDEO, DIVDEU, and DIVDEUO).
	 *
	 * These instructions are defined as optional (Embedded.Phased-In, Server) in Power ISA 2.06.
	 */
	public static final PowerPCCpuIsaFeature DIVWE      = new PowerPCCpuIsaFeature(16);
	/**
	 * POPCNTW and POPCNTD instructions.
	 *
	 * These instructions are defined as optional (Embedded.Phased-In, Server) in Power ISA 2.06.
	 */
	public static final PowerPCCpuIsaFeature POPCNTW    = new PowerPCCpuIsaFeature(17);
	/**
	 * LDBRX and STDBRX instructions.
	 *
	 * These instructions are defined in Power ISA 2.06.
	 */
	public static final PowerPCCpuIsaFeature ISA206     = new PowerPCCpuIsaFeature(18);
	/**
	 * LFIWZX instruction.
	 *
	 * This instruction is defined as optional (Phased-In) in Power ISA 2.06 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature LFIWZX     = new PowerPCCpuIsaFeature(19);
	/**
	 * FCTIDU, FCTIDUZ, FCTIWU, FCTIWUZ, FCFIDU, FCFIDS, and FCFIDUS instructions.
	 *
	 * These instructions are defined as optional (Phased-In) in Power ISA 2.06 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature FCTIWU     = new PowerPCCpuIsaFeature(20);
	/**
	 * FTDIV and FTSQRT instructions.
	 *
	 * These instructions are defined as optional (Phased-In) in Power ISA 2.06 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature FTDIV      = new PowerPCCpuIsaFeature(21);
	/**
	 * LBARX, LHARX, STBCX, and STHCX instructions.
	 *
	 * These instructions are defined as optional (Phased-In) in Power ISA 2.06 in Floating-Point category.
	 */
	public static final PowerPCCpuIsaFeature LBARX      = new PowerPCCpuIsaFeature(22);
	/**
	 * LQARX and STQCX instructions.
	 *
	 * These instructions are defined in Power ISA 2.07 in Load/Store Quadword category.
	 */
	public static final PowerPCCpuIsaFeature LQARX      = new PowerPCCpuIsaFeature(23);
	/**
	 * LQ and STQ instructions (accessible in problem state).
	 *
	 * LQ and STQ instructions are redefined as accessible in problem state in Power ISA 2.07 in Load/Store Quadword category.
	 */
	public static final PowerPCCpuIsaFeature LQ         = new PowerPCCpuIsaFeature(24);
	/**
	 * VCIPHER, VCIPHERLAST, VNCIPHER, VNCIPHERLAST, VSBOX, VSHASIGMAW, and VSHASIGMAD instructions.
	 *
	 * These instructions are defined in Power ISA 2.07 in VMX.Crypto category.
	 */
	public static final PowerPCCpuIsaFeature VMXCrypto  = new PowerPCCpuIsaFeature(25);
	/**
	 * Transactional Memory instructions.
	 *
	 * These instructions are defined in Power ISA 2.07 in Transactional Memory category.
	 */
	public static final PowerPCCpuIsaFeature TM         = new PowerPCCpuIsaFeature(26);

	protected PowerPCCpuIsaFeature(int id) {
		super(id, CpuArchitecture.PowerPC.getId());
	}

};
