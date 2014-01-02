;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text code readable executable align=32

; ControlWord = (PrecisionControl << 8) + (RoundingControl << 10)
; PrecisionControl:
;  * 0b00 - single precision (24 bits)
;  * 0b01 - reserved
;  * 0b10 - double precision (53 bits)
;  * 0b11 - double extended precision (64 bits)
; RoundingControl:
;  * 0b00 - round to nearest (even)
;  * 0b01 - round down (toward -inf)
;  * 0b10 - round up (toward +inf)
;  * 0b11 - round toward zero (truncate)

global _ftol2
global _ftol2_sse
_ftol2:
_ftol2_sse:
	; Control word: double precision + round toward zero
	FLD   QWORD PTR [esp + 4]
	PUSH  DWORD PTR 111000000000b
	FSTCW WORD PTR [esp + 2]
	FLDCW WORD PTR [esp]
	SUB   esp, 4
	FISTP DWORD PTR [esp]
	FLDCW WORD PTR [esp + 6]
	POP   eax
	RET   4
