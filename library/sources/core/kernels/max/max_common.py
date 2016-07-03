from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.avx_instruction_maps import *
from instruction_maps.sse_instruction_maps import *

def avx_scalar_instruction_select(input_type, output_type):
    SCALAR_MOV = avx_scalar_mov_map[output_type]
    SCALAR_MAX = avx_scalar_max_map[output_type]
    return SCALAR_MOV, SCALAR_MAX

def avx_vector_instruction_select(input_type, output_type):
    SIMD_LOAD = avx_vector_unaligned_mov_map[input_type]
    SIMD_MAX = avx_vector_max_map[output_type]
    SIMD_STORE = avx_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_MAX, SIMD_STORE
