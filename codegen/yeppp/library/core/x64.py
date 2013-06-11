#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

__author__ = 'Marat'

from peachpy.x64 import *

def SCALAR_INT_ADD_SUB(xPointer, yPointer, zPointer, x_type, y_type, z_type, operation):
	acc = GeneralPurposeRegister64() if z_type.get_size() == 8 else GeneralPurposeRegister32()
	LOAD.ELEMENT( acc, [xPointer], x_type )
	temp = GeneralPurposeRegister64() if z_type.get_size() == 8 else GeneralPurposeRegister32()
	LOAD.ELEMENT( temp, [yPointer], y_type )

	COMPUTE = { 'Add': ADD, 'Subtract': SUB }[operation]
	COMPUTE( acc, temp )

	STORE.ELEMENT( [zPointer], acc, z_type )

def AddSub_VusVus_Vus_Nehalem(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['Add', 'Subtract']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if z_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )
	
					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )
	
					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )
	
					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )
	
					LABEL( "zM16" )
					TEST( zPointer, 15 )
					JZ( "zA16" )
	
					SCALAR_INT_ADD_SUB(xPointer, yPointer, zPointer, x_type, y_type, z_type, function)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JZ( "return_ok" )
					JMP( "zM16" )
	
					LABEL( "zA16" )
					SUB( length, 64 / z_size )
					JB( "zA16_restore" )
	
					if x_size == z_size:
						SIMD_LOAD = MOVDQU
						load_increment = 16
					else:
						load_increment = 8
						if x_type.is_signed_integer():
							SIMD_LOAD = { 1: PMOVSXBW, 2: PMOVSXWD, 4: PMOVSXDQ }[x_size]
						else:
							SIMD_LOAD = { 1: PMOVZXBW, 2: PMOVZXWD, 4: PMOVZXDQ }[x_size]
	
					if function == 'Add':
						SIMD_COMPUTE = { 1: PADDB, 2: PADDW, 4: PADDD, 8: PADDQ }[z_size]
					elif function == 'Subtract':
						SIMD_COMPUTE = { 1: PSUBB, 2: PSUBW, 4: PSUBD, 8: PSUBQ }[z_size]
					SIMD_STORE = MOVDQA
	
					ALIGN( 16 )
					LABEL( "zA16_loop" )
	
					SIMD_LOAD( xmm0, [xPointer] )
					SIMD_LOAD( xmm4, [yPointer] )
					SIMD_COMPUTE( xmm0, xmm4 )
					SIMD_STORE( [zPointer], xmm0 )
	
					SIMD_LOAD( xmm1, [xPointer + load_increment] )
					SIMD_LOAD( xmm5, [yPointer + load_increment] )
					SIMD_COMPUTE( xmm1, xmm5 )
					SIMD_STORE( [zPointer + 16], xmm1 )
	
					SIMD_LOAD( xmm2, [xPointer + load_increment * 2] )
					SIMD_LOAD( xmm6, [yPointer + load_increment * 2] )
					SIMD_COMPUTE( xmm2, xmm6 )
					SIMD_STORE( [zPointer + 32], xmm2 )
	
					SIMD_LOAD( xmm3, [xPointer + load_increment * 3] )
					SIMD_LOAD( xmm7, [yPointer + load_increment * 3] )
					SIMD_COMPUTE( xmm3, xmm7 )
					SIMD_STORE( [zPointer + 48], xmm3 )
	
					ADD( xPointer, load_increment * 4 )
					ADD( yPointer, load_increment * 4 )
					ADD( zPointer, 64 )
					SUB( length, 64 / z_size )
					JAE( "zA16_loop" )
	
					LABEL( "zA16_restore" )
					ADD( length, 64 / z_size )
					JZ( "return_ok" )
					LABEL( "finalize" )
	
					SCALAR_INT_ADD_SUB(xPointer, yPointer, zPointer, x_type, y_type, z_type, function)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JNZ( "finalize" )
	
					LABEL( "return_ok" )
					XOR(eax, eax)
					LABEL( "return" )
					RET()

def SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type):
	acc = GeneralPurposeRegister64() if z_type.get_size() == 8 else GeneralPurposeRegister32()
	LOAD.ELEMENT( acc, [xPointer], x_type )
	temp = GeneralPurposeRegister64() if z_type.get_size() == 8 else GeneralPurposeRegister32()
	LOAD.ELEMENT( temp, [yPointer], y_type )

	IMUL( acc, temp )
	
	STORE.ELEMENT( [zPointer], acc, z_type )

