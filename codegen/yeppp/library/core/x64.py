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

	EXECUTE = { 'Add': ADD, 'Subtract': SUB }[operation]
	EXECUTE( acc, temp )

	STORE.ELEMENT( [zPointer], acc, z_type )

def AddSub_VusVus_Vus_implementation(codegen, function_signature, module, function, arguments):
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

				codegen.begin_function(function_signature, arguments, 'Nehalem')

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

				return codegen.end_function()

def SCALAR_INT_MUL(xPointer, yPointer, zPointer, x_type, y_type, z_type):
	microarchitecture = Function.get_current().microarchitecture
	has_bmi2 = microarchitecture.is_supported('BMI2')
	
	acc = GeneralPurposeRegister64() if z_type.get_size() == 8 else GeneralPurposeRegister32()
	LOAD.ELEMENT( acc, [xPointer], x_type )
	temp = GeneralPurposeRegister64() if z_type.get_size() == 8 else GeneralPurposeRegister32()
	LOAD.ELEMENT( temp, [yPointer], y_type )

	if has_bmi2:
		MULX( acc, acc, temp )
	else:
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

				codegen.begin_function(function_signature, arguments, 'Nehalem')

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
				PMUL( xmm0, [yPointer] )

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

				return codegen.end_function()

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

				codegen.begin_function(function_signature, arguments, 'Nehalem')

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

				return codegen.end_function()

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

				codegen.begin_function(function_signature, arguments, 'Nehalem')

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

				return codegen.end_function()

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

				codegen.begin_function(function_signature, arguments, 'Nehalem')

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

				return codegen.end_function()

