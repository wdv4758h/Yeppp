;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

%ifidn __OUTPUT_FORMAT__,elf32
	section .text.memcmp align=32
		global memcmp:function internal
		memcmp:
%elifidn __OUTPUT_FORMAT__,win32
	section .text align=32
		global _memcmp
		_memcmp:
%elifidn __OUTPUT_FORMAT__,macho32
	section .text
		global memcmp
		memcmp:
%endif

	PUSH edi
	PUSH esi
	CLD
	MOV esi, [esp + 8 + 4]
	MOV edi, [esp + 8 + 8]
	MOV ecx, [esp + 8 + 12]
	REPE CMPSB
	JNE .return_sign
	XOR eax, eax
	POP esi
	POP edi
	RET

.return_sign:
	MOVZX eax, byte [esi - 1]
	MOVZX ecx, byte [edi - 1]
	CMP eax, ecx
	SETA al
	SETB cl
	SUB al, cl
	MOVSX eax, al
	POP esi
	POP edi
	RET