def Mul_VTuVTu_VTu_implementation(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function == 'Multiply':
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if z_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				if x_size != z_size:
					return

				if x_size not in [2, 4]:
					return

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					PMUL = { 2: PMULLW, 4: PMULLD }[x_size]

					LABEL( "yM16" )
					TEST( yPointer, 15 )
					JZ( "yA16" )

					SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JZ( "return_ok" )
					JMP( "yM16" )

					LABEL( "yA16" )
					SUB( length, 128 / z_size )
					JB( "yA16_restore" )

					MOVDQU( xmm0, [xPointer] )
					MOVDQU( xmm1, [xPointer + 16] )
					MOVDQU( xmm2, [xPointer + 32] )
					MOVDQU( xmm3, [xPointer + 48] )
					MOVDQU( xmm4, [xPointer + 64] )
					PMUL( xmm0, [yPointer] )
					MOVDQU( xmm5, [xPointer + 80] )
					PMUL( xmm1, [yPointer + 16] )
					MOVDQU( xmm6, [xPointer + 96] )
					PMUL( xmm2, [yPointer + 32] )
					MOVDQU( xmm7, [xPointer + 112] )
					PMUL( xmm3, [yPointer + 48] )
					SUB( xPointer, -128 )
					SUB( length, 128 / z_size )
					JB( "skip_SWP" )

					ALIGN( 16 )
					LABEL( "yA16_loop" )

					MOVDQU( [zPointer], xmm0 )
					MOVDQU( xmm0, [xPointer] )
					PMUL( xmm4, [yPointer + 64] )

					MOVDQU( [zPointer + 16], xmm1 )
					MOVDQU( xmm1, [xPointer + 16] )
					PMUL( xmm5, [yPointer + 80] )

					MOVDQU( [zPointer + 32], xmm2 )
					MOVDQU( xmm2, [xPointer + 32] )
					PMUL( xmm6, [yPointer + 96] )

					MOVDQU( [zPointer + 48], xmm3 )
					MOVDQU( xmm3, [xPointer + 48] )
					PMUL( xmm7, [yPointer + 112] )

					SUB( yPointer, -128 )

					MOVDQU( [zPointer + 64], xmm4 )
					MOVDQU( xmm4, [xPointer + 64] )
					PMUL(xmm0, [yPointer] )
	
					MOVDQU( [zPointer + 80], xmm5 )
					MOVDQU( xmm5, [xPointer + 80] )
					PMUL( xmm1, [yPointer + 16] )

					MOVDQU( [zPointer + 96], xmm6 )
					MOVDQU( xmm6, [xPointer + 96] )
					PMUL( xmm2, [yPointer + 32] )

					MOVDQU( [zPointer + 112], xmm7 )
					MOVDQU( xmm7, [xPointer + 112] )
					PMUL( xmm3, [yPointer + 48] )

					SUB( xPointer, -128 )
					SUB( zPointer, -128 )
					SUB( length, 128 / z_size )
					JAE( "yA16_loop" )

					LABEL( "skip_SWP" )

					MOVDQU( [zPointer], xmm0 )
					PMUL( xmm4, [yPointer + 64] )

					MOVDQU( [zPointer + 16], xmm1 )
					PMUL( xmm5, [yPointer + 80] )

					MOVDQU( [zPointer + 32], xmm2 )
					PMUL( xmm6, [yPointer + 96] )

					MOVDQU( [zPointer + 48], xmm3 )
					PMUL( xmm7, [yPointer + 112] )

					SUB( yPointer, -128 )

					MOVDQU( [zPointer + 64], xmm4 )
					PMUL( xmm0, [yPointer] )

					MOVDQU( [zPointer + 80], xmm5 )
					PMUL( xmm1, [yPointer + 16] )

					MOVDQU( [zPointer + 96], xmm6 )
					PMUL( xmm2, [yPointer + 32] )

					MOVDQU( [zPointer + 112], xmm7 )
					PMUL( xmm3, [yPointer + 48] )

					SUB( zPointer, -128 )

					LABEL( "yA16_restore" )
					ADD( length, 128 / z_size )
					JZ( "return_ok" )
					LABEL( "finalize" )

					SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JNZ( "finalize" )

					LABEL( "return_ok" )
					XOR(eax, eax)
					LABEL( "return" )
					RET()

def Mul_V16usV16us_V32us_implementation(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function == 'Multiply':
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if z_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				if x_size == z_size or x_size != 2:
					return

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )
					
					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )
	
					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )
	
					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )
	
					PMUL_LOW = PMULLW
					PMUL_HIGH = PMULHW if z_type.is_signed_integer() else PMULHUW
	
					LABEL( "zM16" )
					TEST( zPointer, 15 )
					JZ( "zA16" )
	
					SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JZ( "return_ok" )
					JMP( "zM16" )
	
					LABEL( "zA16" )
					SUB( length, 64 / z_size )
					JB( "zA16_restore" )
	
					ALIGN( 16 )
					LABEL( "zA16_loop" )
	
					MOVDQU( xmm0, [xPointer] )
					MOVDQU( xmm1, [yPointer] )
					MOVDQA( xmm2, xmm0 )
					PMUL_LOW( xmm0, xmm1 )
					PMUL_HIGH( xmm2, xmm1 )
					MOVDQA( xmm1, xmm0 )
					PUNPCKLWD( xmm0, xmm2 )
					PUNPCKHWD( xmm1, xmm2 )
					MOVDQA( [zPointer], xmm0 )
					MOVDQA( [zPointer + 16], xmm1 )
	
					MOVDQU( xmm4, [xPointer + 16] )
					MOVDQU( xmm5, [yPointer + 16] )
					MOVDQA( xmm6, xmm4 )
					PMUL_LOW( xmm4, xmm5 )
					PMUL_HIGH( xmm6, xmm5 )
					MOVDQA( xmm5, xmm4 )
					PUNPCKLWD( xmm4, xmm6 )
					PUNPCKHWD( xmm5, xmm6 )
					MOVDQA( [zPointer + 32], xmm4 )
					MOVDQA( [zPointer + 48], xmm5 )
	
					ADD( xPointer, 32 )
					ADD( yPointer, 32 )
					ADD( zPointer, 64 )
					SUB( length, 64 / z_size )
					JAE( "zA16_loop" )
	
					LABEL( "zA16_restore" )
					ADD( length, 64 / z_size )
					JZ( "return_ok" )
					LABEL( "finalize" )
	
					SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JNZ( "finalize" )
	
					LABEL( "return_ok" )
					XOR(eax, eax)
					LABEL( "return" )
					RET()

