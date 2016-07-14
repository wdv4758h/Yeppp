from peachpy.x86_64 import *
from peachpy import *
from peachpy.c.types import *

# =================================================
# ADDITION
# =================================================
sse_vector_add_map = {
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

sse_scalar_add_map = {
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

# =================================================
# SUBTRACTION
# =================================================
sse_vector_sub_map = {
    Yep8s : PSUBB,
    Yep8u : PSUBB,
    Yep16s: PSUBW,
    Yep16u: PSUBW,
    Yep32s: PSUBD,
    Yep32u: PSUBD,
    Yep64s: PSUBQ,
    Yep64u: PSUBQ,
    Yep32f: SUBPS,
    Yep64f: SUBPD
}

sse_scalar_sub_map = {
    Yep8s : SUB,
    Yep8u : SUB,
    Yep16s: SUB,
    Yep16u: SUB,
    Yep32s: SUB,
    Yep32u: SUB,
    Yep64s: SUB,
    Yep64u: SUB,
    Yep32f: SUBSS,
    Yep64f: SUBSD
}

# =================================================
# MOV
# =================================================
sse_vector_aligned_mov_map = {
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

sse_vector_unaligned_mov_map = {
    Yep8s : MOVDQU,
    Yep8u : MOVDQU,
    Yep16s: MOVDQU,
    Yep16u: MOVDQU,
    Yep32s: MOVDQU,
    Yep64s: MOVDQU,
    Yep32f: MOVUPS,
    Yep64f: MOVUPD
}

sse_vector_movsx_map = {
    (Yep8s, Yep16s) : PMOVSXBW,
    (Yep8u, Yep16u) : PMOVZXBW,
    (Yep16s, Yep32s): PMOVSXWD,
    (Yep16u, Yep32u): PMOVZXWD,
    (Yep32s, Yep64s): PMOVSXDQ,
    (Yep32u, Yep64u): PMOVZXDQ
}

sse_scalar_mov_map = {
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

sse_scalar_movsx_map = {
    (Yep8s, Yep16s) : MOVSX,
    (Yep8u, Yep16u) : MOVZX,
    (Yep16s, Yep32s): MOVSX,
    (Yep16u, Yep32u): MOVZX,
    (Yep32s, Yep64s): MOVSXD,
    (Yep32u, Yep64u): MOV
}

sse_scalar_max_map = {
    
}

sse_vector_max_map = {

}

sse_scalar_min_map = {

}

sse_vector_min_map = {

}

# =================================================
# REGS
# =================================================
sse_scalar_register_map = {
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
