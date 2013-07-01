#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

__author__ = 'Marat'

from peachpy.arm import *

def SCALAR_INT_ADD_SUB_MUL(xPointer, yPointer, zPointer, input_type, output_type, operation):
	acc = GeneralPurposeRegister()
	LOAD.ELEMENT( acc, [xPointer], input_type, increment_pointer = True )
	temp = GeneralPurposeRegister()
	LOAD.ELEMENT( temp, [yPointer], input_type, increment_pointer = True )

	COMPUTE = { 'Add': ADD, 'Subtract': SUB }[operation]
	COMPUTE( acc, temp )

	STORE.ELEMENT( [zPointer], acc, output_type, increment_pointer = True )

def PipelineMap_VXusfVXusf_VYusf(xPointer, yPointer, zPointer, length, batch_elements, input_type, output_type, scalar_function, instruction_columns, instruction_offsets):
	# Check that we have an offset for each instruction column
	assert len(instruction_columns) == len(instruction_offsets)

	max_instructions  = max(map(len, instruction_columns))
	
	return_ok                 = Label("return_ok")
	return_null_pointer       = Label("return_null_pointer")
	return_misaligned_pointer = Label("return_misaligned_pointer")
	return_any                = Label("return")
	batch_process_finish      = Label("batch_process_finish")
	process_single            = Label("process_single")
	process_batch             = Label("process_batch")
	process_batch_prologue    = Label("process_batch_prologue") 
	process_batch_epilogue    = Label("process_batch_epilogue") 

	# Check parameters
	TST( xPointer, xPointer )
	BEQ( return_null_pointer )
	
	TST( xPointer, input_type.get_size() - 1 )
	BNE( return_misaligned_pointer )
	
	TST( yPointer, yPointer )
	BEQ( return_null_pointer )
	
	TST( yPointer, input_type.get_size() - 1 )
	BNE( return_misaligned_pointer )

	TST( zPointer, zPointer )
	BEQ( return_null_pointer )
	
	TST( zPointer, output_type.get_size() - 1 )
	BNE( return_misaligned_pointer )

	# If length is zero, return immediately
	TST( length, length )
	BEQ( return_ok )

	SUBS( length, batch_elements )
	BLO( batch_process_finish )

	LABEL( process_batch_prologue )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			if i >= instruction_offset:
				Function.get_current().add_instruction(instruction_column[i - instruction_offset])

	SUBS( length, batch_elements )
	BLO( process_batch_epilogue )

	LABEL( process_batch )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			Function.get_current().add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

	SUBS( length, batch_elements )
	BHS( process_batch )

	LABEL( process_batch_epilogue )
	for i in range(max_instructions):
		for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
			if i < instruction_offset:
				Function.get_current().add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

	LABEL( batch_process_finish )
	ADDS( length, batch_elements )
	BEQ( return_ok )

	LABEL( process_single )
	scalar_function(xPointer, yPointer, zPointer)
	SUBS( length, 1 )
	BNE( process_single )

	LABEL( return_ok )
	MOV( r0, 0 )
	
	LABEL( return_any )
	RETURN()

	LABEL( return_null_pointer )
	MOV( r0, 1 )
	B( return_any )
	
	LABEL( return_misaligned_pointer )
	MOV( r0, 2 )
	B( return_any )

def AddSub_VXusVXus_VXus_NEON(codegen, function_signature, module, function, arguments, error_diagnostics_mode = False):
	if codegen.abi.name in ['arm-softeabi', 'arm-hardeabi']:
		if module == 'Core':
			if function in ['Add', 'Subtract']:
				x_argument, y_argument, z_argument, length_argument = tuple(arguments)

				x_type = x_argument.get_type().get_primitive_type()
				y_type = y_argument.get_type().get_primitive_type()
				z_type = z_argument.get_type().get_primitive_type()

				if any(type.is_floating_point() for type in (x_type, y_type, z_type)):
					return

				if len(set([x_type, y_type, z_type])) != 1:
					return
				else:
					ctype = x_type
					if ctype.get_size() == 8:
						return

				def PROCESS_SCALAR(xPointer, yPointer, zPointer):
					SCALAR_INT_ADD_SUB_MUL(xPointer, yPointer, zPointer, ctype, ctype, function)

				VLOAD  = { 1: VLD1.I8, 2: VLD1.I16, 4: VLD1.I32, 8: VLD1.I64 }[ctype.get_size()]
				VSTORE = { 1: VST1.I8, 2: VST1.I16, 4: VST1.I32, 8: VST1.I64 }[ctype.get_size()]
				if function == 'Add':
					VCOMPUTE = { 1: VADD.I8, 2: VADD.I16, 4: VADD.I32, 8: VADD.I64 }[ctype.get_size()]
				elif function == 'Subtract':
					VCOMPUTE = { 1: VSUB.I8, 2: VSUB.I16, 4: VSUB.I32, 8: VSUB.I64 }[ctype.get_size()]

				with Function(codegen, function_signature, arguments, 'CortexA9', collect_origin = bool(error_diagnostics_mode), check_only = bool(error_diagnostics_mode)):
					xPointer, yPointer, zPointer, length = LOAD.PARAMETERS()
					
					unroll_registers = 6
					register_size    = 16
					batch_elements   = unroll_registers * register_size / ctype.get_size()

					x = [QRegister() for _ in range(unroll_registers)]
					y = [QRegister() for _ in range(unroll_registers)]

					instruction_offsets = (0, 0, 2, 2, 5)
					instruction_columns = [InstructionStream() for _ in range(5)] 
					for i in range(0, unroll_registers, 2):
						with instruction_columns[0]:
							VLOAD( (x[i].get_low_part(), x[i].get_high_part(), x[i+1].get_low_part(), x[i+1].get_high_part()), [xPointer.wb()] )
						with instruction_columns[1]:
							VLOAD( (y[i].get_low_part(), y[i].get_high_part(), y[i+1].get_low_part(), y[i+1].get_high_part()), [yPointer.wb()] )
						with instruction_columns[2]:
							VCOMPUTE( x[i], y[i] )
						with instruction_columns[3]:
							VCOMPUTE( x[i+1], y[i+1] )
						with instruction_columns[4]:
							VSTORE( (x[i].get_low_part(), x[i].get_high_part(), x[i+1].get_low_part(), x[i+1].get_high_part()), [zPointer.wb()] )
				
					PipelineMap_VXusfVXusf_VYusf(xPointer, yPointer, zPointer, length, batch_elements, ctype, ctype, PROCESS_SCALAR, instruction_columns, instruction_offsets)
