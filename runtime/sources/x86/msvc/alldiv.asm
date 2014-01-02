;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text code readable executable align=32

; Implementation from AMD Optimization manual
global __alldiv
__alldiv:
	PUSH ebx    ; Save EBX as per calling convention.
	PUSH esi    ; Save ESI as per calling convention.
	PUSH edi    ; Save EDI as per calling convention.
	MOV  ecx, [esp + 28] ; divisor_hi
	MOV  ebx, [esp + 24] ; divisor_lo
	MOV  edx, [esp + 20] ; dividend_hi
	MOV  eax, [esp + 16] ; dividend_lo
	MOV  esi, ecx        ; divisor_hi
	XOR  esi, edx        ; divisor_hi ^ dividend_hi 
	SAR  esi, 31         ; (quotient < 0) ? -1 : 0
	MOV  edi, edx        ; dividend_hi
	SAR  edi, 31         ; (dividend < 0) ? -1 : 0
	XOR  eax, edi        ; If (dividend < 0),
	XOR  edx, edi        ;  compute 1s complement of dividend.
	SUB  eax, edi        ; If (dividend < 0),
	SBB  edx, edi        ;  compute 2s complement of dividend.
	MOV  edi, ecx        ; divisor_hi
	SAR  edi, 31         ; (divisor < 0) ? -1 : 0
	XOR  ebx, edi        ; If (divisor < 0),
	XOR  ecx, edi        ;  compute 1s complement of divisor.
	SUB  ebx, edi        ; If (divisor < 0),
	SBB  ecx, edi        ;  compute 2s complement of divisor.
	JNZ  .big_divisor    ; divisor > 2^32 - 1
	CMP  edx, ebx        ; Only one division needed (ECX = 0)?
	JAE  .two_divs       ; Need two divisions.
	DIV  ebx             ; EAX = quotient_lo
	MOV  edx, ecx        ; EDX = quotient_hi = 0 (quotient in EDX:EAX)
	XOR  eax, esi        ; If (quotient < 0),
	XOR  edx, esi        ;  compute 1s complement of result.
	SUB  eax, esi        ; If (quotient < 0),
	SBB  edx, esi        ;  compute 2s complement of result.
	POP  edi             ; Restore EDI as per calling convention.
	POP  esi             ; Restore ESI as per calling convention.
	POP  ebx             ; Restore EBX as per calling convention.
	RET  16              ; Done, return to caller.

	ALIGN 8
.two_divs:
	MOV  ecx, eax     ; Save dividend_lo in ECX.
	MOV  eax, edx     ; Get dividend_hi.
	XOR  edx, edx     ; Zero-extend it into EDX:EAX.
	DIV  ebx          ; quotient_hi in EAX
	XCHG eax, ecx     ; ECX = quotient_hi, EAX = dividend_lo
	DIV  ebx          ; EAX = quotient_lo
	MOV  edx, ecx     ; EDX = quotient_hi (quotient in EDX:EAX)

	; Make quotient signed.
	XOR  eax, esi            ; If (quotient < 0),
	XOR  edx, esi            ;  compute 1s complement of result.
	SUB  eax, esi            ; If (quotient < 0),
	SBB  edx, esi            ;  compute 2s complement of result.
	POP  edi                 ; Restore EDI as per calling convention.
	POP  esi                 ; Restore ESI as per calling convention.
	POP  ebx                 ; Restore EBX as per calling convention.
	RET  16                  ; Done, return to caller.

	ALIGN 8
.big_divisor:
	SUB  esp, 12             ; Create three local variables.
	MOV  [esp], eax          ; dividend_lo
	MOV  [esp + 4], ebx      ; divisor_lo
	MOV  [esp + 8], edx      ; dividend_hi
	MOV  edi, ecx            ; Save divisor_hi.
	SHR  edx, 1              ; Shift both
	RCR  eax, 1              ;  divisor and
	ROR  edi, 1              ;  and dividend
	RCR  ebx, 1              ;  right by 1 bit.
	BSR  ecx, ecx            ; ECX = number of remaining shifts
	SHRD ebx, edi, cl        ; Scale down divisor and
	SHRD eax, edx, cl        ;  dividend such that divisor is
	SHR  edx, cl             ;  less than 2^32 (that is, fits in EBX).
	ROL  edi, 1              ; Restore original divisor_hi.
	DIV  ebx                 ; Compute quotient.
	MOV  ebx, [esp]          ; dividend_lo
	MOV  ecx, eax            ; Save quotient.
	IMUL edi, eax            ; quotient * divisor high word (low only)
	MUL  dword [esp + 4]     ; quotient * divisor low word
	ADD  edx, edi            ; EDX:EAX = quotient * divisor
	SUB  ebx, eax            ; dividend_lo - (quot.*divisor)_lo
	MOV  eax, ecx            ; Get quotient.
	MOV  ecx, [esp + 8]      ; dividend_hi
	SBB  ecx, edx            ; Subtract (divisor * quot.) from dividend
	SBB  eax, 0              ; Adjust quotient if remainder is negative.
	XOR  edx, edx            ; Clear high word of quotient.
	ADD  esp, 12             ; Remove local variables.

	; Make quotient signed.
	XOR  eax, esi            ; If (quotient < 0),
	XOR  edx, esi            ;  compute 1s complement of result.
	SUB  eax, esi            ; If (quotient < 0),
	SBB  edx, esi            ;  compute 2s complement of result.
	POP  edi                 ; Restore EDI as per calling convention.
	POP  esi                 ; Restore ESI as per calling convention.
	POP  ebx                 ; Restore EBX as per calling convention.
	RET  16                  ; Done, return to caller.
