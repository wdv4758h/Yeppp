from peachpy.x86_64 import *
from peachpy import *
from instruction_maps.avx_instruction_maps import *
from instruction_maps.sse_instruction_maps import *

def avx2_scalar_instruction_select(input_type, output_type, op):
    if input_type == Yep32u and output_type == Yep64u:
        SCALAR_LOAD = lambda x, y: MOV(x.as_dword, y)
    elif input_type.size == output_type.size:
        SCALAR_LOAD = avx_scalar_mov_map[input_type]
    else:
        SCALAR_LOAD = avx_scalar_movsx_map[(input_type, output_type)]

    op_map = { "add"      : avx_scalar_add_map,
               "subtract" : avx_scalar_sub_map,
               "max"      : avx_scalar_max_map,
               "min"      : avx_scalar_min_map }[op]

    if output_type in [Yep8s, Yep8u, Yep16s, Yep16u, Yep32s, Yep32u,
            Yep64s, Yep64u]:
        SCALAR_OP = lambda x, y, z: op_map[output_type](x, z) \
            if x == y else op_map[output_type](x, y)
    else:
        SCALAR_OP = lambda x, y, z: op_map[output_type](x, y, z)

    SCALAR_STORE = avx_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_OP, SCALAR_STORE


def avx2_vector_instruction_select(input_type, output_type, op):
    if input_type.size == output_type.size:
        SIMD_LOAD = avx_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = avx_vector_movsx_map[(input_type, output_type)]

    op_map = { "add"      : avx_vector_add_map,
               "subtract" : avx_vector_sub_map,
               "max"      : avx_vector_max_map,
               "min"      : avx_vector_min_map }[op]

    SIMD_OP = op_map[output_type]
    SIMD_STORE = avx_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_OP, SIMD_STORE


def sse_scalar_instruction_select(input_type, output_type, op):
    if input_type == Yep32u and output_type == Yep64u:
        SCALAR_LOAD = lambda x, y: MOV(x.as_dword, y)
    elif input_type.size == output_type.size:
        SCALAR_LOAD = sse_scalar_mov_map[input_type]
    else:
        SCALAR_LOAD = sse_scalar_movsx_map[(input_type, output_type)]

    op_map = { "add"      : sse_scalar_add_map,
               "subtract" : sse_scalar_sub_map,
               "max"      : sse_scalar_max_map,
               "min"      : sse_scalar_min_map }[op]

    SCALAR_OP = lambda x, y, z: op_map[output_type](x, z) \
        if x == y else op_map[output_type](x, y)

    SCALAR_STORE = sse_scalar_mov_map[output_type]
    return SCALAR_LOAD, SCALAR_OP, SCALAR_STORE


def sse_vector_instruction_select(input_type, output_type, op):
    if input_type.size == output_type.size:
        SIMD_LOAD = sse_vector_unaligned_mov_map[input_type]
    else:
        SIMD_LOAD = sse_vector_movsx_map[(input_type, output_type)]

    op_map = { "add"      : sse_vector_add_map,
               "subtract" : sse_vector_sub_map,
               "max"      : sse_vector_max_map,
               "min"      : sse_vector_min_map }[op]

    SIMD_OP = lambda x, y, z: op_map[output_type](x, z) \
        if x == y else op_map[output_type](x, y)

    SIMD_STORE = sse_vector_aligned_mov_map[output_type]
    return SIMD_LOAD, SIMD_OP, SIMD_STORE


def scalar_instruction_select(input_type, output_type, op, isa_ext):
    if isa_ext == "AVX2":
        return avx2_scalar_instruction_select(input_type, output_type, op)
    elif isa_ext == "SSE":
        return sse_scalar_instruction_select(input_type, output_type, op)


def vector_instruction_select(input_type, output_type, op, isa_ext):
    if isa_ext == "AVX2":
        return avx2_vector_instruction_select(input_type, output_type, op)
    elif isa_ext == "SSE":
        return sse_vector_instruction_select(input_type, output_type, op)


def scalar_reg_select(OUTPUT_TYPE, isa_ext):
    if isa_ext == "AVX2":
        reg_type = avx_scalar_register_map[OUTPUT_TYPE]
    elif isa_ext == "SSE":
        reg_type = sse_scalar_register_map[OUTPUT_TYPE]
    return reg_type(), reg_type()


def vector_reg_select(isa_ext, UNROLL_FACTOR, scalar=False):
    if isa_ext == "AVX2":
        reg = YMMRegister
    elif isa_ext == "SSE":
        reg = XMMRegister

    simd_accs = [reg() for _ in range(UNROLL_FACTOR)]
    if scalar:
        simd_ops = reg()
    else:
        simd_ops = [reg() for _ in range(UNROLL_FACTOR)]
    return simd_accs, simd_ops


def MOV_GPR_TO_VECTOR(vector_reg, gpr, input_type, output_type, isa_ext):
    if isa_ext == "AVX2":
        avx2_mov_gpr_to_vector(vector_reg, gpr, input_type, output_type)
    elif isa_ext == "SSE":
        sse_mov_gpr_to_vector(vector_reg, gpr, input_type, output_type)


def avx2_mov_gpr_to_vector(vector_reg, gpr, input_type, output_type):
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


def sse_mov_gpr_to_vector(vector_reg, gpr, input_type, output_type):
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