def SumSquares_Vf_Sf_implementation_Nehalem(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumSquares']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not x_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)

				codegen.begin_function(function_signature, arguments, 'Nehalem')

				xPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( xPointer, x_argument )

				yPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( yPointer, y_argument )

				length = GeneralPurposeRegister64()
				LOAD.PARAMETER( length, length_argument )

				SCALAR_LOAD  = { 4: MOVSS, 8: MOVSD }[x_size]
				SCALAR_ADD   = { 4: ADDSS, 8: ADDSD }[x_size]
				SCALAR_MUL   = { 4: MULSS, 8: MULSD }[x_size]
				SCALAR_STORE = { 4: MOVSS, 8: MOVSD }[x_size]
				SIMD_LOAD    = MOVAPS
				SIMD_ADD     = { 4: ADDPS, 8: ADDPD }[x_size]
				SIMD_MUL     = { 4: MULPS, 8: MULPD }[x_size]
				
				if x_size == 4:
					def SIMD_ZERO(register):
						XORPS( register, register )
					def SIMD_REDUCE(register):
						HADDPS( register, register )
						HADDPS( register, register )
				else:
					def SIMD_ZERO(register):
						XORPD( register, register )
					def SIMD_REDUCE(register):
						HADDPD( register, register )

				def PROCESS_SCALAR(xmm_acc):
					xmm_temp = SSERegister()
					SCALAR_LOAD( xmm_temp, [xPointer] )
					SCALAR_MUL( xmm_temp, xmm_temp )
					SCALAR_ADD( xmm_acc, xmm_temp )

				SIMD_ZERO( xmm8 )
				SIMD_ZERO( xmm9 )
				SIMD_ZERO( xmm10 )
				SIMD_ZERO( xmm11 )
				SIMD_ZERO( xmm12 )
				SIMD_ZERO( xmm13 )
				SIMD_ZERO( xmm14 )
				SIMD_ZERO( xmm15 )

				LABEL( "xM16" )
				TEST( xPointer, 15)
				JZ( "xA16" )

				PROCESS_SCALAR( xmm0 )
				ADD( xPointer, x_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				JMP( "xM16" )

				LABEL( "xA16" )
				SUB( length, 128 / x_size )
				JB( "xA16_restore" )

				SIMD_LOAD( xmm0, [xPointer] )
				SIMD_LOAD( xmm1, [xPointer + 16] )
				SIMD_LOAD( xmm2, [xPointer + 32] )
				SIMD_LOAD( xmm3, [xPointer + 48] )
				SIMD_LOAD( xmm4, [xPointer + 64] )
				SIMD_MUL( xmm0, xmm0 )
				SIMD_LOAD( xmm5, [xPointer + 80] )
				SIMD_MUL( xmm1, xmm1 )
				SIMD_LOAD( xmm6, [xPointer + 96] )
				SIMD_MUL( xmm2, xmm2 )
				SIMD_LOAD( xmm7, [xPointer + 112] )
				SIMD_MUL( xmm3, xmm3 )
				SUB( xPointer, -128 )

				SUB( length, 128 / x_size )
				JB( "skip_SWP" )

				ALIGN( 16 )
				LABEL( "xA16_loop" )

				SIMD_ADD( xmm8, xmm0 )
				SIMD_LOAD( xmm0, [xPointer] )
				SIMD_MUL( xmm4, xmm4 )

				SIMD_ADD( xmm9, xmm1 )
				SIMD_LOAD( xmm1, [xPointer + 16] )
				SIMD_MUL( xmm5, xmm5 )

				SIMD_ADD( xmm10, xmm2 )
				SIMD_LOAD( xmm2, [xPointer + 32] )
				SIMD_MUL( xmm6, xmm6 )

				SIMD_ADD( xmm11, xmm3 )
				SIMD_LOAD( xmm3, [xPointer + 48] )
				SIMD_MUL( xmm7, xmm7 )

				SIMD_ADD( xmm12, xmm4 )
				SIMD_LOAD( xmm4, [xPointer + 64] )
				SIMD_MUL( xmm0, xmm0 )

				SIMD_ADD( xmm13, xmm5 )
				SIMD_LOAD( xmm5, [xPointer + 80] )
				SIMD_MUL( xmm1, xmm1 )

				SIMD_ADD( xmm14, xmm6 )
				SIMD_LOAD( xmm6, [xPointer + 96] )
				SIMD_MUL( xmm2, xmm2 )

				SIMD_ADD( xmm15, xmm7 )
				SIMD_LOAD( xmm7, [xPointer + 112] )
				SIMD_MUL( xmm3, xmm3 )

				SUB( xPointer, -128 )
				SUB( length, 128 / x_size )
				JAE( "xA16_loop" )

				LABEL( "skip_SWP" )

				SIMD_ADD( xmm8, xmm0 )
				SIMD_MUL( xmm4, xmm4 )
				SIMD_ADD( xmm9, xmm1 )
				SIMD_MUL( xmm5, xmm5 )
				SIMD_ADD( xmm10, xmm2 )
				SIMD_MUL( xmm6, xmm6 )
				SIMD_ADD( xmm11, xmm3 )
				SIMD_MUL( xmm7, xmm7 )
				SIMD_ADD( xmm12, xmm4 )
				SIMD_ADD( xmm13, xmm5 )
				SIMD_ADD( xmm14, xmm6 )
				SIMD_ADD( xmm15, xmm7 )

				LABEL( "xA16_restore" )
				ADD( length, 128 / x_size )
				JZ( "return_ok" )
				LABEL( "finalize" )

				PROCESS_SCALAR( xmm0 )
				ADD( xPointer, x_size )
				SUB( length, 1 )
				JNZ( "finalize" )

				LABEL( "return_ok" )

				SIMD_ADD( xmm8, xmm9 )
				SIMD_ADD( xmm10, xmm11 )
				SIMD_ADD( xmm12, xmm13 )
				SIMD_ADD( xmm14, xmm15 )

				SIMD_ADD( xmm8, xmm10 )
				SIMD_ADD( xmm12, xmm14 )

				SIMD_ADD( xmm8, xmm12 )

				SIMD_REDUCE( xmm8 )
				SCALAR_STORE( [yPointer], xmm8 )

				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def SumSquares_Vf_Sf_implementation_SandyBridge(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumSquares']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not x_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)

				codegen.begin_function(function_signature, arguments, 'SandyBridge')
				xPointer = GeneralPurposeRegister64()
				yPointer = GeneralPurposeRegister64()
				length = GeneralPurposeRegister64()

				LOAD.PARAMETER( xPointer, x_argument )
				LOAD.PARAMETER( yPointer, y_argument )
				LOAD.PARAMETER( length, length_argument )

				if x_size == 4:
					SCALAR_LOAD = VMOVSS
					SCALAR_ADD = VADDSS
					SCALAR_MUL = VMULSS
					SCALAR_STORE = VMOVSS

					SIMD_LOAD = VMOVAPS
					SIMD_ADD = VADDPS
					SIMD_MUL = VMULPS

					def SIMD_ZERO(register):
						VXORPS(register, register, register)
					def SIMD_REDUCE(register):
						VHADDPS(register, register, register)
						VHADDPS(register, register, register)
				else:
					SCALAR_LOAD = VMOVSD
					SCALAR_ADD = VADDSD
					SCALAR_MUL = VMULSD
					SCALAR_STORE = VMOVSD

					SIMD_LOAD = VMOVAPD
					SIMD_ADD = VADDPD
					SIMD_MUL = VMULPD

					def SIMD_ZERO(register):
						VXORPD(register, register, register)
					def SIMD_REDUCE(register):
						VHADDPD(register, register, register)

				def process_scalar():
					SCALAR_LOAD( xmm0, [xPointer] )
					SCALAR_MUL( xmm0, xmm0 )
					SCALAR_ADD( xmm8, xmm0 )

				SIMD_ZERO(ymm8)
				SIMD_ZERO(ymm9)
				SIMD_ZERO(ymm10)
				SIMD_ZERO(ymm11)
				SIMD_ZERO(ymm12)
				SIMD_ZERO(ymm13)
				SIMD_ZERO(ymm14)
				SIMD_ZERO(ymm15)

				LABEL( "xM32" )
				TEST( xPointer, 31)
				JZ( "xA32" )

				process_scalar()
				ADD( xPointer, x_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				JMP( "xM32" )

				LABEL( "xA32" )
				SUB( length, 256 / x_size )
				JB( "xA32_restore" )

				SIMD_LOAD( ymm0, [xPointer] )
				SIMD_LOAD( ymm1, [xPointer + 32] )
				SIMD_LOAD( ymm2, [xPointer + 64] )
				SIMD_LOAD( ymm3, [xPointer + 96] )
				SIMD_LOAD( ymm4, [xPointer + 128] )
				SIMD_MUL( ymm0, ymm0 )
				SIMD_LOAD( ymm5, [xPointer + 160] )
				SIMD_MUL( ymm1, ymm1 )
				SIMD_LOAD( ymm6, [xPointer + 192] )
				SIMD_MUL( ymm2, ymm2 )
				SIMD_LOAD( ymm7, [xPointer + 224] )
				SIMD_MUL( ymm3, ymm3 )
				ADD( xPointer, 256 )

				SUB( length, 256 / x_size )
				JB( "skip_SWP" )

				ALIGN( 16 )
				LABEL( "xA32_loop" )

				SIMD_ADD( ymm8, ymm0 )
				SIMD_LOAD( ymm0, [xPointer] )
				SIMD_MUL( ymm4, ymm4 )

				SIMD_ADD( ymm9, ymm1 )
				SIMD_LOAD( ymm1, [xPointer + 32] )
				SIMD_MUL( ymm5, ymm5 )

				SIMD_ADD( ymm10, ymm2 )
				SIMD_LOAD( ymm2, [xPointer + 64] )
				SIMD_MUL( ymm6, ymm6 )

				SIMD_ADD( ymm11, ymm3 )
				SIMD_LOAD( ymm3, [xPointer + 96] )
				SIMD_MUL( ymm7, ymm7 )

				SIMD_ADD( ymm12, ymm4 )
				SIMD_LOAD( ymm4, [xPointer + 128] )
				SIMD_MUL( ymm0, ymm0 )

				SIMD_ADD( ymm13, ymm5 )
				SIMD_LOAD( ymm5, [xPointer + 160] )
				SIMD_MUL( ymm1, ymm1 )

				SIMD_ADD( ymm14, ymm6 )
				SIMD_LOAD( ymm6, [xPointer + 192] )
				SIMD_MUL( ymm2, ymm2 )

				SIMD_ADD( ymm15, ymm7 )
				SIMD_LOAD( ymm7, [xPointer + 224] )
				SIMD_MUL( ymm3, ymm3 )

				ADD( xPointer, 256 )
				SUB( length, 256 / x_size )
				JAE( "xA32_loop" )

				LABEL( "skip_SWP" )

				SIMD_ADD( ymm8, ymm0 )
				SIMD_MUL( ymm4, ymm4 )
				SIMD_ADD( ymm9, ymm1 )
				SIMD_MUL( ymm5, ymm5 )
				SIMD_ADD( ymm10, ymm2 )
				SIMD_MUL( ymm6, ymm6 )
				SIMD_ADD( ymm11, ymm3 )
				SIMD_MUL( ymm7, ymm7 )
				SIMD_ADD( ymm12, ymm4 )
				SIMD_ADD( ymm13, ymm5 )
				SIMD_ADD( ymm14, ymm6 )
				SIMD_ADD( ymm15, ymm7 )

				LABEL( "xA32_restore" )

				SIMD_ADD( ymm8, ymm9 )
				SIMD_ADD( ymm10, ymm11 )
				SIMD_ADD( ymm12, ymm13 )
				SIMD_ADD( ymm14, ymm15 )

				SIMD_ADD( ymm8, ymm10 )
				SIMD_ADD( ymm12, ymm14 )

				SIMD_ADD( ymm8, ymm12 )

				VEXTRACTF128( xmm9, ymm8, 1 )
				SIMD_ADD( xmm8, xmm9 )

				SIMD_REDUCE( xmm8 )

				ADD( length, 256 / x_size )
				JZ( "return_ok" )
				LABEL( "finalize" )

				process_scalar()
				ADD( xPointer, x_size )
				SUB( length, 1 )
				JNZ( "finalize" )

				LABEL( "return_ok" )

				SCALAR_STORE( [yPointer], xmm8 )

				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def SumSquares_Vf_Sf_implementation_Bulldozer(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['SumSquares']:
				x_argument, y_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()

				if not x_type.is_floating_point():
					return

				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)

				codegen.begin_function(function_signature, arguments, 'Bulldozer')

				xPointer = GeneralPurposeRegister64()
				yPointer = GeneralPurposeRegister64()
				length = GeneralPurposeRegister64()

				LOAD.PARAMETER( xPointer, x_argument )
				LOAD.PARAMETER( yPointer, y_argument )
				LOAD.PARAMETER( length, length_argument )

				if x_size == 4:
					SCALAR_LOAD = VMOVSS
					SCALAR_ADD = VADDSS
					SCALAR_MUL = VMULSS
					SCALAR_STORE = VMOVSS

					SIMD_LOAD = VMOVAPS
					SIMD_ADD = VADDPS
					SIMD_FMA = lambda dst, src: VFMADDPS(dst, src, src, dst)

					def SIMD_ZERO(register):
						VXORPS(register, register, register)
					def SIMD_REDUCE(register):
						VHADDPS(register, register, register)
						VHADDPS(register, register, register)
				else:
					SCALAR_LOAD = VMOVSD
					SCALAR_ADD = VADDSD
					SCALAR_MUL = VMULSD
					SCALAR_STORE = VMOVSD

					SIMD_LOAD = VMOVAPD
					SIMD_ADD = VADDPD
					SIMD_FMA = lambda dst, src: VFMADDPD(dst, src, src, dst)

					def SIMD_ZERO(register):
						VXORPD(register, register, register)
					def SIMD_REDUCE(register):
						VHADDPD(register, register, register)

				def process_scalar():
					SCALAR_LOAD( xmm0, [xPointer] )
					SCALAR_MUL( xmm0, xmm0 )
					SCALAR_ADD( xmm8, xmm0 )

				SIMD_ZERO(ymm8)
				SIMD_ZERO(ymm9)
				SIMD_ZERO(ymm10)
				SIMD_ZERO(ymm11)
				SIMD_ZERO(ymm12)
				SIMD_ZERO(ymm13)
				SIMD_ZERO(ymm14)
				SIMD_ZERO(ymm15)

				LABEL( "xM16" )
				TEST( xPointer, 15)
				JZ( "xA16" )

				process_scalar()
				ADD( xPointer, x_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				JMP( "xM16" )

				LABEL( "xA16" )
				SUB( length, 128 / x_size )
				JB( "xA16_restore" )

				SIMD_LOAD( xmm0, [xPointer] )
				SIMD_LOAD( xmm1, [xPointer + 16] )
				SIMD_LOAD( xmm2, [xPointer + 32] )
				SIMD_LOAD( xmm3, [xPointer + 48] )
				SIMD_LOAD( xmm4, [xPointer + 64] )
				SIMD_LOAD( xmm5, [xPointer + 80] )
				SIMD_LOAD( xmm6, [xPointer + 96] )
				SIMD_LOAD( xmm7, [xPointer + 112] )
				ADD( xPointer, 128 )

				SUB( length, 128 / x_size )
				JB( "skip_SWP" )

				ALIGN( 16 )
				LABEL( "xA16_loop" )

				SIMD_FMA( xmm8, xmm0 )
				SIMD_LOAD( xmm0, [xPointer] )

				SIMD_FMA( xmm9, xmm1 )
				SIMD_LOAD( xmm1, [xPointer + 16] )

				SIMD_FMA( xmm10, xmm2 )
				SIMD_LOAD( xmm2, [xPointer + 32] )

				SIMD_FMA( xmm11, xmm3 )
				SIMD_LOAD( xmm3, [xPointer + 48] )

				SIMD_FMA( xmm12, xmm4 )
				SIMD_LOAD( xmm4, [xPointer + 64] )

				SIMD_FMA( xmm13, xmm5 )
				SIMD_LOAD( xmm5, [xPointer + 80] )

				SIMD_FMA( xmm14, xmm6 )
				SIMD_LOAD( xmm6, [xPointer + 96] )

				SIMD_FMA( xmm15, xmm7 )
				SIMD_LOAD( xmm7, [xPointer + 112] )

				ADD( xPointer, 128 )
				SUB( length, 128 / x_size )
				JAE( "xA16_loop" )

				LABEL( "skip_SWP" )

				SIMD_FMA( xmm8, xmm0 )
				SIMD_FMA( xmm9, xmm1 )
				SIMD_FMA( xmm10, xmm2 )
				SIMD_FMA( xmm11, xmm3 )
				SIMD_FMA( xmm12, xmm4 )
				SIMD_FMA( xmm13, xmm5 )
				SIMD_FMA( xmm14, xmm6 )
				SIMD_FMA( xmm15, xmm7 )

				LABEL( "xA16_restore" )

				SIMD_ADD( xmm8, xmm9 )
				SIMD_ADD( xmm10, xmm11 )
				SIMD_ADD( xmm12, xmm13 )
				SIMD_ADD( xmm14, xmm15 )

				SIMD_ADD( xmm8, xmm10 )
				SIMD_ADD( xmm12, xmm14 )

				SIMD_ADD( xmm8, xmm12 )

				SIMD_REDUCE( xmm8 )

				ADD( length, 128 / x_size )
				JZ( "return_ok" )
				LABEL( "finalize" )

				process_scalar()
				ADD( xPointer, x_size )
				SUB( length, 1 )
				JNZ( "finalize" )

				LABEL( "return_ok" )

				SCALAR_STORE( [yPointer], xmm8 )

				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def DotProduct_VfVf_Sf_implementation_SandyBridge(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['DotProduct']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if not z_type.is_floating_point():
					return

				x_argument = arguments[0]
				y_argument = arguments[1]
				z_argument = arguments[2]
				length_argument = arguments[3]

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()


				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				codegen.begin_function(function_signature, arguments, 'SandyBridge')

				xPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( xPointer, x_argument )
				
				yPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( yPointer, y_argument )
				
				zPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( zPointer, z_argument )

				length = GeneralPurposeRegister64()
				LOAD.PARAMETER( length, length_argument )

				if x_size == 4:
					SCALAR_LOAD = VMOVSS
					SCALAR_MUL = VMULSS
					SCALAR_STORE = VMOVSS
					SIMD_LOAD = VMOVUPS
					SIMD_ADD = VADDPS
					SIMD_MUL = VMULPS
					def SIMD_ZERO(register):
						VXORPS(register, register)
					def SIMD_REDUCE(register):
						VHADDPS(register, register)
						VHADDPS(register, register)
				else:
					SCALAR_LOAD = VMOVSD
					SCALAR_MUL = VMULSD
					SCALAR_STORE = VMOVSD
					SIMD_LOAD = VMOVUPD
					SIMD_ADD = VADDPD
					SIMD_MUL = VMULPD
					def SIMD_ZERO(register):
						VXORPD(register, register)
					def SIMD_REDUCE(register):
						VHADDPD(register, register)

				def PROCESS_SCALAR(ymm_acc, xPointer, yPointer):
					xmm_temp = SSERegister()
					
					SCALAR_LOAD( xmm_temp, [xPointer] )
					SCALAR_MUL( xmm_temp, [yPointer] )
					SIMD_ADD( ymm_acc, xmm_temp.get_hword() )

				def PROCESS_BATCH(ymm_acc, xPointer, yPointer):
					for i in range(len(ymm_acc)):
						ymm_temp = AVXRegister()
						SIMD_LOAD( ymm_temp, [yPointer + i * 32] )
						SIMD_MUL( ymm_temp, [xPointer + i * 32] )
						SIMD_ADD( ymm_acc[i], ymm_temp )

				sourceAlignment = 32
				batchRegisters = 4
				batchElements = batchRegisters * 4

				ymm_acc = [AVXRegister() for i in range(batchRegisters)]
				for i in range(batchRegisters):
					SIMD_ZERO( ymm_acc[i].get_oword() )

				CMP( length, 0 )
				JE( "return_ok" )

				TEST( xPointer, sourceAlignment - 1 )
				JZ( "source_32b_aligned" )

				LABEL( "source_32b_misaligned" )
				PROCESS_SCALAR( ymm_acc[0], xPointer, yPointer )
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				TEST( xPointer, sourceAlignment - 1 )
				JNZ( "source_32b_misaligned" )

				LABEL( "source_32b_aligned" )
				SUB( length, batchElements )
				JB( 'process_restore' )

				ALIGN( 16 )
				LABEL( "process_batch" )
				PROCESS_BATCH( ymm_acc, xPointer, yPointer )
				ADD( xPointer, batchElements * x_size )
				ADD( yPointer, batchElements * y_size )
				SUB( length, batchElements )
				JAE( "process_batch" )

				LABEL( "process_restore" )
				ADD( length, batchElements )
				JZ( "reduce" )
				
				LABEL( "process_single" )
				PROCESS_SCALAR(ymm_acc[0], xPointer, yPointer)
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JNZ( "process_single" )

				LABEL( "reduce" )
				for i in range(0, batchRegisters, 2):
					SIMD_ADD(ymm_acc[i], ymm_acc[i + 1])
				for i in range(0, batchRegisters, 4):
					SIMD_ADD(ymm_acc[i], ymm_acc[i + 2])

				xmm_temp = SSERegister()
				VEXTRACTF128( xmm_temp, ymm_acc[0], 1 )
				xmm_acc = ymm_acc[0].get_oword() 
				SIMD_ADD( xmm_acc, xmm_acc, xmm_temp )
				SIMD_REDUCE( xmm_acc )
				SCALAR_STORE( [zPointer], xmm_acc )

				LABEL( "return_ok" )
				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def DotProduct_VfVf_Sf_implementation_Haswell(codegen, function_signature, module, function, arguments):
	if codegen.abi.name in ['x64-ms', 'x64-sysv']:
		if module == 'Core':
			if function in ['DotProduct']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if not z_type.is_floating_point():
					return

				x_argument = arguments[0]
				y_argument = arguments[1]
				z_argument = arguments[2]
				length_argument = arguments[3]

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()


				x_size = x_type.get_size(codegen.abi)
				y_size = y_type.get_size(codegen.abi)
				z_size = z_type.get_size(codegen.abi)

				codegen.begin_function(function_signature, arguments, 'Haswell')

				xPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( xPointer, x_argument )
				
				yPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( yPointer, y_argument )
				
				zPointer = GeneralPurposeRegister64()
				LOAD.PARAMETER( zPointer, z_argument )

				length = GeneralPurposeRegister64()
				LOAD.PARAMETER( length, length_argument )

				if x_size == 4:
					SCALAR_LOAD = VMOVSS
					SCALAR_STORE = VMOVSS
					SIMD_LOAD = VMOVUPS
					SIMD_ADD = VADDPS
					SIMD_FMA = VFMADD231PS
					def SIMD_ZERO(register):
						VXORPS(register, register)
					def SIMD_REDUCE(register):
						VHADDPS(register, register)
						VHADDPS(register, register)
				else:
					SCALAR_LOAD = VMOVSD
					SCALAR_STORE = VMOVSD
					SIMD_LOAD = VMOVUPD
					SIMD_ADD = VADDPD
					SIMD_FMA = VFMADD231PD
					def SIMD_ZERO(register):
						VXORPD(register, register)
					def SIMD_REDUCE(register):
						VHADDPD(register, register)

				def PROCESS_SCALAR(ymm_acc, xPointer, yPointer):
					ymm_x = AVXRegister()
					SCALAR_LOAD( ymm_x.get_oword(), [xPointer] )

					ymm_y = AVXRegister()
					SCALAR_LOAD( ymm_y.get_oword(), [yPointer] )

					SIMD_FMA( ymm_acc, ymm_x, ymm_y, ymm_acc )

				def PROCESS_BATCH(ymm_acc, xPointer, yPointer):
					for i in range(len(ymm_acc)):
						ymm_temp = AVXRegister()
						SIMD_LOAD( ymm_temp, [yPointer + i * 32] )
						SIMD_FMA( ymm_acc[i], ymm_temp, [xPointer + i * 32], ymm_acc[i] )

				sourceAlignment = 32
				batchRegisters = 4
				batchElements = batchRegisters * 4

				ymm_acc = [AVXRegister() for i in range(batchRegisters)]
				for i in range(batchRegisters):
					SIMD_ZERO( ymm_acc[i].get_oword() )

				CMP( length, 0 )
				JE( "return_ok" )

				TEST( xPointer, sourceAlignment - 1 )
				JZ( "source_32b_aligned" )

				LABEL( "source_32b_misaligned" )
				PROCESS_SCALAR( ymm_acc[0], xPointer, yPointer )
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				TEST( xPointer, sourceAlignment - 1 )
				JNZ( "source_32b_misaligned" )

				LABEL( "source_32b_aligned" )
				SUB( length, batchElements )
				JB( 'process_restore' )

				ALIGN( 16 )
				LABEL( "process_batch" )
				PROCESS_BATCH( ymm_acc, xPointer, yPointer )
				ADD( xPointer, batchElements * x_size )
				ADD( yPointer, batchElements * y_size )
				SUB( length, batchElements )
				JAE( "process_batch" )

				LABEL( "process_restore" )
				ADD( length, batchElements )
				JZ( "reduce" )
				
				LABEL( "process_single" )
				PROCESS_SCALAR(ymm_acc[0], xPointer, yPointer)
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JNZ( "process_single" )

				LABEL( "reduce" )
				for i in range(0, batchRegisters, 2):
					SIMD_ADD(ymm_acc[i], ymm_acc[i + 1])
				for i in range(0, batchRegisters, 4):
					SIMD_ADD(ymm_acc[i], ymm_acc[i + 2])

				xmm_temp = SSERegister()
				VEXTRACTF128( xmm_temp, ymm_acc[0], 1 )
				xmm_acc = ymm_acc[0].get_oword() 
				SIMD_ADD( xmm_acc, xmm_acc, xmm_temp )
				SIMD_REDUCE( xmm_acc )
				SCALAR_STORE( [zPointer], xmm_acc )

				LABEL( "return_ok" )
				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def DotProduct_VfVf_Sf_implementation_Nehalem(codegen, function_signature, module, function, arguments):
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

				codegen.begin_function(function_signature, arguments, 'Nehalem')
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
					SCALAR_ADD = ADDSS
					SCALAR_MUL = MULSS
					SCALAR_STORE = MOVSS
					SIMD_LOAD = MOVUPS
					SIMD_ADD = ADDPS
					SIMD_MUL = MULPS
					def SIMD_ZERO(register):
						XORPS(register, register)
					def SIMD_REDUCE(register):
						HADDPS(register, register)
						HADDPS(register, register)
				else:
					SCALAR_LOAD = MOVSD
					SCALAR_ADD = ADDSD
					SCALAR_MUL = MULSD
					SCALAR_STORE = MOVSD
					SIMD_LOAD = MOVUPD
					SIMD_ADD = ADDPD
					SIMD_MUL = MULPD
					def SIMD_ZERO(register):
						XORPD( register, register )
					def SIMD_REDUCE(register):
						HADDPD( register, register )

				def PROCESS_SCALAR(xmm_acc, xPointer, yPointer):
					xmm_temp = SSERegister()
					
					SCALAR_LOAD( xmm_temp, [xPointer] )
					SCALAR_MUL( xmm_temp, [yPointer] )
					SCALAR_ADD( xmm_acc, xmm_temp )

				def PROCESS_BATCH(xmm_acc, xPointer, yPointer):
					for i in range(len(xmm_acc)):
						xmm_temp = SSERegister()
						SIMD_LOAD( xmm_temp, [yPointer + i * 16] )
						SIMD_MUL( xmm_temp, [xPointer + i * 16] )
						SIMD_ADD( xmm_acc[i], xmm_temp )

				sourceAlignment = 16
				batchRegisters = 4
				batchElements = batchRegisters * 2

				xmm_acc = [SSERegister() for i in range(batchRegisters)]
				for i in range(batchRegisters):
					SIMD_ZERO( xmm_acc[i] )

				CMP( length, 0 )
				JE( "return_ok" )

				TEST( xPointer, sourceAlignment - 1 )
				JZ( "source_16b_aligned" )

				LABEL( "source_16b_misaligned" )
				PROCESS_SCALAR( xmm_acc[0], xPointer, yPointer )
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				TEST( xPointer, sourceAlignment - 1 )
				JNZ( "source_16b_misaligned" )

				LABEL( "source_16b_aligned" )
				SUB( length, batchElements )
				JB( 'process_restore' )

				ALIGN( 16 )
				LABEL( "process_batch" )
				PROCESS_BATCH( xmm_acc, xPointer, yPointer )
				ADD( xPointer, batchElements * x_size )
				ADD( yPointer, batchElements * y_size )
				SUB( length, batchElements )
				JAE( "process_batch" )

				LABEL( "process_restore" )
				ADD( length, batchElements )
				JZ( "reduce" )
				
				LABEL( "process_single" )
				PROCESS_SCALAR(xmm_acc[0], xPointer, yPointer)
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JNZ( "process_single" )

				LABEL( "reduce" )
				for i in range(0, batchRegisters, 2):
					SIMD_ADD(xmm_acc[i], xmm_acc[i + 1])
				for i in range(0, batchRegisters, 4):
					SIMD_ADD(xmm_acc[i], xmm_acc[i + 2])

				SIMD_REDUCE( xmm_acc[0] )
				SCALAR_STORE( [zPointer], xmm_acc[0] )

				LABEL( "return_ok" )
				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def DotProduct_VfVf_Sf_implementation_Bulldozer(codegen, function_signature, module, function, arguments):
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

				codegen.begin_function(function_signature, arguments, 'Bulldozer')
				xPointer = GeneralPurposeRegister64()
				yPointer = GeneralPurposeRegister64()
				zPointer = GeneralPurposeRegister64()
				length = GeneralPurposeRegister64()

				LOAD.PARAMETER( xPointer, x_argument )
				LOAD.PARAMETER( yPointer, y_argument )
				LOAD.PARAMETER( zPointer, z_argument )
				LOAD.PARAMETER( length, length_argument )

				if x_size == 4:
					SCALAR_LOAD = VMOVSS
					SCALAR_FMA = VFMADDSS
					SCALAR_STORE = VMOVSS
					SIMD_LOAD = VMOVUPS
					SIMD_FMA = VFMADDPS
					SIMD_ADD = VADDPS
					def SIMD_ZERO(register):
						VXORPS( register, register )
					def SIMD_REDUCE(xmm_partial_sum):
						VHADDPS( xmm_partial_sum, xmm_partial_sum )
						VHADDPS( xmm_partial_sum, xmm_partial_sum )
				else:
					SCALAR_LOAD = VMOVSD
					SCALAR_FMA = VFMADDSD
					SCALAR_STORE = VMOVSD
					SIMD_LOAD = VMOVUPD
					SIMD_FMA = VFMADDPD
					SIMD_ADD = VADDPD
					def SIMD_ZERO(register):
						VXORPD( register, register )
					def SIMD_REDUCE(xmm_partial_sum):
						xmm_temp = SSERegister()
						VUNPCKHPD( xmm_temp, xmm_partial_sum, xmm_partial_sum )
						VADDSD( xmm_partial_sum, xmm_partial_sum, xmm_temp )

				def PROCESS_SCALAR(xmm_acc, xPointer, yPointer):
					xmm_x = SSERegister()
					SCALAR_LOAD( xmm_x, [xPointer] )
					xmm_y = SSERegister()
					SCALAR_LOAD( xmm_y, [yPointer] )
					
					SIMD_FMA( xmm_acc, xmm_x, xmm_y, xmm_acc )

				def PROCESS_BATCH(xmm_acc, xPointer, yPointer):
					for i in range(len(xmm_acc)):
						xmm_temp = SSERegister()
						SIMD_LOAD( xmm_temp, [yPointer + i * 16] )
						SIMD_FMA( xmm_acc[i], xmm_temp, [xPointer + i * 16], xmm_acc[i] )

				sourceAlignment = 16
				batchRegisters = 6
				batchElements = batchRegisters * 2

				xmm_acc = [SSERegister() for i in range(batchRegisters)]
				for i in range(batchRegisters):
					SIMD_ZERO( xmm_acc[i] )

				CMP( length, 0 )
				JE( "return_ok" )

				TEST( xPointer, sourceAlignment - 1 )
				JZ( "source_%db_aligned" % sourceAlignment )

				LABEL( "source_%db_misaligned" % sourceAlignment )
				PROCESS_SCALAR(xmm_acc[0], xPointer, yPointer)
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JZ( "return_ok" )
				TEST( xPointer, sourceAlignment - 1 )
				JNZ( "source_%db_misaligned" % sourceAlignment )

				LABEL( "source_%db_aligned" % sourceAlignment )
				SUB( length, batchElements )
				JB( 'process_restore' )

				ALIGN( 16 )
				LABEL( "process_batch" )
				PROCESS_BATCH(xmm_acc, xPointer, yPointer)
				ADD( xPointer, batchElements * x_size )
				ADD( yPointer, batchElements * y_size )
				SUB( length, batchElements )
				JAE( "process_batch" )

				LABEL( "process_restore" )
				ADD( length, batchElements )
				JZ( "reduce" )
				
				LABEL( "process_single" )
				PROCESS_SCALAR(xmm_acc[0], xPointer, yPointer)
				ADD( xPointer, x_size )
				ADD( yPointer, y_size )
				SUB( length, 1 )
				JNZ( "process_single" )

				LABEL( "reduce" )
				for i in range(1, batchRegisters, 2):
					SIMD_ADD( xmm_acc[i - 1], xmm_acc[i] )
				for i in range(2, batchRegisters, 4):
					SIMD_ADD( xmm_acc[i - 2], xmm_acc[i] )
				for i in range(4, batchRegisters, 8):
					SIMD_ADD( xmm_acc[i - 4], xmm_acc[i] )

				SIMD_REDUCE( xmm_acc[0] )
				SCALAR_STORE( [zPointer], xmm_acc[0] )

				LABEL( "return_ok" )
				XOR(eax, eax)
				LABEL( "return" )
				RET()

				return codegen.end_function()

def DotProduct_V64fV64f_S64f_implementation_Bonnell(codegen, function_signature, module, function, arguments):
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

				codegen.begin_function(function_signature, arguments, 'Bonnell')

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

				return codegen.end_function()