def Mul_V32usV32us_V64us_implementation(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function == 'Multiply':
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if z_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				if x_size == z_size or x_size != 4:
					return

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )
	
					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )
	
					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )
	
					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )
	
					PMUL = PMULDQ if z_type.is_signed_integer() else PMULUDQ
	
					LABEL( "zM16" )
					TEST( zPointer, 15 )
					JZ( "zA16" )
	
					SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JZ( "return_ok" )
					JMP( "zM16" )
	
					LABEL( "zA16" )
					SUB( length, 96 / z_size )
					JB( "zA16_restore" )
	
					PMOVZXDQ( xmm0, [xPointer] )
					PMOVZXDQ( xmm1, [yPointer] )
	
					PMOVZXDQ( xmm2, [xPointer + 8] )
					PMOVZXDQ( xmm3, [yPointer + 8] )
	
					PMOVZXDQ( xmm4, [xPointer + 16] )
					PMOVZXDQ( xmm5, [yPointer + 16] )
	
					PMOVZXDQ( xmm6, [xPointer + 24] )
					PMOVZXDQ( xmm7, [yPointer + 24] )
					PMUL( xmm0, xmm1 )
	
					PMOVZXDQ( xmm8, [xPointer + 32] )
					PMOVZXDQ( xmm9, [yPointer + 32] )
					PMUL( xmm2, xmm3 )
	
					PMOVZXDQ( xmm10, [xPointer + 40] )
					PMOVZXDQ( xmm11, [yPointer + 40] )
					PMUL( xmm4, xmm5 )
	
					ADD( xPointer, 48 )
					ADD( yPointer, 48 )
					SUB( length, 96 / z_size )
					JB( "skip_SWP" )
	
					ALIGN( 16 )
					LABEL( "zA16_loop" )
	
					MOVDQA( [zPointer], xmm0 )
					PMOVZXDQ( xmm0, [xPointer] )
					PMOVZXDQ( xmm1, [yPointer] )
					PMUL( xmm6, xmm7 )
	
					MOVDQA( [zPointer + 16], xmm2 )
					PMOVZXDQ( xmm2, [xPointer + 8] )
					PMOVZXDQ( xmm3, [yPointer + 8] )
					PMUL( xmm8, xmm9 )
	
					MOVDQA( [zPointer + 32], xmm4 )
					PMOVZXDQ( xmm4, [xPointer + 16] )
					PMOVZXDQ( xmm5, [yPointer + 16] )
					PMUL( xmm10, xmm11 )
	
					MOVDQA( [zPointer + 48], xmm6 )
					PMOVZXDQ( xmm6, [xPointer + 24] )
					PMOVZXDQ( xmm7, [yPointer + 24] )
					PMUL( xmm0, xmm1 )
	
					MOVDQA( [zPointer + 64], xmm8 )
					PMOVZXDQ( xmm8, [xPointer + 32] )
					PMOVZXDQ( xmm9, [yPointer + 32] )
					PMUL( xmm2, xmm3 )
	
					MOVDQA( [zPointer + 80], xmm10 )
					PMOVZXDQ( xmm10, [xPointer + 40] )
					PMOVZXDQ( xmm11, [yPointer + 40] )
					PMUL( xmm4, xmm5 )
	
					ADD( xPointer, 48 )
					ADD( yPointer, 48 )
					ADD( zPointer, 96 )
					SUB( length, 96 / z_size )
					JAE( "zA16_loop" )
	
					LABEL( "skip_SWP" )
	
					MOVDQA( [zPointer], xmm0 )
					PMUL( xmm6, xmm7 )
	
					MOVDQA( [zPointer + 16], xmm2 )
					PMUL( xmm8, xmm9 )
	
					MOVDQA( [zPointer + 32], xmm4 )
					PMUL( xmm10, xmm11 )
	
					MOVDQA( [zPointer + 48], xmm6 )
					MOVDQA( [zPointer + 64], xmm8 )
					MOVDQA( [zPointer + 80], xmm10 )
	
					ADD( zPointer, 96 )
	
					LABEL( "zA16_restore" )
					ADD( length, 96 / z_size )
					JZ( "return_ok" )
					LABEL( "finalize" )
	
					SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type)
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JNZ( "finalize" )
	
					LABEL( "return_ok" )
					XOR(eax, eax)
					LABEL( "return" )
					RET()

