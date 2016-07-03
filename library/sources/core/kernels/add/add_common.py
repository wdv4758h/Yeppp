from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.avx_instruction_maps import *
from instruction_maps.sse_instruction_maps import *

def avx_scalar_instruction_select(input_type, output_type):
    # Choose the scalar load instruction.
    # The special case is 32u -> 64u, as there is no zero-extension
    # instruction, we have to cast the register from 64 bit to 32 bit.
    if input_type == Yep32u and output_type == Yep64u:
        SCALAR_LOAD = lambda x, y: MOV(x.as_dword, y)
    elif input_type.size == output_type.size:
        SCALAR_LOAD = avx_scalar_mov_map[input_type]
    else:
        SCALAR_LOAD = avx_scalar_movsx_map[(input_type, output_type)]

    # We don't want to have to worry about the order of operands if we
    # use the generic add instruction
    if output_type in [Yep8s, Yep8u, Yep16s, Yep16u, Yep32s, Yep32u,
            Yep64s, Yep64u]:
        SCALAR_ADD = lambda x, y, z: avx_scalar_add_map[output_type](x, z) \
            if x == y else avx_scalar_add_map[output_type](x, y)
    else:
        SCALAR_ADD = lambda x, y, z: avx_scalar_add_map[output_type](x, y, z)

    SCALAR_STORE = avx_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE

def avx_vector_instruction_select(input_type, output_type):
    if input_type.size == output_type.size:
        SIMD_LOAD = avx_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = avx_vector_movsx_map[(input_type, output_type)]

    SIMD_ADD = avx_vector_add_map[output_type]
    SIMD_STORE = avx_vector_aligned_mov_map[output_type]

    if input_type.size != output_type.size:
        UNPACK = avx_high_unpack_map[(input_type, output_type)]
    else:
        UNPACK = None
    return SIMD_LOAD, SIMD_ADD, SIMD_STORE, UNPACK

def AVX_MOV_GPR_TO_VECTOR(vector_reg, gpr, input_type, output_type):
    if input_type == Yep32f:
        VMOVSS(vector_reg.as_xmm, gpr, gpr)
    elif input_type == Yep64f:
        VMOVSD(vector_reg.as_xmm, gpr, gpr)
    else:
        GPR_TO_VECTOR_MOV = avx_scalar_reg_to_vector_reg_mov_map[output_type]
        if input_type.size < 4:
            GPR_TO_VECTOR_MOV(vector_reg.as_xmm, gpr.as_dword)
        else:
            GPR_TO_VECTOR_MOV(vector_reg.as_xmm, gpr)
    BROADCAST = avx_broadcast_map[output_type]
    BROADCAST(vector_reg, vector_reg.as_xmm)

def sse_scalar_instruction_select(input_type, output_type):
    # Choose the scalar load instruction.
    # The special case is 32u -> 64u, as there is no zero-extension
    # instruction, we have to cast the register from 64 bit to 32 bit.
    if input_type == Yep32u and output_type == Yep64u:
        SCALAR_LOAD = lambda x, y: MOV(x.as_dword, y)
    elif input_type.size == output_type.size:
        SCALAR_LOAD = sse_scalar_mov_map[input_type]
    else:
        SCALAR_LOAD = sse_scalar_movsx_map[(input_type, output_type)]

    # We don't want to have to worry about the order of operands if we
    # use the generic add instruction
    SCALAR_ADD = lambda x, y, z: sse_scalar_add_map[output_type](x, z) \
        if x == y else sse_scalar_add_map[output_type](x, y)

    SCALAR_STORE = sse_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE

def sse_vector_instruction_select(input_type, output_type):
    if input_type.size == output_type.size:
        SIMD_LOAD = sse_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = sse_vector_movsx_map[(input_type, output_type)]

    SIMD_ADD = lambda x, y, z: sse_vector_add_map[output_type](x, z) \
        if x == y else sse_vector_add_map[output_type](x, y)
    SIMD_STORE = sse_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_ADD, SIMD_STORE

def SSE_MOV_GPR_TO_VECTOR(vector_reg, gpr, input_type, output_type):
    if input_type == Yep32f:
        PSHUFD(vector_reg, gpr, 0x0)
    elif input_type == Yep64f:
        assert vector_reg == gpr
        PUNPCKLQDQ(vector_reg, gpr) # In this case, vector_reg == gpr
    elif output_type.size <= 4:
        if output_type.size < 4:
            MOVZX(gpr.as_dword, gpr)
        if output_type.size == 1:
            IMUL(gpr.as_dword, gpr.as_dword, 0x01010101)
        elif output_type.size == 2:
            IMUL(gpr.as_dword, gpr.as_dword, 0x00010001)
        MOVD(vector_reg, gpr.as_dword)
        PSHUFD(vector_reg, vector_reg, 0x0)
    elif output_type.size == 8:
        MOVQ(vector_reg, gpr)
        PUNPCKLQDQ(vector_reg, vector_reg)

