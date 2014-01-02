;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text code readable executable align=32

; Implementation from AMD Optimization manual
global __aulldiv
__aulldiv:
	PUSH ebx             ; Save EBX as per calling convention.
	MOV  ecx, [esp + 20] ; divisor_hi
	MOV  ebx, [esp + 16] ; divisor_lo
	MOV  edx, [esp + 12] ; dividend_hi
	MOV  eax, [esp + 8]  ; dividend_lo
	TEST ecx, ecx        ; divisor > (2^32 – 1)?
	JNZ  .big_divisor    ; Yes, divisor > 2^32 – 1.
	CMP  edx, ebx        ; Only one division needed (ECX = 0)?
	JAE  .two_divs       ; Need two divisions.
	DIV  ebx             ; EAX = quotient_lo
	MOV  edx, ecx        ; EDX = quotient_hi = 0 (quotient in EDX:EAX)
	POP  ebx             ; Restore EBX as per calling convention.
	RET  16              ; Done, return to caller.

	ALIGN 8
.two_divs:
	MOV  ecx, eax   ; Save dividend_lo in ECX.
	MOV  eax, edx   ; Get dividend_hi.
	XOR  edx, edx   ; Zero-extend it into EDX:EAX.
	DIV  ebx        ; quotient_hi in EAX
	XCHG eax, ecx   ; ECX = quotient_hi, EAX = dividend_lo
	DIV  ebx        ; EAX = quotient_lo
	MOV  edx, ecx   ; EDX = quotient_hi (quotient in EDX:EAX)
	POP  ebx        ; Restore EBX as per calling convention.
	RET  16         ; Done, return to caller.

	ALIGN 8
.big_divisor:
	PUSH edi                  ; Save EDI as per calling convention.
	MOV  edi, ecx             ; Save divisor_hi.
	SHR  edx, 1               ; Shift both divisor and dividend right
	RCR  eax, 1               ;  by 1 bit.
	ROR  edi, 1
	RCR  ebx, 1
	BSR  ecx, ecx             ; ECX = number of remaining shifts
	SHRD ebx, edi, cl         ; Scale down divisor and dividend
	SHRD eax, edx, cl         ;  such that divisor is less than
	SHR  edx, cl              ;  2^32 (that is, it fits in EBX).
	ROL  edi, 1               ; Restore original divisor_hi.
	DIV  ebx                  ; Compute quotient.
	MOV  ebx, [esp + 12]      ; dividend_lo
	MOV  ecx, eax             ; Save quotient.
	IMUL edi, eax             ; quotient * divisor high word (low only)
	MUL  dword [esp + 20]     ; quotient * divisor low word
	ADD  edx, edi             ; EDX:EAX = quotient * divisor
	SUB  ebx, eax             ; dividend_lo – (quot.*divisor)_lo
	MOV  eax, ecx             ; Get quotient.
	MOV  ecx, [esp + 16]      ; dividend_hi
	SBB  ecx, edx             ; Subtract (divisor * quot.) from dividend.
	SBB  eax, 0               ; Adjust quotient if remainder negative.
	XOR  edx, edx             ; Clear high word of quot. (EAX<=FFFFFFFFh).
	POP  edi                  ; Restore EDI as per calling convention.
	POP  ebx                  ; Restore EBX as per calling convention.
	RET  16                   ; Done, return to caller.
