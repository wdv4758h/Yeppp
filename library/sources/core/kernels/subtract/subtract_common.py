from instruction_maps.avx_instruction_maps import * # The correct instructions to use depending on argument type
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
    # use the generic sub instruction
    if output_type in [Yep8s, Yep8u, Yep16s, Yep16u, Yep32s, Yep32u,
            Yep64s, Yep64u]:
        SCALAR_SUB = lambda x, y, z: avx_scalar_sub_map[output_type](x, z) \
            if x == y else avx_scalar_sub_map[output_type](x, y)
    else:
        SCALAR_SUB = lambda x, y, z: avx_scalar_sub_map[output_type](x, y, z)

    SCALAR_STORE = avx_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_SUB, SCALAR_STORE

def avx_vector_instruction_select(input_type, output_type):
    if input_type.size == output_type.size:
        SIMD_LOAD = avx_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = avx_vector_movsx_map[(input_type, output_type)]

    SIMD_SUB = avx_vector_sub_map[output_type]
    SIMD_STORE = avx_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_SUB, SIMD_STORE

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
    # use the generic sub instruction
    SCALAR_SUB = lambda x, y, z: sse_scalar_sub_map[output_type](x, z) \
        if x == y else sse_scalar_sub_map[output_type](x, y)

    SCALAR_STORE = sse_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_SUB, SCALAR_STORE

def sse_vector_instruction_select(input_type, output_type):
    if input_type.size == output_type.size:
        SIMD_LOAD = sse_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = sse_vector_movsx_map[(input_type, output_type)]

    SIMD_SUB = lambda x, y, z: sse_vector_sub_map[output_type](x, z) \
        if x == y else sse_vector_sub_map[output_type](x, y)
    SIMD_STORE = sse_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_SUB, SIMD_STORE