def AddSubMulMinMax_VfVf_Vf_implementation(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['Add', 'Subtract', 'Multiply', 'Min', 'Max']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if not z_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					yPointer = GeneralPurposeRegister64()
					zPointer = GeneralPurposeRegister64()
					length = GeneralPurposeRegister64()
	
					LOAD.PARAMETER( xPointer, x_argument )
					LOAD.PARAMETER( yPointer, y_argument )
					LOAD.PARAMETER( zPointer, z_argument )
					LOAD.PARAMETER( length, length_argument )
	
					if x_size == 4:
						SCALAR_LOAD = MOVSS
						SCALAR_COMPUTE = { "Add": ADDSS, "Subtract": SUBSS, "Multiply": MULSS, 'Min': MINSS, 'Max': MAXSS }[function]
						SCALAR_STORE = MOVSS
						SIMD_LOAD = MOVUPS
						SIMD_COMPUTE = { "Add": ADDPS, "Subtract": SUBPS, "Multiply": MULPS, 'Min': MINPS, 'Max': MAXPS }[function]
						SIMD_STORE = MOVUPS
					else:
						SCALAR_LOAD = MOVSD
						SCALAR_COMPUTE = { "Add": ADDSD, "Subtract": SUBSD, "Multiply": MULSD, 'Min': MINSD, 'Max': MAXSD }[function]
						SCALAR_STORE = MOVSD
						SIMD_LOAD = MOVUPD
						SIMD_COMPUTE = { "Add": ADDPD, "Subtract": SUBPD, "Multiply": MULPD, 'Min': MINPD, 'Max': MAXPD }[function]
						SIMD_STORE = MOVUPD
	
					def PROCESS_SCALAR():
						SCALAR_LOAD( xmm0, [xPointer] )
						SCALAR_LOAD( xmm1, [yPointer] )
						SCALAR_COMPUTE( xmm0, xmm1 )
						SCALAR_STORE( [zPointer], xmm0 )
	
					LABEL( "yM16" )
					TEST( yPointer, 15)
					JZ( "yA16" )
	
					PROCESS_SCALAR()
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JZ( "return_ok" )
					JMP( "yM16" )
	
					LABEL( "yA16" )
					SUB( length, 128 / z_size )
					JB( "yA16_restore" )
	
					SIMD_LOAD( xmm0, [xPointer] )
					SIMD_LOAD( xmm1, [xPointer + 16 * 1] )
	
					SIMD_LOAD( xmm2, [xPointer + 16 * 2] )
					SIMD_COMPUTE( xmm0, [yPointer] )
	
					SIMD_LOAD( xmm3, [xPointer + 16 * 3] )
					SIMD_COMPUTE( xmm1, [yPointer + 16 * 1] )
	
					SIMD_LOAD( xmm4, [xPointer + 16 * 4] )
					SIMD_COMPUTE( xmm2, [yPointer + 16 * 2] )
	
					SIMD_LOAD( xmm5, [xPointer + 16 * 5] )
					SIMD_COMPUTE( xmm3, [yPointer + 16 * 3] )
	
					SIMD_LOAD( xmm6, [xPointer + 16 * 6] )
					SIMD_COMPUTE( xmm4, [yPointer + 16 * 4] )
	
					SIMD_LOAD( xmm7, [xPointer + 16 * 7] )
					SIMD_COMPUTE( xmm5, [yPointer + 16 * 5] )
	
					ADD( xPointer, 128 )
					SUB( length, 128 / z_size )
					JB( "skip_SWP" )
	
					ALIGN( 16 )
					LABEL( "yA16_loop" )
	
					SIMD_STORE( [zPointer], xmm0 )
					SIMD_LOAD( xmm0, [xPointer] )
					SIMD_COMPUTE( xmm6, [yPointer + 16 * 6] )
	
					SIMD_STORE( [zPointer + 16 * 1], xmm1 )
					SIMD_LOAD( xmm1, [xPointer + 16 * 1] )
					SIMD_COMPUTE( xmm7, [yPointer + 16 * 7] )
	
					ADD( yPointer, 128 )
	
					SIMD_STORE( [zPointer + 16 * 2], xmm2 )
					SIMD_LOAD( xmm2, [xPointer + 16 * 2] )
					SIMD_COMPUTE( xmm0, [yPointer] )
	
					SIMD_STORE( [zPointer + 16 * 3], xmm3 )
					SIMD_LOAD( xmm3, [xPointer + 16 * 3] )
					SIMD_COMPUTE( xmm1, [yPointer + 16 * 1] )
	
					SIMD_STORE( [zPointer + 16 * 4], xmm4 )
					SIMD_LOAD( xmm4, [xPointer + 16 * 4] )
					SIMD_COMPUTE( xmm2, [yPointer + 16 * 2] )
	
					SIMD_STORE( [zPointer + 16 * 5], xmm5 )
					SIMD_LOAD( xmm5, [xPointer + 16 * 5] )
					SIMD_COMPUTE( xmm3, [yPointer + 16 * 3] )
	
					SIMD_STORE( [zPointer + 16 * 6], xmm6 )
					SIMD_LOAD( xmm6, [xPointer + 16 * 6] )
					SIMD_COMPUTE( xmm4, [yPointer + 16 * 4] )
	
					SIMD_STORE( [zPointer + 16 * 7], xmm7 )
					SIMD_LOAD( xmm7, [xPointer + 16 * 7] )
					SIMD_COMPUTE( xmm5, [yPointer + 16 * 5] )
	
					ADD( xPointer, 128 )
					ADD( zPointer, 128 )
					SUB( length, 128 / z_size )
					JAE( "yA16_loop" )
	
					LABEL( "skip_SWP" )
	
					SIMD_STORE( [zPointer], xmm0 )
					SIMD_COMPUTE( xmm6, [yPointer + 16 * 6] )
	
					SIMD_STORE( [zPointer + 16 * 1], xmm1 )
					SIMD_COMPUTE( xmm7, [yPointer + 16 * 7] )
	
					SIMD_STORE( [zPointer + 16 * 2], xmm2 )
					SIMD_STORE( [zPointer + 16 * 3], xmm3 )
					SIMD_STORE( [zPointer + 16 * 4], xmm4 )
					SIMD_STORE( [zPointer + 16 * 5], xmm5 )
					SIMD_STORE( [zPointer + 16 * 6], xmm6 )
					SIMD_STORE( [zPointer + 16 * 7], xmm7 )
	
					ADD( yPointer, 128 )
					ADD( zPointer, 128 )
	
					LABEL( "yA16_restore" )
					ADD( length, 128 / z_size )
					JZ( "return_ok" )
					LABEL( "finalize" )
	
					PROCESS_SCALAR()
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					ADD( zPointer, z_size )
					SUB( length, 1 )
					JNZ( "finalize" )
	
					LABEL( "return_ok" )
					XOR(eax, eax)
					LABEL( "return" )
					RET()

def PipelineReduce_VXf_SXf(xPointer, yPointer, length, accumulators, ctype, scalar_function, reduction_function, instruction_columns, instruction_offsets):
	# Check that we have an offset for each instruction column
	assert len(instruction_columns) == len(instruction_offsets)

	max_instructions  = max(map(len, instruction_columns))
	max_register_size = max(register.get_size() for register in accumulators)
	batch_bytes       = sum(register.get_size() for register in accumulators)
	batch_elements    = batch_bytes / ctype.get_size()
	
	source_y_aligned          = Label("source_y_%sb_aligned" % max_register_size)
	source_y_misaligned       = Label("source_y_%sb_misaligned" % max_register_size)
	return_ok                 = Label("return_ok")
	return_null_pointer       = Label("return_null_pointer")
	return_misaligned_pointer = Label("return_misaligned_pointer")
	return_any                = Label("return")
	reduce_batch              = Label("reduce_batch")
	batch_process_finish      = Label("batch_process_finish")
	process_single            = Label("process_single")
	process_batch             = Label("process_batch")
	process_batch_prologue    = Label("process_batch_prologue") 
	process_batch_epilogue    = Label("process_batch_epilogue") 

	# Check parameters
	TEST( xPointer, xPointer )
	JZ( return_null_pointer )
	
	TEST( xPointer, ctype.get_size() - 1 )
	JNZ( return_misaligned_pointer )
	
	TEST( yPointer, yPointer )
	JZ( return_null_pointer )
	
	TEST( yPointer, ctype.get_size() - 1 )
	JNZ( return_misaligned_pointer )

	# If length is zero, return immediately
	TEST( length, length )
	JZ( return_ok )

	# Initialize accumulators to zero
	for accumulator in accumulators:
		LOAD.ZERO( accumulator, ctype )

	# If the y pointer is not aligned by register size, process by one element until it becomes aligned
	TEST( yPointer, max_register_size - 1 )
	JZ( source_y_aligned )

	LABEL( source_y_misaligned )
	scalar_function(accumulators[0], xPointer)
	ADD( xPointer, ctype.get_size() )
	ADD( yPointer, ctype.get_size() )
	SUB( length, 1 )
	JZ( reduce_batch )

	TEST( yPointer, max_register_size - 1 )
	JNZ( source_y_misaligned )

	LABEL( source_y_aligned )
	SUB( length, batch_elements )
	JB( batch_process_finish )

	LABEL( process_batch_prologue )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			if i >= instruction_offset:
				Function.get_current().add_instruction(instruction_column[i - instruction_offset])

	SUB( length, batch_elements )
	JB( process_batch_epilogue )

	ALIGN( 16 )
	LABEL( process_batch )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			Function.get_current().add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

	SUB( length, batch_elements )
	JAE( process_batch )

	LABEL( process_batch_epilogue )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			if i < instruction_offset:
				Function.get_current().add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

	LABEL( batch_process_finish )
	ADD( length, batch_elements )
	JZ( reduce_batch )

	LABEL( process_single )
	scalar_function(accumulators[0], xPointer)
	ADD( xPointer, ctype.get_size() )
	ADD( yPointer, ctype.get_size() )
	SUB( length, 1 )
	JNZ( process_single )

	LABEL( reduce_batch )
	reduction_function(accumulators, ctype, ctype)
	
	STORE.ELEMENT( [yPointer], accumulators[0], ctype )
	
	LABEL( return_ok )
	XOR( eax, eax )
	
	LABEL( return_any )
	RETURN()

	LABEL( return_null_pointer )
	MOV( eax, 1 )
	JMP( return_any )
	
	LABEL( return_misaligned_pointer )
	MOV( eax, 2 )
	JMP( return_any )

def SumAbs_VXf_SXf_SSE(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumAbs']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type)):
					return

				if len(set([x_type, y_type])) != 1:
					return
				else:
					ctype = x_type

				SIMD_LOAD  = {4: MOVUPS, 8: MOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: ADDPS, 8: ADDPD}[x_type.get_size()]
				SIMD_AND   = {4: ANDPS, 8: ANDPD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer, xmm_abs_mask):
					# Load x
					x = SSERegister()
					LOAD.ELEMENT( x, [xPointer], x_type )
					# Take absolute value
					SIMD_AND( x, xmm_abs_mask )
					# Accumulate
					SIMD_ADD( acc, x )

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					xmm_abs_mask = SSERegister()
					LOAD.CONSTANT( xmm_abs_mask, Constant.uint64x2(0x7FFFFFFFFFFFFFFFL))

					unroll_registers  = 7
					register_size     = 16
					acc  = [SSERegister() for _ in range(unroll_registers)]
					temp = [SSERegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 3, 4)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_AND( temp[i], xmm_abs_mask )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )

					scalar_function = lambda accumulator, x_pointer: PROCESS_SCALAR(accumulator, x_pointer, xmm_abs_mask)
					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, scalar_function, REDUCE.SUM, instruction_columns, instruction_offsets)

