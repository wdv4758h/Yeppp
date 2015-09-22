from peachpy.x86_64 import *
from peachpy import *
from peachpy.c.types import *

packed_add_map = {
    const_Yep8s : VPADDB,
    const_Yep8u : VPADDB,
    const_Yep16s: VPADDW,
    const_Yep16u: VPADDW,
    const_Yep32s: VPADDD,
    const_Yep32u: VPADDD,
    const_Yep64s: VPADDQ,
    const_Yep64u: VPADDQ,
    const_Yep32f: VADDPS,
    const_Yep64f: VADDPD
}

scalar_add_map = {
    const_Yep8s : ADD,
    const_Yep8u : ADD,
    Yep16s      : ADD,
    const_Yep16s: ADD,
    Yep16u      : ADD,
    const_Yep16u: ADD,
    Yep32s      : ADD,
    const_Yep32s: ADD,
    Yep32u      : ADD,
    const_Yep32u: ADD,
    Yep64s      : ADD,
    const_Yep64s: ADD,
    Yep64u      : ADD,
    const_Yep64u: ADD,
    Yep32f: VADDSS,
    Yep64f: VADDSD
}

packed_aligned_move_map = {
    Yep8s       : VMOVDQA,
    const_Yep8s : VMOVDQA,
    Yep8u       : VMOVDQA,
    const_Yep8u : VMOVDQA,
    Yep16s      : VMOVDQA,
    const_Yep16s: VMOVDQA,
    Yep16u      : VMOVDQA,
    const_Yep16u: VMOVDQA,
    Yep32s      : VMOVDQA,
    const_Yep32s: VMOVDQA,
    Yep32u      : VMOVDQA,
    const_Yep32u: VMOVDQA,
    Yep64s      : VMOVDQA,
    const_Yep64s: VMOVDQA,
    Yep64u      : VMOVDQA,
    const_Yep64u: VMOVDQA,
    Yep32f      : VMOVAPS,
    const_Yep32f: VMOVAPS,
    Yep64f      : VMOVAPD,
}

packed_unaligned_move_map = {
    const_Yep8s : VMOVDQU,
    const_Yep8u : VMOVDQU,
    const_Yep16s: VMOVDQU,
    const_Yep16u: VMOVDQU,
    const_Yep32s: VMOVDQU,
    const_Yep64s: VMOVDQU,
    const_Yep32f: VMOVUPS,
    const_Yep64f: VMOVUPD
}

packed_movsx_map = {
    (const_Yep8s, Yep16s) : VPMOVSXBW,
    (const_Yep8u, Yep16u) : VPMOVZXBW,
    (const_Yep16s, Yep32s): VPMOVSXWD,
    (const_Yep16u, Yep32u): VPMOVZXWD,
    (const_Yep32s, Yep64s): VPMOVSXDQ,
    (const_Yep32u, Yep64u): VPMOVZXDQ
}

scalar_move_map = {
    Yep8s       : MOV,
    const_Yep8s : MOV,
    Yep8u       : MOV,
    const_Yep8u : MOV,
    Yep16s      : MOV,
    const_Yep16s: MOV,
    Yep16u      : MOV,
    const_Yep16u: MOV,
    Yep32s      : MOV,
    const_Yep32s: MOV,
    Yep32u      : MOV,
    const_Yep32u: MOV,
    Yep64s      : MOV,
    const_Yep64s: MOV,
    Yep64u      : MOV,
    const_Yep64u: MOV,
    Yep32f      : VMOVSS,
    const_Yep32f: VMOVSS,
    Yep64f      : VMOVSD
}

scalar_register_map = {
    Yep8s       : GeneralPurposeRegister8,
    const_Yep8s : GeneralPurposeRegister8,
    Yep8u       : GeneralPurposeRegister8,
    const_Yep8u : GeneralPurposeRegister8,
    Yep16s      : GeneralPurposeRegister16,
    const_Yep16s: GeneralPurposeRegister16,
    Yep16u      : GeneralPurposeRegister16,
    const_Yep16u: GeneralPurposeRegister16,
    Yep32s      : GeneralPurposeRegister32,
    const_Yep32s: GeneralPurposeRegister32,
    Yep32u      : GeneralPurposeRegister32,
    const_Yep32u: GeneralPurposeRegister32,
    Yep64s      : GeneralPurposeRegister64,
    const_Yep64s: GeneralPurposeRegister64,
    Yep64u      : GeneralPurposeRegister64,
    const_Yep64u: GeneralPurposeRegister64,
    const_Yep32f: XMMRegister,
    Yep64f      : XMMRegister
}
