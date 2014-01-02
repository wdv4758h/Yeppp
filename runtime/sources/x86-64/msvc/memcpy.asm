;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text align=32
global memcpy
memcpy:
	MOV r9, rcx

.process_by_1_prologue:
	TEST rcx, 15
	JZ .process_by_32_prologue

	MOVZX eax, byte [rcx]
	MOV [rdx], al
	ADD rcx, 1
	ADD rdx, 1
	SUB r8, 1
	JNZ .process_by_1_prologue

.process_by_32_prologue:
	SUB r8, 32
	JB .process_by_32_epilogue
	
	align 32
.process_by_32:
	MOVUPS xmm0, [byte rcx]
	MOVUPS xmm1, [byte rcx + 16]
	MOVAPS [byte rdx + 0], xmm0
	MOVAPS [byte rdx + 16], xmm1
	ADD rcx, 32
	ADD rdx, 32
	SUB r8, 32
	JAE .process_by_32

.process_by_32_epilogue:
	ADD r8, 32
	JZ .return

.process_by_1_epilogue:
	MOVZX eax, byte [rsi]
	MOV [rdi], al
	ADD rsi, 1
	ADD rdi, 1
	SUB r8, 1
	JNZ .process_by_1_epilogue

.return:
	MOV rax, r9
	RET