def SumAbs_VXf_SXf_AVX(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumAbs']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type)):
					return

				if len(set([x_type, y_type])) != 1:
					return
				else:
					ctype = x_type

				SIMD_LOAD  = {4: VMOVUPS, 8: VMOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: VADDPS, 8: VADDPD}[x_type.get_size()]
				SIMD_AND   = {4: VANDPS, 8: VANDPD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer, ymm_abs_mask):
					# Load x
					x = SSERegister()
					LOAD.ELEMENT( x, [xPointer], x_type )
					# Take absolute value
					SIMD_AND( x, ymm_abs_mask.get_oword() )
					# Accumulate
					if isinstance(acc, AVXRegister):
						SIMD_ADD( acc, x.get_hword() )
					else:
						SIMD_ADD( acc, x )

				with Function(codegen, function_signature, arguments, 'SandyBridge'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					ymm_abs_mask = AVXRegister()
					LOAD.CONSTANT( ymm_abs_mask, Constant.uint64x4(0x7FFFFFFFFFFFFFFFL))

					unroll_registers  = 7
					register_size     = 32
					acc  = [AVXRegister() for _ in range(unroll_registers)]
					temp = [AVXRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 4, 5)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_AND( temp[i], ymm_abs_mask )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )

					scalar_function = lambda accumulator, x_pointer: PROCESS_SCALAR(accumulator, x_pointer, ymm_abs_mask)
					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, scalar_function, REDUCE.SUM, instruction_columns, instruction_offsets)

				with Function(codegen, function_signature, arguments, 'Bulldozer'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					ymm_abs_mask = AVXRegister()
					LOAD.CONSTANT( ymm_abs_mask, Constant.uint64x4(0x7FFFFFFFFFFFFFFFL))

					unroll_registers  = 6
					acc  = [AVXRegister() if i % 3 == 2 else SSERegister() for i in range(unroll_registers)]
					temp = [AVXRegister() if i % 3 == 2 else SSERegister() for i in range(unroll_registers)]

					instruction_offsets = (0, 3, 4)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					offset = 0 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + offset] )
						with instruction_columns[1]:
							if isinstance(temp[i], AVXRegister):
								SIMD_AND( temp[i], ymm_abs_mask )
							else:
								SIMD_AND( temp[i], ymm_abs_mask.get_oword() )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
						offset += acc[i].get_size()
					with instruction_columns[0]:
						ADD( xPointer, sum(register.get_size() for register in acc) )

					scalar_function = lambda accumulator, x_pointer: PROCESS_SCALAR(accumulator, x_pointer, ymm_abs_mask)
					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, scalar_function, REDUCE.SUM, instruction_columns, instruction_offsets)

