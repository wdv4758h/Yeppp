from peachpy.x86_64 import *
from peachpy import *
from peachpy.c.types import *

# =================================================
# ADDITION
# =================================================
avx_vector_add_map = {
    Yep8s : VPADDB,
    Yep8u : VPADDB,
    Yep16s: VPADDW,
    Yep16u: VPADDW,
    Yep32s: VPADDD,
    Yep32u: VPADDD,
    Yep64s: VPADDQ,
    Yep64u: VPADDQ,
    Yep32f: VADDPS,
    Yep64f: VADDPD
}

avx_scalar_add_map = {
    Yep8s : ADD,
    Yep8u : ADD,
    Yep16s: ADD,
    Yep16u: ADD,
    Yep32s: ADD,
    Yep32u: ADD,
    Yep64s: ADD,
    Yep64u: ADD,
    Yep32f: VADDSS,
    Yep64f: VADDSD
}

# =================================================
# SUBTRACTION
# =================================================
avx_vector_sub_map = {
    Yep8s : VPSUBB,
    Yep8u : VPSUBB,
    Yep16s: VPSUBW,
    Yep16u: VPSUBW,
    Yep32s: VPSUBD,
    Yep32u: VPSUBD,
    Yep64s: VPSUBQ,
    Yep64u: VPSUBQ,
    Yep32f: VSUBPS,
    Yep64f: VSUBPD
}

avx_scalar_sub_map = {
    Yep8s : SUB,
    Yep8u : SUB,
    Yep16s: SUB,
    Yep16u: SUB,
    Yep32s: SUB,
    Yep32u: SUB,
    Yep64s: SUB,
    Yep64u: SUB,
    Yep32f: VSUBSS,
    Yep64f: VSUBSD
}

# =================================================
# MULTIPLICATION
# =================================================
avx_vector_mult_low_map = {
    Yep16s      : VPMULLW,
    Yep16u      : VPMULLW,
    Yep32s      : VPMULLD,
    Yep32u      : VPMULLD
}

avx_vector_mult_high_map = {
    Yep16s      : VPMULHW,
    Yep16u      : VPMULHUW
}

avx_vector_multiply_map = {
    Yep32f      : VMULPS,
    Yep64f      : VMULPD
}

avx_scalar_multiply_map = {
    Yep8s       : IMUL,
    Yep8u       : IMUL,
    Yep16s      : IMUL,
    Yep16u      : IMUL,
    Yep32s      : IMUL,
    Yep32u      : IMUL,
    Yep64s      : IMUL,
    Yep64u      : IMUL,
    Yep32f      : VMULSS,
    Yep64f      : VMULSD
}

# =================================================
# MAXIMUM/MINIMUM
# =================================================
avx_vector_max_map = {
    Yep8s       : VPMAXSB,
    Yep8u       : VPMAXUB,
    Yep16s      : VPMAXSW,
    Yep16u      : VPMAXUW,
    Yep32s      : VPMAXSD,
    Yep32u      : VPMAXUD,
    Yep64s      : VPMAXSQ,
    Yep64u      : VPMAXUQ,
    Yep32f      : VMAXPS,
    Yep64f      : VMAXPD
}

avx_scalar_max_map = {
    Yep8s       : None,
    Yep8u       : None,
    Yep16s      : None,
    Yep16u      : None,
    Yep32s      : None,
    Yep32u      : None,
    Yep64s      : None,
    Yep64u      : None,
    Yep32f      : VMAXSS,
    Yep64f      : VMAXSD
}

avx_vector_min_map = {
    Yep8s       : VPMINSB,
    Yep8u       : VPMINUB,
    Yep16s      : VPMINSW,
    Yep16u      : VPMINUW,
    Yep32s      : VPMINSD,
    Yep32u      : VPMINUD,
    Yep64s      : VPMINSQ,
    Yep64u      : VPMINUQ,
    Yep32f      : VMINPS,
    Yep64f      : VMINPD
}

