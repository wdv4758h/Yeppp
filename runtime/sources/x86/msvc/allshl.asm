;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text code readable executable align=32

global __allshl
__allshl:
	TEST ecx, 32
	JNZ  .large_shift
	SHLD edx, eax, cl
	SHL  eax, cl
	RET
.large_shift:
	SHL eax, cl
	MOV edx, eax
	XOR eax, eax
	RET
