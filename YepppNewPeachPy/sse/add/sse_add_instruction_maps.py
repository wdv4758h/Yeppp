from peachpy.x86_64 import *
from peachpy import *
from peachpy.c.types import *

packed_add_map = {
    Yep8s : PADDB,
    Yep8u : PADDB,
    Yep16s: PADDW,
    Yep16u: PADDW,
    Yep32s: PADDD,
    Yep32u: PADDD,
    Yep64s: PADDQ,
    Yep64u: PADDQ,
    Yep32f: ADDPS,
    Yep64f: ADDPD
}

scalar_add_map = {
    Yep8s : ADD,
    Yep8u : ADD,
    Yep16s: ADD,
    Yep16u: ADD,
    Yep32s: ADD,
    Yep32u: ADD,
    Yep64s: ADD,
    Yep64u: ADD,
    Yep32f: ADDSS,
    Yep64f: ADDSD
}

packed_aligned_move_map = {
    Yep8s       : MOVDQA,
    Yep8u       : MOVDQA,
    Yep16s      : MOVDQA,
    Yep16u      : MOVDQA,
    Yep32s      : MOVDQA,
    Yep32u      : MOVDQA,
    Yep64s      : MOVDQA,
    Yep64u      : MOVDQA,
    Yep32f      : MOVAPS,
    Yep64f      : MOVAPD,
}

packed_unaligned_move_map = {
    Yep8s : MOVDQU,
    Yep8u : MOVDQU,
    Yep16s: MOVDQU,
    Yep16u: MOVDQU,
    Yep32s: MOVDQU,
    Yep64s: MOVDQU,
    Yep32f: MOVUPS,
    Yep64f: MOVUPD
}

packed_movsx_map = {
    (Yep8s, Yep16s) : PMOVSXBW,
    (Yep8u, Yep16u) : PMOVZXBW,
    (Yep16s, Yep32s): PMOVSXWD,
    (Yep16u, Yep32u): PMOVZXWD,
    (Yep32s, Yep64s): PMOVSXDQ,
    (Yep32u, Yep64u): PMOVZXDQ
}

scalar_move_map = {
    Yep8s       : MOV,
    Yep8u       : MOV,
    Yep16s      : MOV,
    Yep16u      : MOV,
    Yep32s      : MOV,
    Yep32u      : MOV,
    Yep64s      : MOV,
    Yep64u      : MOV,
    Yep32f      : MOVSS,
    Yep64f      : MOVSD
}

scalar_register_map = {
    Yep8s       : GeneralPurposeRegister8,
    Yep8u       : GeneralPurposeRegister8,
    Yep16s      : GeneralPurposeRegister16,
    Yep16u      : GeneralPurposeRegister16,
    Yep32s      : GeneralPurposeRegister32,
    Yep32u      : GeneralPurposeRegister32,
    Yep64s      : GeneralPurposeRegister64,
    Yep64u      : GeneralPurposeRegister64,
    Yep32f      : XMMRegister,
    Yep64f      : XMMRegister
}
