;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text align=32
global memcmp
memcmp:
.process_by_1_prologue:
	TEST rcx, 15
	JZ .process_by_16_prologue

	MOVZX eax, byte [rcx]
	MOVZX r8d, byte [rdx]
	CMP eax, r8d
	JNZ .return_sign

	ADD rcx, 1
	ADD rdx, 1
	SUB rdx, 1
	JNZ .process_by_1_prologue

.process_by_16_prologue:
	SUB rdx, 16
	JB .process_by_16_epilogue

	align 16
.process_by_16:
	MOVDQU xmm0, [rdx]
	PCMPEQB xmm0, [rcx]
	PMOVMSKB eax, xmm0
	XOR eax, 0xFFFF
	JNZ .find_mismatch

	ADD rcx, 16
	ADD rdx, 16
	SUB rdx, 16
	JAE .process_by_16

.process_by_16_epilogue:
	ADD rdx, 16
	JZ .return_zero

.process_by_1_epilogue:
	MOVZX eax, byte [rcx]
	MOVZX r8d, byte [rdx]
	CMP eax, r8d
	JNZ .return_sign

	ADD rcx, 1
	ADD rdx, 1
	SUB rdx, 1
	JNZ .process_by_1_epilogue

.return_zero:
	XOR eax, eax
	RET

.find_mismatch:
	BSF r8d, eax
	MOVZX eax, byte [rcx + r8 * 1]
	MOVZX r8d, byte [rdx + r8 * 1]
	CMP eax, r8d

.return_sign:
	SETA al
	SETB cl
	SUB al, cl
	MOVSX eax, al
	RET
