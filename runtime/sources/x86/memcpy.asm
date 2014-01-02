;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

%ifidn __OUTPUT_FORMAT__,elf32
	section .text.memcpy align=32
		global memcpy:function internal
		memcpy:
%elifidn __OUTPUT_FORMAT__,win32
	section .text align=32
		global _memcpy
		_memcpy:
%elifidn __OUTPUT_FORMAT__,macho32
	section .text
		global memcpy
		memcpy:
%endif

	PUSH edi
	PUSH esi
	CLD
	MOV edi, [esp + 8 + 4]
	MOV esi, [esp + 8 + 8]
	MOV ecx, [esp + 8 + 12]
	MOV eax, edi
	REP MOVSB
	POP esi
	POP edi
	RET