avx_scalar_min_map = {
    Yep8s       : None,
    Yep8u       : None,
    Yep16s      : None,
    Yep16u      : None,
    Yep32s      : None,
    Yep32u      : None,
    Yep64s      : None,
    Yep64u      : None,
    Yep32f      : VMINSS,
    Yep64f      : VMINSD
}
# =================================================
# UNPACK
# =================================================
avx_high_unpack_map = {
    (Yep8s, Yep16s) : VPUNPCKHBW,
    (Yep8u, Yep16u) : VPUNPCKHBW,
    (Yep16s, Yep32s): VPUNPCKHWD,
    (Yep16u, Yep32u): VPUNPCKHWD,
    (Yep32s, Yep64s): VPUNPCKHDQ,
    (Yep32u, Yep64u): VPUNPCKHDQ
}

avx_low_unpack_map = {
    (Yep8s, Yep16s) : VPUNPCKLBW,
    (Yep8u, Yep16u) : VPUNPCKLBW,
    (Yep16s, Yep32s): VPUNPCKLWD,
    (Yep16u, Yep32u): VPUNPCKLWD,
    (Yep32s, Yep64s): VPUNPCKLDQ,
    (Yep32u, Yep64u): VPUNPCKLDQ
}

# =================================================
# MOV
# =================================================
avx_vector_aligned_mov_map = {
    Yep8s       : VMOVDQA,
    Yep8u       : VMOVDQA,
    Yep16s      : VMOVDQA,
    Yep16u      : VMOVDQA,
    Yep32s      : VMOVDQA,
    Yep32u      : VMOVDQA,
    Yep64s      : VMOVDQA,
    Yep64u      : VMOVDQA,
    Yep32f      : VMOVAPS,
    Yep64f      : VMOVAPD,
}

avx_vector_unaligned_mov_map = {
    Yep8s : VMOVDQU,
    Yep8u : VMOVDQU,
    Yep16s: VMOVDQU,
    Yep16u: VMOVDQU,
    Yep32s: VMOVDQU,
    Yep64s: VMOVDQU,
    Yep32f: VMOVUPS,
    Yep64f: VMOVUPD
}

avx_vector_movsx_map = {
    (Yep8s, Yep16s) : VPMOVSXBW,
    (Yep8u, Yep16u) : VPMOVZXBW,
    (Yep16s, Yep32s): VPMOVSXWD,
    (Yep16u, Yep32u): VPMOVZXWD,
    (Yep32s, Yep64s): VPMOVSXDQ,
    (Yep32u, Yep64u): VPMOVZXDQ
}

avx_scalar_mov_map = {
    Yep8s       : MOV,
    Yep8u       : MOV,
    Yep16s      : MOV,
    Yep16u      : MOV,
    Yep32s      : MOV,
    Yep32u      : MOV,
    Yep64s      : MOV,
    Yep64u      : MOV,
    Yep32f      : VMOVSS,
    Yep64f      : VMOVSD
}

avx_scalar_movsx_map = {
    (Yep8s, Yep16s) : MOVSX,
    (Yep8u, Yep16u) : MOVZX,
    (Yep16s, Yep32s): MOVSX,
    (Yep16u, Yep32u): MOVZX,
    (Yep32s, Yep64s): MOVSXD,
    (Yep32u, Yep64u): MOV
}

avx_scalar_reg_to_vector_reg_mov_map = {
    Yep8s   : VMOVD,
    Yep8u   : VMOVD,
    Yep16s  : VMOVD,
    Yep16u  : VMOVD,
    Yep32s  : VMOVD,
    Yep32u  : VMOVD,
    Yep64s  : VMOVQ,
    Yep64u  : VMOVQ,
    Yep32f  : None,
    Yep64f  : None
}

# =================================================
# BROADCAST
# =================================================
avx_broadcast_map = {
    Yep8s   : VPBROADCASTB,
    Yep8u   : VPBROADCASTB,
    Yep16s  : VPBROADCASTW,
    Yep16u  : VPBROADCASTW,
    Yep32s  : VPBROADCASTD,
    Yep32u  : VPBROADCASTD,
    Yep64s  : VPBROADCASTQ,
    Yep64u  : VPBROADCASTQ,
    Yep32f  : VBROADCASTSS,
    Yep64f  : VBROADCASTSD
}

# =================================================
# REGS
# =================================================
avx_scalar_register_map = {
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
