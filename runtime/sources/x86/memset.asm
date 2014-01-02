;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

%ifidn __OUTPUT_FORMAT__,elf32
	section .text.memset align=32
		global memset:function internal
		memset:
%elifidn __OUTPUT_FORMAT__,win32
	section .text align=32
		global _memset
		_memset:
%elifidn __OUTPUT_FORMAT__,macho32
	section .text
		global memset
		memset:
%endif

	PUSH edi
	PUSH esi
	CLD
	MOV edi, [esp + 8 + 4]
	MOV eax, [esp + 8 + 8]
	MOV ecx, [esp + 8 + 12]
	MOV edx, edi
	REP STOSB
	MOV eax, edx
	POP esi
	POP edi
	RET
