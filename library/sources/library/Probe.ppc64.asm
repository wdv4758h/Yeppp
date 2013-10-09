/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

.macro BEGIN_PPC64_FUNCTION name
	.globl \name
	.section ".opd","aw"
	.align 3
\name:
	.quad .L.\name,.TOC.@tocbase
	.type \name, @function
	.text
.L.\name:
.endm

.macro END_PPC64_FUNCTION name
	.size \name,.-.L.\name
.endm

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFSQRT
	.internal _yepLibrary_ProbeFSQRT
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FSQRT f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFSQRT

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFRES
	.internal _yepLibrary_ProbeFRES
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FRES f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFRES

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFRE
	.internal _yepLibrary_ProbeFRE
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FRE f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFRE

BEGIN_PPC64_FUNCTION _yepLibrary_ProbePOPCNTB
	.internal _yepLibrary_ProbePOPCNTB
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	POPCNTB r3, r3
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbePOPCNTB

BEGIN_PPC64_FUNCTION _yepLibrary_ProbePOPCNTW
	.internal _yepLibrary_ProbePOPCNTW
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	POPCNTW r3, r3
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbePOPCNTW

BEGIN_PPC64_FUNCTION _yepLibrary_ProbePRTYW
	.internal _yepLibrary_ProbePRTYW
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	PRTYW r3, r3
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbePRTYW

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeISEL
	.internal _yepLibrary_ProbeISEL
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	ISELEQ r3, r3, r3
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeISEL

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeBPERMD
	.internal _yepLibrary_ProbeBPERMD
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	BPERMD r3, r3, r3
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeBPERMD

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFRIN
	.internal _yepLibrary_ProbeFRIN
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FRIN f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFRIN

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFCPSGN
	.internal _yepLibrary_ProbeFCPSGN
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FCPSGN f1, f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFCPSGN

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFCTIWU
	.internal _yepLibrary_ProbeFCTIWU
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FCTIWU f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFCTIWU

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeFTDIV
	.internal _yepLibrary_ProbeFTDIV
	.machine "power7"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	FTDIV cr0, f1, f1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeFTDIV

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeDIVWE
	.internal _yepLibrary_ProbeDIVWE
	.machine "power7"
	LI r4, 1
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	DIVWE r4, r4, r4
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeDIVWE

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeVADDUDM
	.internal _yepLibrary_ProbeVADDUDM
	.machine "power8"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	VADDUDM v0, v0, v0
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeVADDUDM

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeVPERMXOR
	.internal _yepLibrary_ProbeVPERMXOR
	.machine "power8"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	VPERMXOR v0, v0, v0, v0
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeVPERMXOR

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeVCIPHER
	.internal _yepLibrary_ProbeVCIPHER
	.machine "power8"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	VCIPHER v0, v0, v0
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeVCIPHER

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeXSADDSP
	.internal _yepLibrary_ProbeXSADDSP
	.machine "power8"
	LI r3, 0
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	XSADDSP vs1, vs1, vs1
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeXSADDSP

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeLFDP
	.internal _yepLibrary_ProbeLFDP
	.machine "power6"
	LI r3, 0
	STDU r1, -112(r1)
	STD r3, 16(r1)
	STD r3, 24(r1)
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	LFDP f2, 16(r1)
	LD r1, 0(r1)
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeLFDP

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeLDBRX
	.internal _yepLibrary_ProbeLDBRX
	.machine "power7"
	LI r3, 0
	STDU r1, -112(r1)
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	LDBRX r0, r0, r1
	LD r1, 0(r1)
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeLDBRX

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeLFIWZX
	.internal _yepLibrary_ProbeLFIWZX
	.machine "power7"
	LI r3, 0
	STDU r1, -112(r1)
	ADDI r4, r1, 8
	STD r3, 8(r1)
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	LFIWZX f1, r0, r4
	LD r1, 0(r1)
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeLFIWZX

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeLBARX
	.internal _yepLibrary_ProbeLBARX
	.machine "power7"
	LI r3, 0
	STDU r1, -112(r1)
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	LBARX r4, 0, r1
	LD r1, 0(r1)
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeLBARX

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeLQARX
	.internal _yepLibrary_ProbeLQARX
	.machine "power8"
	LI r3, 0
	STDU r1, -112(r1)
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	LQARX r4, 0, r1
	LD r1, 0(r1)
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeLQARX

BEGIN_PPC64_FUNCTION _yepLibrary_ProbeLQ
	.internal _yepLibrary_ProbeLQ
	.machine "power8"
	LI r3, 0
	STDU r1, -112(r1)
	# If the next line raises SIGILL, the signal handler will change r3 to 1 and skip the instruction (4 bytes)
	LQ r4, 16(r1)
	LD r1, 0(r1)
	BLR
END_PPC64_FUNCTION _yepLibrary_ProbeLQ

