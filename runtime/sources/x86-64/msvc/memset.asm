;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text align=32
global memset
memset:
	MOV rax, rcx

.process_by_1_prologue:
	TEST rcx, 15
	JZ .process_by_32_prologue

	MOV [rcx], dl
	ADD rcx, 1
	SUB r8, 1
	JNZ .process_by_1_prologue

.process_by_32_prologue:
	SUB r8, 32
	JB .process_by_32_epilogue

	MOVZX edx, dl
	IMUL edx, edx, 0x01010101
	MOVD xmm0, edx
	PSHUFD xmm0, xmm0, 0

	align 16
.process_by_32:
	MOVAPS [byte rcx + 0], xmm0
	MOVAPS [byte rcx + 16], xmm0
	ADD rcx, 32
	SUB r8, 32
	JAE .process_by_32

.process_by_32_epilogue:
	ADD r8, 32
	JZ .return

.process_by_1_epilogue:
	MOV [rcx], dl
	ADD rcx, 1
	SUB r8, 1
	JNZ .process_by_1_epilogue

.return:
	RET
