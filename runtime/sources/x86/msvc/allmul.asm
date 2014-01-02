;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text code readable executable align=32

global __allmul
__allmul:
	PUSH ebx
	; Stack frame:
	; - [esp + 0]  = old ebx
	; - [esp + 4]  = return address
	; - [esp + 8]  = A[0:31]
	; - [esp + 12] = A[32:63]
	; - [esp + 16] = B[0:31]
	; - [esp + 20] = B[32:63]
	MOV  ecx, [esp + 8]  ; ecx = A[0:31]
	MOV  eax, [esp + 16] ; eax = B[0:31]
	MOV  ebx, eax        ; ebx = B[0:31]
	MUL  eax             ; edx:eax = A[0:31] * B[0:31]
	IMUL ebx, [esp + 12] ; ebx = B[0:31] * A[32:63]
	IMUL ecx, [esp + 20] ; ecx = A[0:31] * B[32:63]
	ADD  edx, ebx
	POP  ebx
	ADD  edx, ecx
	RET
