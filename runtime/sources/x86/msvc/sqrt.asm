;
;               Yeppp! library runtime infrastructure
;
; This file is part of Yeppp! library and licensed under MIT license.
; See runtime/LICENSE.txt for details.
;
;

section .text code readable executable align=32

global _sqrt
_sqrt:
	fld QWORD PTR [esp + 4]
	fsqrt
	ret