def Sum_VXf_SXf_SSE(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['Sum']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type)):
					return

				if len(set([x_type, y_type])) != 1:
					return
				else:
					ctype = x_type

				SIMD_LOAD  = {4: MOVUPS, 8: MOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: ADDPS, 8: ADDPD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer):
					# Load x
					x = SSERegister()
					LOAD.ELEMENT( x, [xPointer], x_type )
					# Accumulate
					SIMD_ADD( acc, x )

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 8
					register_size     = 16
					acc  = [SSERegister() for _ in range(unroll_registers)]
					temp = [SSERegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 5)
					instruction_columns = [InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

def Sum_VXf_SXf_AVX(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['Sum']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type)):
					return

				if len(set([x_type, y_type])) != 1:
					return
				else:
					ctype = x_type

				SIMD_LOAD  = {4: VMOVUPS, 8: VMOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: VADDPS, 8: VADDPD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer):
					# Load x
					x = SSERegister()
					LOAD.ELEMENT( x, [xPointer], x_type )
					# Accumulate
					if isinstance(acc, AVXRegister):
						SIMD_ADD( acc, x.get_hword() )
					else:
						SIMD_ADD( acc, x )

				with Function(codegen, function_signature, arguments, 'SandyBridge'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 9
					register_size     = 32
					acc  = [AVXRegister() for _ in range(unroll_registers)]
					temp = [AVXRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 4)
					instruction_columns = [InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

				with Function(codegen, function_signature, arguments, 'Bulldozer'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 9
					acc  = [AVXRegister() if i % 3 == 2 else SSERegister() for i in range(unroll_registers)]
					temp = [AVXRegister() if i % 3 == 2 else SSERegister() for i in range(unroll_registers)]

					instruction_offsets = (0, 4)
					instruction_columns = [InstructionStream(), InstructionStream()] 
					offset = 0 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + offset])
						with instruction_columns[1]:
							SIMD_ADD( acc[i], temp[i] )
						offset += acc[i].get_size()
					with instruction_columns[0]:
						ADD( xPointer, sum(register.get_size() for register in acc) )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

def SumSquares_VXf_SXf_SSE(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumSquares']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type)):
					return

				if len(set([x_type, y_type])) != 1:
					return
				else:
					ctype = x_type

				SCALAR_MUL = {4: MULSS, 8: MULSD}[x_type.get_size()]
				SIMD_LOAD  = {4: MOVUPS, 8: MOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: ADDPS, 8: ADDPD}[x_type.get_size()]
				SIMD_MUL   = {4: MULPS, 8: MULPD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer):
					# Load x
					temp = SSERegister()
					LOAD.ELEMENT( temp, [xPointer], x_type )
					# Square x
					SCALAR_MUL( temp, temp )
					# Accumulate
					SIMD_ADD( acc, temp )

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 8
					register_size     = 16
					acc  = [SSERegister() for _ in range(unroll_registers)]
					temp = [SSERegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 2, 5)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_MUL( temp[i], temp[i] )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )
					with instruction_columns[1]:
						ADD( yPointer, register_size * unroll_registers )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

def SumSquares_VXf_SXf_AVX(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumSquares']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type)):
					return

				if len(set([x_type, y_type])) != 1:
					return
				else:
					ctype = x_type

				SCALAR_MUL = {4: VMULSS, 8: VMULSD}[x_type.get_size()]
				SIMD_LOAD  = {4: VMOVUPS, 8: VMOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: VADDPS, 8: VADDPD}[x_type.get_size()]
				SIMD_MUL   = {4: VMULPS, 8: VMULPD}[x_type.get_size()]
				SIMD_FMA4  = {4: VFMADDPS, 8: VFMADDPD}[x_type.get_size()]
				SIMD_FMA3  = {4: VFMADD231PS, 8: VFMADD231PD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer):
					if Target.has_fma():
						# Load x
						x = SSERegister()
						LOAD.ELEMENT( x, [xPointer], x_type )
						# Square x and accumulate
						if Target.has_fma4():
							if isinstance(acc, AVXRegister):
								SIMD_FMA4( acc, x.get_hword(), x.get_hword(), acc )
							else:
								SIMD_FMA4( acc, x, x, acc )
						else:
							SIMD_FMA3( acc, x.get_hword(), x.get_hword(), acc )
					else:
						# Load x
						temp = SSERegister()
						LOAD.ELEMENT( temp, [xPointer], x_type )
						# Square x
						SCALAR_MUL( temp, temp )
						# Accumulate
						SIMD_ADD( acc, temp.get_hword() )

				with Function(codegen, function_signature, arguments, 'SandyBridge'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 8
					register_size     = 32
					acc  = [AVXRegister() for _ in range(unroll_registers)]
					temp = [AVXRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 2, 5)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_MUL( temp[i], temp[i] )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )
					with instruction_columns[1]:
						ADD( yPointer, register_size * unroll_registers )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

				with Function(codegen, function_signature, arguments, 'Bulldozer'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 12
					acc  = [SSERegister() if i % 3 != 2 else AVXRegister() for i in range(unroll_registers)]
					temp = [SSERegister() if i % 3 != 2 else AVXRegister() for i in range(unroll_registers)]

					instruction_offsets = (0, 3)
					instruction_columns = [InstructionStream(), InstructionStream()]
					offset = 0 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + offset])
						with instruction_columns[1]:
							SIMD_FMA4( acc[i], temp[i], [yPointer + offset], acc[i] )
						offset += acc[i].get_size()
					with instruction_columns[0]:
						ADD( xPointer, sum(register.get_size() for register in acc) )
					with instruction_columns[1]:
						ADD( yPointer, sum(register.get_size() for register in acc) )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

				with Function(codegen, function_signature, arguments, 'Haswell'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 12
					register_size     = 32
					acc  = [AVXRegister() for _ in range(unroll_registers)]
					temp = [AVXRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 3)
					instruction_columns = [InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_FMA3( acc[i], temp[i], [yPointer + i * register_size], acc[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )
					with instruction_columns[1]:
						ADD( yPointer, register_size * unroll_registers )

					PipelineReduce_VXf_SXf(xPointer, yPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)
				
def PipelineReduce_VXfVXf_SXf(xPointer, yPointer, zPointer, length, accumulators, ctype, scalar_function, reduction_function, instruction_columns, instruction_offsets, use_simd = True):
	# Check that we have an offset for each instruction column
	assert len(instruction_columns) == len(instruction_offsets)

	max_instructions  = max(map(len, instruction_columns))
	max_register_size = max(register.get_size() for register in accumulators)
	if use_simd:
		batch_bytes       = sum(register.get_size() for register in accumulators)
		batch_elements    = batch_bytes / ctype.get_size()
	else:
		batch_bytes       = len(accumulators) * ctype.get_size()
		batch_elements    = len(accumulators)
	
	source_y_aligned          = Label("source_y_%sb_aligned" % max_register_size)
	source_y_misaligned       = Label("source_y_%sb_misaligned" % max_register_size)
	return_ok                 = Label("return_ok")
	return_null_pointer       = Label("return_null_pointer")
	return_misaligned_pointer = Label("return_misaligned_pointer")
	return_any                = Label("return")
	reduce_batch              = Label("reduce_batch")
	batch_process_finish      = Label("batch_process_finish")
	process_single            = Label("process_single")
	process_batch             = Label("process_batch")
	process_batch_prologue    = Label("process_batch_prologue") 
	process_batch_epilogue    = Label("process_batch_epilogue") 

	# Check parameters
	TEST( xPointer, xPointer )
	JZ( return_null_pointer )
	
	TEST( xPointer, ctype.get_size() - 1 )
	JNZ( return_misaligned_pointer )
	
	TEST( yPointer, yPointer )
	JZ( return_null_pointer )
	
	TEST( yPointer, ctype.get_size() - 1 )
	JNZ( return_misaligned_pointer )

	TEST( zPointer, zPointer )
	JZ( return_null_pointer )
	
	TEST( zPointer, ctype.get_size() - 1 )
	JNZ( return_misaligned_pointer )

	# If length is zero, return immediately
	TEST( length, length )
	JZ( return_ok )

	# Initialize accumulators to zero
	for accumulator in accumulators:
		LOAD.ZERO( accumulator, ctype )

	if use_simd:
		# If the y pointer is not aligned by register size, process by one element until it becomes aligned
		TEST( yPointer, max_register_size - 1 )
		JZ( source_y_aligned )
	
		LABEL( source_y_misaligned )
		scalar_function(accumulators[0], xPointer, yPointer)
		ADD( xPointer, ctype.get_size() )
		ADD( yPointer, ctype.get_size() )
		SUB( length, 1 )
		JZ( reduce_batch )
	
		TEST( yPointer, max_register_size - 1 )
		JNZ( source_y_misaligned )
	
		LABEL( source_y_aligned )

	SUB( length, batch_elements )
	JB( batch_process_finish )

	LABEL( process_batch_prologue )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			if i >= instruction_offset:
				Function.get_current().add_instruction(instruction_column[i - instruction_offset])

	SUB( length, batch_elements )
	JB( process_batch_epilogue )

	ALIGN( 16 )
	LABEL( process_batch )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			Function.get_current().add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

	SUB( length, batch_elements )
	JAE( process_batch )

	LABEL( process_batch_epilogue )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			if i < instruction_offset:
				Function.get_current().add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

	LABEL( batch_process_finish )
	ADD( length, batch_elements )
	JZ( reduce_batch )

	LABEL( process_single )
	scalar_function(accumulators[0], xPointer, yPointer)
	ADD( xPointer, ctype.get_size() )
	ADD( yPointer, ctype.get_size() )
	SUB( length, 1 )
	JNZ( process_single )

	LABEL( reduce_batch )
	reduction_function(accumulators, ctype, ctype)
	
	STORE.ELEMENT( [zPointer], accumulators[0], ctype )
	
	LABEL( return_ok )
	XOR( eax, eax )
	
	LABEL( return_any )
	RETURN()

	LABEL( return_null_pointer )
	MOV( eax, 1 )
	JMP( return_any )
	
	LABEL( return_misaligned_pointer )
	MOV( eax, 2 )
	JMP( return_any )

def DotProduct_VXfVXf_SXf_SSE(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['DotProduct']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type, z_type)):
					return

				if len(set([x_type, y_type, z_type])) != 1:
					return
				else:
					ctype = x_type

				SCALAR_MUL  = {4: MULSS, 8: MULSD}[x_type.get_size()]
				SIMD_LOAD   = {4: MOVUPS, 8: MOVUPD}[x_type.get_size()]
				SIMD_ADD    = {4: ADDPS, 8: ADDPD}[x_type.get_size()]
				SIMD_MUL    = {4: MULPS, 8: MULPD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer, yPointer):
					# Load x
					temp = SSERegister()
					LOAD.ELEMENT( temp, [xPointer], x_type )
					# Load y and multiply
					SCALAR_MUL( temp, [yPointer] )
					# Accumulate
					SIMD_ADD( acc, temp )

				with Function(codegen, function_signature, arguments, 'Nehalem'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 8
					register_size     = 16
					acc  = [SSERegister() for _ in range(unroll_registers)]
					temp = [SSERegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 2, 5)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_MUL( temp[i], [yPointer + i * register_size] )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )
					with instruction_columns[1]:
						ADD( yPointer, register_size * unroll_registers )

					PipelineReduce_VXfVXf_SXf(xPointer, yPointer, zPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)
					
				if ctype.get_size() == 8:
					with Function(codegen, function_signature, arguments, 'Bonnell'):
						xPointer = GeneralPurposeRegister64()
						LOAD.PARAMETER( xPointer, x_argument )
	
						yPointer = GeneralPurposeRegister64()
						LOAD.PARAMETER( yPointer, y_argument )
	
						zPointer = GeneralPurposeRegister64()
						LOAD.PARAMETER( zPointer, z_argument )
	
						length = GeneralPurposeRegister64()
						LOAD.PARAMETER( length, length_argument )
	
						unroll_registers  = 8
						acc  = [SSERegister() for _ in range(unroll_registers)]
						temp = [SSERegister() for _ in range(unroll_registers)]
	
						instruction_offsets = (0, 1, 5)
						instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
						for i in range(unroll_registers):
							with instruction_columns[0]:
								MOVSD( temp[i], [xPointer + i * ctype.get_size()] )
							with instruction_columns[1]:
								MULSD( temp[i], [yPointer + i * ctype.get_size()] )
							with instruction_columns[2]:
								ADDSD( acc[i], temp[i] )
						with instruction_columns[0]:
							ADD( xPointer, ctype.get_size() * unroll_registers )
						with instruction_columns[1]:
							ADD( yPointer, ctype.get_size() * unroll_registers )
	
						PipelineReduce_VXfVXf_SXf(xPointer, yPointer, zPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets, use_simd = False)
						

def DotProduct_VXfVXf_SXf_AVX(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['DotProduct']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if not all(type.is_floating_point() for type in (x_type, y_type, z_type)):
					return

				if len(set([x_type, y_type, z_type])) != 1:
					return
				else:
					ctype = x_type

				SCALAR_MUL = {4: VMULSS, 8: VMULSD}[x_type.get_size()]
				SIMD_LOAD  = {4: VMOVUPS, 8: VMOVUPD}[x_type.get_size()]
				SIMD_ADD   = {4: VADDPS, 8: VADDPD}[x_type.get_size()]
				SIMD_MUL   = {4: VMULPS, 8: VMULPD}[x_type.get_size()]
				SIMD_FMA4  = {4: VFMADDPS, 8: VFMADDPD}[x_type.get_size()]
				SIMD_FMA3  = {4: VFMADD231PS, 8: VFMADD231PD}[x_type.get_size()]

				def PROCESS_SCALAR(acc, xPointer, yPointer):
					if Target.has_fma():
						# Load x
						x = SSERegister()
						LOAD.ELEMENT( x, [xPointer], x_type )
						# Load y
						y = SSERegister()
						LOAD.ELEMENT( y, [yPointer], y_type )
						# Multiply-accumulate
						if Target.has_fma4():
							if isinstance(acc, AVXRegister):
								SIMD_FMA4( acc, x.get_hword(), y.get_hword(), acc )
							else:
								SIMD_FMA4( acc, x, y, acc )
						else:
							SIMD_FMA3( acc, x.get_hword(), y.get_hword(), acc )
					else:
						# Load x
						temp = SSERegister()
						LOAD.ELEMENT( temp, [xPointer], x_type )
						# Load y and multiply
						SCALAR_MUL( temp, [yPointer] )
						# Accumulate
						SIMD_ADD( acc, temp.get_hword() )

				with Function(codegen, function_signature, arguments, 'SandyBridge'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 8
					register_size     = 32
					acc  = [AVXRegister() for _ in range(unroll_registers)]
					temp = [AVXRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 2, 5)
					instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_MUL( temp[i], [yPointer + i * register_size] )
						with instruction_columns[2]:
							SIMD_ADD( acc[i], temp[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )
					with instruction_columns[1]:
						ADD( yPointer, register_size * unroll_registers )

					PipelineReduce_VXfVXf_SXf(xPointer, yPointer, zPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

				with Function(codegen, function_signature, arguments, 'Bulldozer'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 12
					acc  = [SSERegister() if i % 3 != 2 else AVXRegister() for i in range(unroll_registers)]
					temp = [SSERegister() if i % 3 != 2 else AVXRegister() for i in range(unroll_registers)]

					instruction_offsets = (0, 3)
					instruction_columns = [InstructionStream(), InstructionStream()]
					offset = 0 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + offset])
						with instruction_columns[1]:
							SIMD_FMA4( acc[i], temp[i], [yPointer + offset], acc[i] )
						offset += acc[i].get_size()
					with instruction_columns[0]:
						ADD( xPointer, sum(register.get_size() for register in acc) )
					with instruction_columns[1]:
						ADD( yPointer, sum(register.get_size() for register in acc) )

					PipelineReduce_VXfVXf_SXf(xPointer, yPointer, zPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)

				with Function(codegen, function_signature, arguments, 'Haswell'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )

					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )

					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )

					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )

					unroll_registers  = 12
					register_size     = 32
					acc  = [AVXRegister() for _ in range(unroll_registers)]
					temp = [AVXRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 3)
					instruction_columns = [InstructionStream(), InstructionStream()] 
					for i in range(unroll_registers):
						with instruction_columns[0]:
							SIMD_LOAD( temp[i], [xPointer + i * register_size] )
						with instruction_columns[1]:
							SIMD_FMA3( acc[i], temp[i], [yPointer + i * register_size], acc[i] )
					with instruction_columns[0]:
						ADD( xPointer, register_size * unroll_registers )
					with instruction_columns[1]:
						ADD( yPointer, register_size * unroll_registers )

					PipelineReduce_VXfVXf_SXf(xPointer, yPointer, zPointer, length, acc, ctype, PROCESS_SCALAR, REDUCE.SUM, instruction_columns, instruction_offsets)
				
def DotProduct_V64fV64f_S64f_Bonnell(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['DotProduct']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if not z_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				if not z_size == 8:
					return

				with Function(codegen, function_signature, arguments, 'Bonnell'):
					xPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( xPointer, x_argument )
	
					yPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( yPointer, y_argument )
	
					zPointer = GeneralPurposeRegister64()
					LOAD.PARAMETER( zPointer, z_argument )
	
					length = GeneralPurposeRegister64()
					LOAD.PARAMETER( length, length_argument )
	
					XORPS( xmm8, xmm8 )
					XORPS( xmm9, xmm9 )
					XORPS( xmm10, xmm10 )
					XORPS( xmm11, xmm11 )
					XORPS( xmm12, xmm12 )
					XORPS( xmm13, xmm13 )
					XORPS( xmm14, xmm14 )
					XORPS( xmm15, xmm15 )
	
					SUB( length, 64 / z_size )
					JB( "xA8_restore" )
	
					MOVSD( xmm0, [yPointer] )
					MOVSD( xmm1, [yPointer + 8] )
					MOVSD( xmm2, [yPointer + 16] )
					MOVSD( xmm3, [yPointer + 24] )
					MOVSD( xmm4, [yPointer + 32] )
					MULSD( xmm0, [xPointer] )
					MOVSD( xmm5, [yPointer + 40] )
					MULSD( xmm1, [xPointer + 8] )
					MOVSD( xmm6, [yPointer + 48] )
					MULSD( xmm2, [xPointer + 16] )
					MOVSD( xmm7, [yPointer + 56] )
					MULSD( xmm3, [xPointer + 24] )
	
					ADD( yPointer, 64 )
	
					SUB( length, 64 / z_size )
					JB( "skip_SWP" )
	
					ALIGN( 16 )
					LABEL( "xA8_loop" )
	
					ADDSD( xmm8, xmm0 )
					MOVSD( xmm0, [yPointer] )
					MULSD( xmm4, [xPointer + 32] )
	
					ADDSD( xmm9, xmm1 )
					MOVSD( xmm1, [yPointer + 8] )
					MULSD( xmm5, [xPointer + 40] )
	
					ADDSD( xmm10, xmm2 )
					MOVSD( xmm2, [yPointer + 16] )
					MULSD( xmm6, [xPointer + 48] )
	
					ADDSD( xmm11, xmm3 )
					MOVSD( xmm3, [yPointer + 24] )
					MULSD( xmm7, [xPointer + 56] )
	
					ADD( xPointer, 64 )
	
					ADDSD( xmm12, xmm4 )
					MOVSD( xmm4, [yPointer + 32] )
					MULSD( xmm0, [xPointer] )
	
					ADDSD( xmm13, xmm5 )
					MOVSD( xmm5, [yPointer + 40] )
					MULSD( xmm1, [xPointer + 8] )
	
					ADDSD( xmm14, xmm6 )
					MOVSD( xmm6, [yPointer + 48] )
					MULSD( xmm2, [xPointer + 16] )
	
					ADDSD( xmm15, xmm7 )
					MOVSD( xmm7, [yPointer + 56] )
					MULSD( xmm3, [xPointer + 24] )
	
					ADD( yPointer, 64 )
					SUB( length, 64 / z_size )
					JAE( "xA8_loop" )
	
					LABEL( "skip_SWP" )
	
					ADDSD( xmm8, xmm0 )
					MULSD( xmm4, [xPointer + 32] )
	
					ADDSD( xmm9, xmm1 )
					MULSD( xmm5, [xPointer + 40] )
	
					ADDSD( xmm10, xmm2 )
					MULSD( xmm6, [xPointer + 48] )
	
					ADDSD( xmm11, xmm3 )
					MULSD( xmm7, [xPointer + 56] )
	
					ADD( xPointer, 64 )
					ADDSD( xmm12, xmm4 )
					ADDSD( xmm13, xmm5 )
					ADDSD( xmm14, xmm6 )
					ADDSD( xmm15, xmm7 )
	
					LABEL( "xA8_restore" )
					ADD( length, 64 / z_size )
					JZ( "return_ok" )
					LABEL( "finalize" )
	
					MOVSD( xmm0, [xPointer] )
					MULSD( xmm0, [yPointer] )
					ADDSD( xmm8, xmm0 )
	
					ADD( xPointer, x_size )
					ADD( yPointer, y_size )
					SUB( length, 1 )
					JNZ( "finalize" )
	
					LABEL( "return_ok" )
	
					ADDSD( xmm8, xmm9 )
					ADDSD( xmm10, xmm11 )
					ADDSD( xmm12, xmm13 )
					ADDSD( xmm14, xmm15 )
	
					ADDSD( xmm8, xmm10 )
					ADDSD( xmm12, xmm14 )
	
					ADDSD( xmm8, xmm12 )
	
					MOVSD( [zPointer], xmm8 )
	
					XOR( eax, eax )
					LABEL( "return" )
					RET()
