#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

import peachpy
import peachpy.codegen
import peachpy.c
import peachpy.java
import peachpy.fortran
import peachpy.csharp
import string
import re

class FunctionArgument(object):
	def __init__(self, name, type = None):
		# Argument name as specified in function signature
		self.declared_name = name
		# Argument type as string as specified in function signature (None if not specified)
		self.declared_type = type
		# The following member variables contain a list of tuples (name, type)
		# with the expansion of this Yeppp! function argument in different contexts and languages

		# Arguments used for public C headers 
		self.c_public_arguments = list()
		# Arguments used for internal C code (e.g. function implementation)
		self.c_private_arguments = list()
		# Arguments used for Java bindings (these map 1-to-1 to JNI types for the C part of bindings)
		self.java_arguments = list()
		# Arguments used for FORTRAN bindings (almost the same as public C arguments)
		self.fortran_arguments = list()
		# Arguments used for DllImport declaration in C#
		self.csharp_dllimport_arguments = list()
		# Arguments used for C# bindings with pointers
		self.csharp_unsafe_arguments = list()
		# Arguments used for C# bindings without pointers
		self.csharp_safe_arguments = list()
		# True if the argument is converted to function return value in Java/C# bindings
		self.is_return_argument = False
		# True if the argument specifies the length of an array argument
		self.is_length_argument = False

	def is_automatic(self):
		# True is the argument type is deduced from function signature
		return self.declared_type is None

	def get_name(self):
		return self.declared_name

	def get_c_public_name(self, index = None):
		if index is None:
			if len(self.c_public_arguments) == 1:
				return self.c_public_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple public C arguments" % self.get_name())
		else:
			return self.c_public_arguments[index].name

	def get_c_public_type(self, index = None):
		if index is None:
			if len(self.c_public_arguments) == 1:
				return self.c_public_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple public C arguments" % self.get_name())
		else:
			return self.c_public_arguments[index].type

	def get_c_private_name(self, index = None):
		if index is None:
			if len(self.c_private_arguments) == 1:
				return self.c_private_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple private C arguments" % self.get_name())
		else:
			return self.c_private_arguments[index].name

	def get_c_private_type(self, index = None):
		if index is None:
			if len(self.c_private_arguments) == 1:
				return self.c_private_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple private C arguments" % self.get_name())
		else:
			return self.c_private_arguments[index].type

	def get_java_name(self, index = None):
		if index is None:
			if len(self.java_arguments) == 1:
				return self.java_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple Java arguments" % self.get_name())
		else:
			return self.java_arguments[index].name

	def get_java_type(self, index = None):
		if index is None:
			if len(self.java_arguments) == 1:
				return self.java_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple Java arguments" % self.get_name())
		else:
			return self.java_arguments[index].type

	def get_fortran_name(self, index = None):
		if index is None:
			if len(self.fortran_arguments) == 1:
				return self.fortran_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple FORTRAN arguments" % self.get_name())
		else:
			return self.fortran_arguments[index].name

	def get_fortran_type(self, index = None):
		if index is None:
			if len(self.fortran_arguments) == 1:
				return self.fortran_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple FORTRAN arguments" % self.get_name())
		else:
			return self.fortran_arguments[index].type

	def get_csharp_dllimport_name(self, index = None):
		if index is None:
			if len(self.csharp_dllimport_arguments) == 1:
				return self.csharp_dllimport_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple DllImport C# arguments" % self.get_name())
		else:
			return self.csharp_dllimport_arguments[index].name

	def get_csharp_dllimport_type(self, index = None):
		if index is None:
			if len(self.csharp_dllimport_arguments) == 1:
				return self.csharp_dllimport_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple DllImport C# arguments" % self.get_name())
		else:
			return self.csharp_dllimport_arguments[index].type

	def get_csharp_unsafe_name(self, index = None):
		if index is None:
			if len(self.csharp_unsafe_arguments) == 1:
				return self.csharp_unsafe_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple unsafe C# arguments" % self.get_name())
		else:
			return self.csharp_unsafe_arguments[index].name

	def get_csharp_unsafe_type(self, index = None):
		if index is None:
			if len(self.csharp_unsafe_arguments) == 1:
				return self.csharp_unsafe_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple unsafe C# arguments" % self.get_name())
		else:
			return self.csharp_unsafe_arguments[index].type

	def get_csharp_safe_name(self, index = None):
		if index is None:
			if len(self.csharp_safe_arguments) == 1:
				return self.csharp_safe_arguments[0].name
			else:
				raise ValueError("The function argument %s expands to multiple safe C# arguments" % self.get_name())
		else:
			return self.csharp_safe_arguments[index].name

	def get_csharp_safe_type(self, index = None):
		if index is None:
			if len(self.csharp_safe_arguments) == 1:
				return self.csharp_safe_arguments[0].type
			else:
				raise ValueError("The function argument %s expands to multiple safe C# arguments" % self.get_name())
		else:
			return self.csharp_safe_arguments[index].type


class ExplicitlyTypedFunctionArgument(FunctionArgument):
	def __init__(self, name, type):
		super(ExplicitlyTypedFunctionArgument, self).__init__(name, type)
		c_type = peachpy.c.Type(type)
		self.c_public_arguments = [peachpy.c.Parameter(name, c_type)]
		if c_type.is_pointer():
			raise ValueError("Invalid argument %s: only implicitly types arguments can be of pointer type" % name)
		else:
			self.c_private_arguments = [peachpy.c.Parameter(name, c_type)]
		java_type = c_type.get_java_analog()
		if java_type:
			self.java_arguments = [peachpy.java.Parameter(name, java_type)]
		else:
			self.java_arguments = None
		fortran_type = c_type.get_fortran_iso_c_analog()
		if fortran_type:
			self.fortran_arguments = [peachpy.fortran.Parameter(name, fortran_type, is_input = True, is_output = False)]
		else:
			self.fortran_arguments = None
		csharp_dllimport_type = c_type.get_csharp_analog(use_unsafe_types = True)
		if csharp_dllimport_type:
			self.csharp_dllimport_arguments = [peachpy.csharp.Parameter(name, csharp_dllimport_type, is_output = False)]
		else:
			self.csharp_dllimport_arguments = None
		csharp_unsafe_type = c_type.get_csharp_analog(size_t_analog = "int", ssize_t_analog = "int")
		if csharp_unsafe_type:
			self.csharp_unsafe_arguments = [peachpy.csharp.Parameter(name, csharp_unsafe_type, is_output = False)]
		else:
			self.csharp_unsafe_arguments = None
		csharp_safe_type = c_type.get_csharp_analog(size_t_analog = "int", ssize_t_analog = "int")
		if csharp_safe_type:
			self.csharp_safe_arguments = [peachpy.csharp.Parameter(name, csharp_safe_type, is_output = False)]
		else:
			self.csharp_safe_arguments = None

	def __str__(self):
		return "%s %s" % (self.declared_type, self.declared_name)

class ImplicitlyTypedFunctionArgument(FunctionArgument):
	def __init__(self, name, type_abbreviation, is_output, length_argument_name = None):
		super(ImplicitlyTypedFunctionArgument, self).__init__(name)
		self.type_abbreviation = type_abbreviation
		# In-place arguments are both input and output 
		self.is_inplace = type_abbreviation.startswith("I")
		self.is_output = is_output or self.is_inplace
		self.is_input = not is_output or self.is_inplace
		if self.is_inplace:
			type_abbreviation = type_abbreviation[1:]

		self.is_vector = type_abbreviation[0] == "V"
		self.is_scalar = type_abbreviation[0] == "S"
		if self.is_vector:
			self.length_argument_name = length_argument_name if length_argument_name else "length"
		type_abbreviation = type_abbreviation[1:]

		type = "Yep" + type_abbreviation
		if self.is_vector or self.is_output:
			type = type + "*"
			if not self.is_output:
				type = "const " + type
		c_type = peachpy.c.Type(type)

		self.c_public_arguments = [peachpy.c.Parameter(name, c_type)]
		if c_type.is_pointer():
			self.c_private_arguments = [peachpy.c.Parameter(name + "Pointer", c_type)]
		else:
			self.c_private_arguments = [peachpy.c.Parameter(name, c_type)]
		java_type = c_type.get_java_analog()
		if java_type:
			if java_type.is_array():
				self.java_arguments = [peachpy.java.Parameter(self.declared_name + "Array", java_type), peachpy.java.Parameter(self.declared_name + "Offset", peachpy.java.Type("int"))]
			else:
				self.java_arguments = [peachpy.java.Parameter(self.declared_name, java_type)]
		else:
			self.java_arguments = None
		if self.is_vector:
			fortran_type = c_type.get_fortran_iso_c_analog()
		else:
			fortran_type = c_type.get_primitive_type().get_fortran_iso_c_analog()
		if fortran_type:
			if self.is_vector:
				fortran_type.set_dimension(self.length_argument_name)
			self.fortran_arguments = [peachpy.fortran.Parameter(self.declared_name, fortran_type, is_input = self.is_input, is_output = self.is_output)]
		else:
			self.fortran_arguments = None

		if self.is_vector:
			csharp_dllimport_type = c_type.get_csharp_analog(use_unsafe_types = True)
		else:
			csharp_dllimport_type = c_type.get_primitive_type().get_csharp_analog()
		if csharp_dllimport_type:
			self.csharp_dllimport_arguments = [peachpy.csharp.Parameter(name, csharp_dllimport_type, is_output = self.is_scalar and self.is_output and not self.is_input)]
		else:
			self.csharp_dllimport_arguments = None
		if self.is_vector:
			csharp_dllimport_type = c_type.get_csharp_analog(use_unsafe_types = True)
		else:
			csharp_dllimport_type = c_type.get_primitive_type().get_csharp_analog()

		if self.is_vector:
			csharp_unsafe_type = c_type.get_csharp_analog(use_unsafe_types = True)
		else:
			csharp_unsafe_type = c_type.get_primitive_type().get_csharp_analog(use_unsafe_types = True)
		if csharp_unsafe_type:
			if self.is_vector:
				self.csharp_unsafe_arguments = [peachpy.csharp.Parameter(name + "Pointer", csharp_unsafe_type, is_output = self.is_scalar and self.is_output and not self.is_input)]
			else:
				self.csharp_unsafe_arguments = [peachpy.csharp.Parameter(name, csharp_unsafe_type, is_output = self.is_scalar and self.is_output and not self.is_input)]
		else:
			self.csharp_unsafe_arguments = None

		if self.is_vector:
			csharp_safe_type = c_type.get_csharp_analog(use_unsafe_types = False)
		else:
			csharp_safe_type = c_type.get_primitive_type().get_csharp_analog(use_unsafe_types = False)
		if csharp_safe_type:
			if csharp_safe_type.is_array():
				self.csharp_safe_arguments = [peachpy.csharp.Parameter(name + "Array", csharp_safe_type, is_output = False),
											  peachpy.csharp.Parameter(name + "Offset", peachpy.csharp.Type("int"))]
			else:
				self.csharp_safe_arguments = [peachpy.csharp.Parameter(name, csharp_safe_type, is_output = self.is_output and not self.is_input)]
		else:
			self.csharp_safe_arguments = None

	def __str__(self):
		return "%s: %s" % (self.declared_name, self.type_abbreviation)

class FunctionSpecialization:
	def __init__(self, declaration):
		function_name_matcher = re.match("yep([A-Za-z]+)_([A-Za-z]+)_", declaration)
		if function_name_matcher is None:
			raise ValueError("Function declaration {0} does not follow Yeppp! naming convention".format(declaration))
		else:
			self.module_name = function_name_matcher.group(1)
			self.function_name = function_name_matcher.group(2)
			arguments_declaration = declaration[function_name_matcher.end():]
			type_abbreviation_regex = "[I]?[VS](?:8[us]|16[usf]|32[usf]|64[usf]|128[us]|16fc|32fc|64fc|32df|64df)"
			inputs_abbreviations = list()
			abbreviation_matcher = re.match(type_abbreviation_regex, arguments_declaration)
			while abbreviation_matcher:
				arguments_declaration = arguments_declaration[abbreviation_matcher.end():]
				inputs_abbreviations.append(abbreviation_matcher.group())
				abbreviation_matcher = re.match(type_abbreviation_regex, arguments_declaration)
			self.inputs_abbreviations = [re.match("[I]?[VS](.+)", input_abbreviation).group(1) for input_abbreviation in inputs_abbreviations]
			if not arguments_declaration.startswith("_"):
				raise ValueError("Function declaration {0} does not contain seperator between inputs and outputs".format(declaration))
			else:
				arguments_declaration = arguments_declaration[1:]
				outputs_abbreviations = list()
				abbreviation_matcher = re.match(type_abbreviation_regex, arguments_declaration)
				while abbreviation_matcher:
					arguments_declaration = arguments_declaration[abbreviation_matcher.end():]
					outputs_abbreviations.append(abbreviation_matcher.group())
					abbreviation_matcher = re.match(type_abbreviation_regex, arguments_declaration)
				self.outputs_abbreviations = [re.match("[I]?[VS](.+)", output_abbreviation).group(1) for output_abbreviation in outputs_abbreviations]
				# Check that the numbers of in-place arguments in the input and output sections is the same
				if sum(input.startswith("I") for input in inputs_abbreviations) != sum(output.startswith("I") for output in outputs_abbreviations):
					raise ValueError("Function declaration {0} contains different number of intput and output in-place arguments".format(declaration))
				else:
					if not arguments_declaration.startswith("(") or not arguments_declaration.endswith(")"):
						raise ValueError("Function declaration {0} misses argument list".format(declaration))
					else:
						self.c_function_signature = declaration[:declaration.index("(")]
						self.short_function_signature = self.c_function_signature[len("yep" + self.module_name + "_"):]
						arguments_declaration = map(string.strip, arguments_declaration[1:-1].split(","))
						self.arguments = list()
						while arguments_declaration:
							argument_string = arguments_declaration.pop(0)
							name_matcher = re.search("([A-Za-z_][A-Za-z0-9_]*)(\[[A-Za-z_][A-Za-z0-9_]+\])?$", argument_string)
							if not name_matcher:
								raise ValueError("Invalid name for argument {0}".format(argument_string))
							else:
								name = name_matcher.group(1)
								type_string = argument_string[:name_matcher.start()].strip()
								if name_matcher.group(2):
									length_argument_name = name_matcher.group(2)[1:-1]
								else:
									length_argument_name = None
								if type_string:
									if length_argument_name:
										raise ValueError("Length specification is allowed only for implicitly types arguments")
									else:
										self.arguments.append(ExplicitlyTypedFunctionArgument(name, type_string))
								else:
									# Consider input arguments if there are any, then output arguments
									is_output_parameter = not inputs_abbreviations
									if is_output_parameter:
										type_abbreviation = outputs_abbreviations.pop(0)
									else:
										type_abbreviation = inputs_abbreviations.pop(0)
										# If this is an in-place argument, remove the matching abbreviation from output list
										if type_abbreviation.startswith("I"):
											outputs_abbreviations.remove(type_abbreviation)
									self.arguments.append(ImplicitlyTypedFunctionArgument(name, type_abbreviation, is_output_parameter, length_argument_name))

						# Detect if any argument can be converted to return value
						scalar_output_arguments = filter(lambda argument: argument.is_automatic() and argument.is_scalar and argument.is_output, self.arguments)
						if len(scalar_output_arguments) == 1:
							self.return_argument = scalar_output_arguments[0]
							self.return_argument.is_return_argument = True
							self.return_argument.java_arguments = [	peachpy.java.Parameter(self.return_argument.get_name(), 
																	self.return_argument.java_arguments[0].get_type().get_primitive_type()) ]
							self.return_argument.csharp_safe_arguments = [	peachpy.csharp.Parameter(self.return_argument.get_name(),
																			self.return_argument.csharp_safe_arguments[0].get_type().get_primitive_type()) ] 
						else:
							self.return_argument = None

						# Detect which arguments are used to specify length of other arguments
						length_arguments = set([argument.length_argument_name for argument in self.arguments if argument.is_automatic() and argument.is_vector and isinstance(argument.length_argument_name, str)])
						for argument in self.arguments:
							if argument.get_name() in length_arguments:
								argument.is_length_argument = True

						# Define variables to be used by default implementation
						self.implementation_macros = dict(
							[("InputType" + str(i), input_abbreviation) for (i, input_abbreviation) in enumerate(self.inputs_abbreviations)] +
							[("OutputType" + str(i), output_abbreviation) for (i, output_abbreviation) in enumerate(self.outputs_abbreviations)])

						# Define variables to be used by documentation
						description_map = {	'8u': 'unsigned 8-bit integer',   '8s': 'signed 8-bit integer',
											'16u': 'unsigned 16-bit integer', '16s': 'signed 16-bit integer',
											'32u': 'unsigned 32-bit integer', '32s': 'signed 32-bit integer',
											'64u': 'unsigned 64-bit integer', '64s': 'signed 64-bit integer',
											'32f': 'single precision (32-bit) floating-point',
											'64f': 'double precision (64-bit) floating-point'}
						self.documentation_macros = dict(
							[("InputType" + str(i), description_map[input_abbreviation]) for (i, input_abbreviation) in enumerate(self.inputs_abbreviations)] +
							[("OutputType" + str(i), description_map[output_abbreviation]) for (i, output_abbreviation) in enumerate(self.outputs_abbreviations)])
						
						self.assembly_functions = { 'x86': list(), 'x64-ms': list(), 'x64-sysv': list(), 'x64-k1om': list() }

						self.c_public_arguments = [c_public_argument for argument in self.arguments for c_public_argument in argument.c_public_arguments]
						self.c_private_arguments = [c_private_argument for argument in self.arguments for c_private_argument in argument.c_private_arguments]
						self.java_arguments = [java_argument for argument in self.arguments for java_argument in argument.java_arguments if not argument.is_return_argument]
						self.fortran_arguments = [fortran_argument for argument in self.arguments for fortran_argument in argument.fortran_arguments]
						self.csharp_dllimport_arguments = [csharp_dllimport_argument for argument in self.arguments for csharp_dllimport_argument in argument.csharp_dllimport_arguments]
						self.csharp_unsafe_arguments = [csharp_unsafe_argument for argument in self.arguments for csharp_unsafe_argument in argument.csharp_unsafe_arguments if not argument.is_return_argument]
						self.csharp_safe_arguments = [csharp_safe_argument for argument in self.arguments for csharp_safe_argument in argument.csharp_safe_arguments if not argument.is_return_argument]

	def generate_assembly_implementation(self, assembly_implementation_generator, assembly_implementation):
		assembly_function = assembly_implementation(assembly_implementation_generator, self.c_function_signature, self.module_name, self.function_name, self.c_private_arguments)
		if assembly_function:
			self.assembly_functions[assembly_implementation_generator.abi.get_name()].append(assembly_function)

	def generate_public_header(self, public_header_generator, default_documentation):
		named_arguments_list = [argument.get_type().format(compact_pointers = False, restrict_qualifier = "YEP_RESTRICT") + " " + argument.get_name()
			for argument in self.c_public_arguments] 

		if default_documentation:
			documentation_lines = filter(bool, (default_documentation % self.documentation_macros).split("\n"))
			# Find position to insert auto-generated return value descriptions
			for i, line in enumerate(documentation_lines):
				if line.startswith("@retval"):
					retval_insert_position = i
			else:
				retval_insert_position = len(documentation_lines)
			documentation_lines.insert(retval_insert_position, "@retval	#YepStatusOk	The computation finished successfully.")
			pointer_names = [argument.get_name() for argument in self.c_public_arguments if argument.get_type().is_pointer()]
			if pointer_names:
				if len(pointer_names) == 1:
					documentation_lines.insert(retval_insert_position + 1, "@retval	#YepStatusNullPointer	The @a %s argument is null." % pointer_names[0])
					documentation_lines.insert(retval_insert_position + 2, "@retval	#YepStatusMisalignedPointer	The @a %s argument is not naturally aligned." % pointer_names[0])
				elif len(pointer_names) == 2:
					documentation_lines.insert(retval_insert_position + 1, "@retval	#YepStatusNullPointer	@a %s or @a %s argument is null." % (pointer_names[0], pointer_names[1]))
					documentation_lines.insert(retval_insert_position + 2, "@retval	#YepStatusMisalignedPointer	@a %s or @a %s argument is not naturally aligned." % (pointer_names[0], pointer_names[1]))
				else:
					formatted_arguments = map(lambda name: "@a " + name, pointer_names)
					formatted_arguments = ", ".join(formatted_arguments[:-1]) + " or " + formatted_arguments[-1]
					documentation_lines.insert(retval_insert_position + 1, "@retval	#YepStatusNullPointer	%s argument is null." % formatted_arguments)
					documentation_lines.insert(retval_insert_position + 2, "@retval	#YepStatusMisalignedPointer	%s argument is not naturally aligned." % formatted_arguments)
			
			documentation_lines.insert(0, "@ingroup\tyep%s" % self.module_name)
			if self.assembly_functions['x86'] or self.assembly_functions['x64-sysv']:
				documentation_lines.append("@par\tOptimized implementations")
				documentation_lines.append("\t\t<table>")
				documentation_lines.append("\t\t\t<tr><th>Architecture</th><th>Target microarchitecture</th><th>Required instruction extensions</th></tr>")
				for assembly_function in self.assembly_functions['x86']:
					isa_extensions = [isa_extension for isa_extension in assembly_function.get_isa_extensions() if isa_extension]
					documentation_lines.append(" * \t\t\t<tr><td>x86</td><td>{0}</td><td>{1}</td></tr>".format(assembly_function.microarchitecture, ", ".join(isa_extensions)))
				for assembly_function in sorted(self.assembly_functions['x64-sysv'], key = lambda function: function.microarchitecture.get_number()):
					isa_extensions = [isa_extension for isa_extension in assembly_function.get_isa_extensions() if isa_extension]
					isa_extensions = sorted(isa_extensions, key = lambda isa_extension: peachpy.x64.supported_isa_extensions.index(isa_extension))
					documentation_lines.append("\t\t\t<tr><td>x86-64</td><td>{0}</td><td>{1}</td></tr>".format(assembly_function.microarchitecture, ", ".join(isa_extensions)))
				documentation_lines.append("\t\t</table>")
			public_header_generator.add_c_comment(documentation_lines, doxygen = True)			
		public_header_generator.add_line("YEP_PUBLIC_SYMBOL enum YepStatus YEPABI {0}({1});".format(self.c_function_signature, ", ".join(named_arguments_list)))

	def generate_dispatch_table_header(self, dispatch_table_header_generator): 
		unnamed_arguments_list = [argument.get_type().format(restrict_qualifier = "YEP_RESTRICT") for argument in self.c_public_arguments] 
		dispatch_table_header_generator.add_line("extern \"C\" YEP_PRIVATE_SYMBOL const FunctionDescriptor<YepStatus (YEPABI*)({0})> _dispatchTable_{1}[];".format(", ".join(unnamed_arguments_list), self.c_function_signature))

	def generate_dispatch_pointer_header(self, dispatch_pointer_header_generator):
		named_arguments_list = [argument.format(compact_pointers = False, restrict_qualifier = "YEP_RESTRICT") for argument in self.c_private_arguments] 
		dispatch_pointer_header_generator.add_line("extern \"C\" YEP_PRIVATE_SYMBOL YepStatus (YEPABI* _{0})({1});".format(self.c_function_signature, ", ".join(named_arguments_list)))

	def generate_dispatch_table(self, dispatch_table_generator):
		unnamed_arguments_list = [argument.get_type().format(compact_pointers = False, restrict_qualifier = "YEP_RESTRICT") for argument in self.c_public_arguments] 
		named_arguments_list = [argument.format(compact_pointers = False, restrict_qualifier = "YEP_RESTRICT") for argument in self.c_public_arguments] 
		yeppp_abi_list = [('x86',      'YEP_X86_ABI'),
						  ('x64-ms',   'YEP_MICROSOFT_X64_ABI'),
						  ('x64-sysv', 'YEP_SYSTEMV_X64_ABI'),
						  ('x64-k1om', 'YEP_K1OM_X64_ABI')]

		dispatch_table_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI _{0}_Default({1});".format(self.c_function_signature, ", ".join(named_arguments_list)))
		for (abi_name, abi_test_macro) in yeppp_abi_list:
			if self.assembly_functions[abi_name]:
				dispatch_table_generator.add_line("#if defined(%s)" % abi_test_macro)
				for assembly_function in self.assembly_functions[abi_name]:
					dispatch_table_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI {0}({1});".format(assembly_function.symbol_name, ", ".join(named_arguments_list)))
				dispatch_table_generator.add_line("#endif // %s" % abi_test_macro)
# 
		dispatch_table_generator.add_line("YEP_USE_CONST_SECTION(DispatchTable) const FunctionDescriptor<YepStatus (YEPABI*)({0})> _dispatchTable_{1}[] = ".format(", ".join(unnamed_arguments_list), self.c_function_signature));
		dispatch_table_generator.add_line("{")
		dispatch_table_generator.indent()

		# Descriptors for function implementations
		for (abi_name, abi_test_macro) in yeppp_abi_list:
			if self.assembly_functions[abi_name]:
				dispatch_table_generator.add_line("#if defined(%s)" % abi_test_macro)
				for assembly_function in self.assembly_functions[abi_name]:
					(isa_features, simd_features, system_features) = assembly_function.get_yeppp_isa_extensions()
					isa_features = " | ".join(isa_features)
					simd_features = " | ".join(simd_features)
					system_features = " | ".join(system_features)
					dispatch_table_generator.add_line("YEP_DESCRIBE_FUNCTION_IMPLEMENTATION({0}, {1}, {2}, {3}, YepCpuMicroarchitecture{4}, \"asm\", YEP_NULL_POINTER, YEP_NULL_POINTER),".
						format(assembly_function.symbol_name, isa_features, simd_features, system_features, assembly_function.microarchitecture.get_name()))
				dispatch_table_generator.add_line("#endif // %s" % abi_test_macro)
		dispatch_table_generator.add_line("YEP_DESCRIBE_FUNCTION_IMPLEMENTATION(_{0}_Default, YepIsaFeaturesDefault, YepSimdFeaturesDefault, YepSystemFeaturesDefault, YepCpuMicroarchitectureUnknown, \"c++\", \"Naive\", \"None\")".format(self.c_function_signature))

		dispatch_table_generator.dedent()
		dispatch_table_generator.add_line("};")
		dispatch_table_generator.add_line()

	def generate_initialization_function(self, initialization_function_generator):
		initialization_function_generator.add_line("*reinterpret_cast<FunctionPointer*>(&_{0}) = _yepLibrary_InitFunction((const FunctionDescriptor<YepStatus (*)()>*)_dispatchTable_{0});".format(self.c_function_signature))

	def generate_dispatch_pointer(self, dispatch_pointer_generator):
		unnamed_arguments_list = [argument.get_type().format(restrict_qualifier = "YEP_RESTRICT", compact_pointers = False) for argument in self.c_public_arguments] 
		dispatch_pointer_generator.add_line("YEP_USE_DATA_SECTION(FunctionPointer) YepStatus (YEPABI*_{0})({1}) = YEP_NULL_POINTER;".format(self.c_function_signature, ", ".join(unnamed_arguments_list)))

	def generate_dispatch_function(self, dispatch_function_generator):
		named_arguments_list = [argument.format(compact_pointers = False, restrict_qualifier = "YEP_RESTRICT")	for argument in self.c_private_arguments] 
		argument_names = [argument.get_name() for argument in self.c_private_arguments]

		dispatch_function_generator.add_line("YEP_USE_CODE_SECTION(DispatchFunction) YepStatus YEPABI {0}({1}) {{".format(self.c_function_signature, ", ".join(named_arguments_list)))
		dispatch_function_generator.indent().add_line("return _{0}({1});".format(self.c_function_signature, ", ".join(argument_names))).dedent()
		dispatch_function_generator.add_line("}")
		dispatch_function_generator.add_line()

	def generate_default_implementation(self, default_implementation_generator, default_implementation):
		named_arguments_list = [argument.format(compact_pointers = False, restrict_qualifier = "YEP_RESTRICT") for argument in self.c_private_arguments] 

		default_implementation_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus _{0}_Default({1}) {{".format(self.c_function_signature, ", ".join(named_arguments_list)))
		default_implementation_generator.indent()

		# Generate parameter checks
		for argument in self.c_private_arguments:
			if argument.get_type().is_pointer():
				default_implementation_generator.add_line("if YEP_UNLIKELY({0} == YEP_NULL_POINTER) {{".format(argument.get_name()))
				default_implementation_generator.indent()
				default_implementation_generator.add_line("return YepStatusNullPointer;")
				default_implementation_generator.dedent()
				default_implementation_generator.add_line("}")
				default_implementation_generator.add_line("if YEP_UNLIKELY(yepBuiltin_GetPointerMisalignment({0}, sizeof({1})) != 0) {{".format(argument.get_name(), argument.get_type().get_primitive_type()))
				default_implementation_generator.indent()
				default_implementation_generator.add_line("return YepStatusMisalignedPointer;")
				default_implementation_generator.dedent()
				default_implementation_generator.add_line("}")

		default_implementation_generator.add_lines(filter(bool, (default_implementation % self.implementation_macros).split("\n")))

		default_implementation_generator.dedent()
		default_implementation_generator.add_line("}")
		default_implementation_generator.add_line()

	def generate_jni_function(self, jni_implementation_generator):
		jni_function_signature = "Java_info_yeppp_" + str(self.module_name) + "_" + self.short_function_signature.replace("_", "_1")
		named_arguments_list = [str(argument.get_jni_analog()) for argument in self.java_arguments]

		return_type = self.return_argument.get_java_type().get_jni_analog() if self.return_argument else "void" 
		jni_implementation_generator.add_line("JNIEXPORT {0} JNICALL {1}(JNIEnv *env, jclass class, {2}) {{".format(return_type, jni_function_signature, ", ".join(named_arguments_list)))
		jni_implementation_generator.indent()

		# Start of the function. This code might be compiled in C89 mode, so all variables should be defined in the function prologue.		
		jni_implementation_generator.add_line("enum YepStatus status;")
		for argument in self.arguments:
			if argument.is_automatic() and argument.is_vector:
				# Define variables for array pointers: for each array passed to function define a corresponding pointer
				element_type = argument.get_c_private_type().get_primitive_type()
				pointer_name = argument.get_c_private_name()
				jni_implementation_generator.add_line("{0}* {1} = NULL;".format(element_type, pointer_name))
			elif argument.is_automatic() and argument.is_scalar and argument.is_output:
				# Define variables for scalar output arguments
				variable_type = argument.get_c_public_type().get_primitive_type()
				variable_name = argument.get_c_public_name()
				jni_implementation_generator.add_line("{0} {1};".format(variable_type, variable_name))
		jni_implementation_generator.add_line()

		# Check parameters:
		for argument in self.arguments:
			if argument.is_automatic() and (argument.is_vector or argument.is_scalar and argument.is_output and not argument.is_return_argument):
				array_name = argument.get_java_name(0)
				offset_name = argument.get_java_name(1)

				jni_implementation_generator.add_line("if YEP_UNLIKELY({0} == NULL) {{".format(array_name))
				jni_implementation_generator.indent()
				jni_implementation_generator.add_line("(*env)->ThrowNew(env, NullPointerException, \"Argument {0} is null\");".format(array_name))
				if self.return_argument:
					jni_implementation_generator.add_line("return ({0})0;".format(self.return_argument.get_java_type().get_jni_analog()))
				else:
					jni_implementation_generator.add_line("return;")
				jni_implementation_generator.dedent()
				jni_implementation_generator.add_line("}")

				jni_implementation_generator.add_line("if YEP_UNLIKELY({0} < 0) {{".format(offset_name))
				jni_implementation_generator.indent()
				jni_implementation_generator.add_line("(*env)->ThrowNew(env, IllegalArgumentException, \"Argument {0} is negative\");".format(offset_name))
				if self.return_argument:
					jni_implementation_generator.add_line("return ({0})0;".format(self.return_argument.get_java_type().get_jni_analog()))
				else:
					jni_implementation_generator.add_line("return;")
				jni_implementation_generator.dedent()
				jni_implementation_generator.add_line("}")

				if argument.is_vector:				
					array_length = argument.length_argument_name
					jni_implementation_generator.add_line("if YEP_UNLIKELY(((YepSize){0}) + ((YepSize){1}) > (YepSize)((*env)->GetArrayLength(env, {2}))) {{".format(offset_name, array_length, array_name))
					jni_implementation_generator.indent()
					jni_implementation_generator.add_line("(*env)->ThrowNew(env, IndexOutOfBoundsException, \"{0} + {1} exceed the length of {2}\");".format(offset_name, array_length, array_name))
					if self.return_argument:
						jni_implementation_generator.add_line("return ({0})0;".format(self.return_argument.get_java_type().get_jni_analog()))
					else:
						jni_implementation_generator.add_line("return;")
					jni_implementation_generator.dedent()
					jni_implementation_generator.add_line("}")
			elif argument.is_length_argument:
				jni_implementation_generator.add_line("if YEP_UNLIKELY({0} < 0) {{".format(argument.get_name()))
				jni_implementation_generator.indent()
				jni_implementation_generator.add_line("(*env)->ThrowNew(env, NegativeArraySizeException, \"Argument {0} is negative\");".format(argument.get_name()))
				if self.return_argument:
					jni_implementation_generator.add_line("return ({0})0;".format(self.return_argument.get_java_type().get_jni_analog()))
				else:
					jni_implementation_generator.add_line("return;")
				jni_implementation_generator.dedent()
				jni_implementation_generator.add_line("}")
				
		jni_implementation_generator.add_line()

		# Initialize pointer for arrays passed to the function
		for argument in self.arguments:
			if argument.is_automatic() and argument.is_vector:
				pointer_name = argument.get_c_private_name()
				array_name = argument.get_java_name(0)
				jni_implementation_generator.add_line("{1} = (*env)->GetPrimitiveArrayCritical(env, {0}, NULL);".format(array_name, pointer_name))
		jni_implementation_generator.add_line()

		# Emit the function call
		call_arguments = list()
		for argument in self.arguments:
			if argument.is_automatic() and argument.is_scalar and argument.is_output:
				call_arguments += ["&" + str(argument.get_c_public_name())]
			elif argument.is_automatic() and argument.is_vector:
				call_arguments += ["&{0}[{1}]".format(argument.get_c_private_name(), argument.get_java_name(1))]
			else:
				call_arguments += [c_private_argument.get_name() for c_private_argument in argument.c_private_arguments]
		jni_implementation_generator.add_line("status = {0}({1});".format(self.c_function_signature, ", ".join(call_arguments)))
		jni_implementation_generator.add_line()

		# Release arrays passed to the function
		for argument in reversed(self.arguments):
			if argument.is_automatic() and argument.is_vector:
				pointer_name = argument.get_c_private_name()
				array_name = argument.get_java_name(0)
				mode = "0" if argument.is_output else "JNI_ABORT"
				jni_implementation_generator.add_line("(*env)->ReleasePrimitiveArrayCritical(env, {0}, {1}, {2});".format(array_name, pointer_name, mode))

		# If function has scalar output other than return argument, they must be written to their place
		if any([argument.is_automatic() and argument.is_scalar and argument.is_output and not argument.is_return_argument for argument in self.arguments]):
			jni_implementation_generator.add_line()
			for argument in self.arguments:
				if argument.is_automatic() and argument.is_scalar and argument.is_output and not argument.is_return_argument:
					method_name = "Set" + str(argument.java_arguments[0].get_type().get_primitive_type()).title() + "ArrayRegion"
					jni_implementation_generator.add_line("(*env)->{0}(env, {1}, {2}, 1, &{3});".format(
						method_name, argument.get_java_name(0), argument.get_java_name(1), argument.get_name()))
					jni_implementation_generator.add_line("if YEP_UNLIKELY((*env)->ExceptionCheck(env) == JNI_TRUE) {")
					jni_implementation_generator.indent()
					if self.return_argument:
						jni_implementation_generator.add_line("return ({0})0;".format(self.return_argument.get_java_type().get_jni_analog()))
					else:
						jni_implementation_generator.add_line("return;")
					jni_implementation_generator.dedent()
					jni_implementation_generator.add_line("}")

		# Check return value and throw exception as necessary
		jni_implementation_generator.add_line("if YEP_UNLIKELY(status != YepStatusOk) {")
		jni_implementation_generator.indent()
		jni_implementation_generator.add_line("yepJNI_ThrowSuitableException(env, status);")
		jni_implementation_generator.dedent()
		jni_implementation_generator.add_line("}")
		jni_implementation_generator.add_line()


		# If function has a non-void return value, emit a return statement
		if self.return_argument:
			jni_implementation_generator.add_line()
			jni_implementation_generator.add_line("return " + str(self.return_argument.get_name()) + ";")
		jni_implementation_generator.dedent()
		jni_implementation_generator.add_line("}")
		jni_implementation_generator.add_line()

	def generate_java_method(self, java_class_generator, java_documentation):
		named_arguments_list = map(str, self.java_arguments)
		return_type = self.return_argument.get_java_type() if self.return_argument else "void" 

		if java_documentation:
			documentation_lines = filter(bool, (java_documentation % self.documentation_macros).split("\n"))
			if self.assembly_functions['x86'] or self.assembly_functions['x64-sysv']:
				documentation_lines.append("@par\tOptimized implementations")
				documentation_lines.append("\t\t<table>")
				documentation_lines.append("\t\t\t<tr><th>Architecture</th><th>Target microarchitecture</th><th>Required instruction extensions</th></tr>")
				for assembly_function in self.assembly_functions['x86']:
					isa_extensions = [isa_extension for isa_extension in assembly_function.get_isa_extensions() if isa_extension]
					documentation_lines.append(" * \t\t\t<tr><td>x86</td><td>{0}</td><td>{1}</td></tr>".format(assembly_function.microarchitecture, ", ".join(isa_extensions)))
				for assembly_function in sorted(self.assembly_functions['x64-sysv'], key = lambda function: function.microarchitecture.get_number()):
					isa_extensions = [isa_extension for isa_extension in assembly_function.get_isa_extensions() if isa_extension]
					isa_extensions = sorted(isa_extensions, key = lambda isa_extension: peachpy.x64.supported_isa_extensions.index(isa_extension))
					documentation_lines.append("\t\t\t<tr><td>x86-64</td><td>{0}</td><td>{1}</td></tr>".format(assembly_function.microarchitecture, ", ".join(isa_extensions)))
				documentation_lines.append("\t\t</table>")
			java_class_generator.add_c_comment(documentation_lines, doxygen = True)			
		java_class_generator.add_line("public static native {0} {1}({2});".format(return_type, self.short_function_signature, ", ".join(named_arguments_list)))

	def generate_fortran_interface(self, fortran_module_generator):
		argument_names = [fortran_argument.get_name() for fortran_argument in self.fortran_arguments]

		fortran_module_generator.add_line("INTEGER(C_INT) FUNCTION {0} & ".format(self.c_function_signature))
		fortran_module_generator.indent()
		fortran_module_generator.add_line("({0}) &".format(", ".join(argument_names)))
		fortran_module_generator.add_line("BIND(C, NAME='{0}')".format(self.c_function_signature))
		fortran_module_generator.add_line()

		argument_symbols = set([fortran_argument.get_type().get_symbol() for fortran_argument in self.fortran_arguments])
		argument_symbols = sorted(argument_symbols, key = lambda symbol: peachpy.fortran.Type.iso_c_symbols.index(symbol))
		fortran_module_generator.add_line("USE ISO_C_BINDING, ONLY: C_INT, {0}".format(", ".join(argument_symbols)))
		fortran_module_generator.add_line("IMPLICIT NONE")

		# Find the maximum type width to align the definitions
		type_width_max = max(len(argument.format(format_type = True, format_name = False)) for argument in self.fortran_arguments)

		# Find which arguments are used as array size: they must be defined first, or an error will be generated during compilation
		length_arguments = set([argument.get_type().dimension for argument in self.fortran_arguments if isinstance(argument.get_type().dimension, str)])
		for fortran_argument in self.fortran_arguments:
			if fortran_argument.get_name() in length_arguments:
				fortran_module_generator.add_line(fortran_argument.format(type_alignment = type_width_max)) 
		for fortran_argument in self.fortran_arguments:
			if fortran_argument.get_name() not in length_arguments:
				fortran_module_generator.add_line(fortran_argument.format(type_alignment = type_width_max)) 

		fortran_module_generator.dedent()
		fortran_module_generator.add_line("END FUNCTION {0}".format(self.c_function_signature))

	def generate_csharp_dllimport_method(self, csharp_dllimport_method_generator):
		named_arguments_list = map(str, self.csharp_dllimport_arguments)
		csharp_dllimport_method_generator.add_line("[DllImport(\"yeppp\", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint=\"{0}\")]".format(self.c_function_signature))
		csharp_dllimport_method_generator.add_line("private static unsafe extern Status {0}({1});".format(self.c_function_signature, ", ".join(named_arguments_list)))
		csharp_dllimport_method_generator.add_line()

	def generate_csharp_unsafe_method(self, csharp_unsafe_method_generator):
		named_arguments_list = map(str, self.csharp_unsafe_arguments)
		return_type = self.return_argument.get_csharp_unsafe_type() if self.return_argument else "void"

		csharp_unsafe_method_generator.add_line("public static unsafe {0} {1}({2})".format(return_type, self.short_function_signature, ", ".join(named_arguments_list)))
		csharp_unsafe_method_generator.add_line("{").indent()

		# If needed, define a variable for return value
		if self.return_argument is not None:
			csharp_unsafe_method_generator.add_line("{0} {1};".format(self.return_argument.get_csharp_unsafe_type(), self.return_argument.get_name()))

		# Emit function call
		call_arguments = list()
		for argument in self.arguments:
			for csharp_unsafe_argument, csharp_dllimport_argument in zip(argument.csharp_unsafe_arguments, argument.csharp_dllimport_arguments):
				if csharp_unsafe_argument.get_type() != csharp_dllimport_argument.get_type():
					if csharp_dllimport_argument.get_type().is_unsigned_integer():
						call_arguments.append("new {0}(unchecked((uint) {1}))".format(csharp_dllimport_argument.get_type(), csharp_unsafe_argument.get_name()))
					else:
						call_arguments.append("new {0}(unchecked({1}))".format(csharp_dllimport_argument.get_type(), csharp_unsafe_argument.get_name()))
				else:
					if argument.is_automatic() and argument.is_scalar and argument.is_output:
						call_arguments.append("out " + csharp_unsafe_argument.get_name())
					else:
						call_arguments.append(csharp_unsafe_argument.get_name())
		csharp_unsafe_method_generator.add_line("{0}({1});".format(self.c_function_signature, ", ".join(call_arguments)))

		# If function has non-void return value, emit return statement
		if self.return_argument is not None:
			csharp_unsafe_method_generator.add_line("return {0};".format(self.return_argument.get_name()))

		csharp_unsafe_method_generator.dedent().add_line("}")
		csharp_unsafe_method_generator.add_empty_lines(2)

	def generate_csharp_safe_method(self, csharp_safe_method_generator):
		named_arguments_list = map(str, self.csharp_safe_arguments)
		return_type = self.return_argument.get_csharp_safe_type() if self.return_argument else "void"

		csharp_safe_method_generator.add_line("public static unsafe {0} {1}({2})".format(return_type, self.short_function_signature, ", ".join(named_arguments_list)))
		csharp_safe_method_generator.add_line("{").indent()

		# Emit pinning of arrays passed to function
		for argument in self.arguments:
			if argument.is_automatic() and argument.is_vector:
				csharp_safe_method_generator.add_line("fixed ({0} {1} = &{2}[{3}])".format(	argument.get_csharp_unsafe_type(),
																							argument.get_csharp_unsafe_name(),
																							argument.get_csharp_safe_name(0),
																							argument.get_csharp_safe_name(1)) )
				csharp_safe_method_generator.add_line("{").indent()

		# Emit call to unsafe method
		call_arguments = [argument.format(include_type = False) for argument in self.csharp_unsafe_arguments]
		if self.return_argument:
			csharp_safe_method_generator.add_line("return {0}({1});".format(self.short_function_signature, ", ".join(call_arguments)))
		else:
			csharp_safe_method_generator.add_line("{0}({1});".format(self.short_function_signature, ", ".join(call_arguments)))

		# Emit end of pinning regions
		for argument in self.arguments:
			if argument.is_automatic() and argument.is_vector:
				csharp_safe_method_generator.dedent().add_line("}")

		csharp_safe_method_generator.dedent().add_line("}")
		csharp_safe_method_generator.add_empty_lines(2)

class FunctionGenerator:
	def __init__(self):
		self.code = []
		self.public_header_generator = None
		self.module_header_generator = None
		self.module_initialization_generator = None
		self.initialization_function_generator = None
		self.default_implementation_generator = None
		self.dispatch_table_header_generator = None
		self.dispatch_table_generator = None
		self.dispatch_pointer_generator = None
		self.java_class_generator = None
		self.jni_implementation_generator = None
		self.fortran_module_generator = None
		self.csharp_safe_method_generator = None
		self.csharp_unsafe_method_generator = None
		self.csharp_extern_method_generator = None
		self.assembly_implementation_generators = dict()

		self.default_implementation = None
		self.assembly_implementations = list()
		self.default_documentation = None
		self.java_documentation = None

	def generate_group_prolog(self, module_name, group_name, group_comment, header_license, source_license):
		from peachpy import x86
		from peachpy import x64

		self.dispatch_table_header_generator = peachpy.codegen.CodeGenerator()
		self.dispatch_table_header_generator.add_c_comment(source_license)
		self.dispatch_table_header_generator.add_line()
		self.dispatch_table_header_generator.add_line("#pragma once")
		self.dispatch_table_header_generator.add_line()
		self.dispatch_table_header_generator.add_line("#include <yepPredefines.h>")
		self.dispatch_table_header_generator.add_line("#include <yepTypes.h>")
		self.dispatch_table_header_generator.add_line("#include <yepPrivate.hpp>")
		self.dispatch_table_header_generator.add_line("#include <yep{0}.h>".format(module_name))
		self.dispatch_table_header_generator.add_line("#include <library/functions.h>".format(module_name))
		self.dispatch_table_header_generator.add_line()

		self.dispatch_pointer_header_generator = peachpy.codegen.CodeGenerator()
		self.dispatch_pointer_header_generator.add_line()
		self.dispatch_pointer_header_generator.add_line()

		self.initialization_function_generator = peachpy.codegen.CodeGenerator()
		self.initialization_function_generator.add_line()
		self.initialization_function_generator.add_line()
		self.initialization_function_generator.add_line("inline static YepStatus _yep{0}_{1}_Init() {{".format(module_name, group_name))
		self.initialization_function_generator.indent()

		self.dispatch_table_generator = peachpy.codegen.CodeGenerator()
		self.dispatch_table_generator.add_c_comment(source_license)
		self.dispatch_table_generator.add_line()
		self.dispatch_table_generator.add_line("#include <yepPredefines.h>")
		self.dispatch_table_generator.add_line("#include <yepTypes.h>")
		self.dispatch_table_generator.add_line("#include <yepPrivate.hpp>")
		self.dispatch_table_generator.add_line("#include <{0}/{1}.disp.h>".format(module_name.lower(), group_name))
		self.dispatch_table_generator.add_line()
		self.dispatch_table_generator.add_line("#if defined(YEP_MSVC_COMPATIBLE_COMPILER)")
		self.dispatch_table_generator.indent()
		self.dispatch_table_generator.add_line("#pragma section(\".rdata$DispatchTable\", read)")
		self.dispatch_table_generator.add_line("#pragma section(\".data$FunctionPointer\", read, write)")
		self.dispatch_table_generator.dedent()
		self.dispatch_table_generator.add_line("#endif")
		self.dispatch_table_generator.add_line()

		self.module_header_generator.add_line("#include <{0}/{1}.disp.h>".format(module_name.lower(), group_name))

		self.module_initialization_generator.add_line("status = _yep{0}_{1}_Init();".format(module_name, group_name))
		self.module_initialization_generator.add_line("if YEP_UNLIKELY(status != YepStatusOk) {")
		self.module_initialization_generator.indent().add_line("return status;").dedent()
		self.module_initialization_generator.add_line("}")

		self.dispatch_pointer_generator = peachpy.codegen.CodeGenerator()
		self.dispatch_pointer_generator.add_line()
		self.dispatch_pointer_generator.add_line()

		self.dispatch_function_generator = peachpy.codegen.CodeGenerator()
		self.dispatch_function_generator.add_line()
		self.dispatch_function_generator.add_line()
		self.dispatch_function_generator.add_line("#if defined(YEP_MSVC_COMPATIBLE_COMPILER)")
		self.dispatch_function_generator.indent()
		self.dispatch_function_generator.add_line("#pragma code_seg( push, \".text$DispatchFunction\" )")
		self.dispatch_function_generator.dedent()
		self.dispatch_function_generator.add_line("#endif")
		self.dispatch_function_generator.add_line()

		self.default_implementation_generator = peachpy.codegen.CodeGenerator()
		self.default_implementation_generator.add_c_comment(source_license)
		self.default_implementation_generator.add_line()
		self.default_implementation_generator.add_line("#include <yepIntrinsics.h>")
		self.default_implementation_generator.add_line("#include <yep{0}.h>".format(module_name))
		self.default_implementation_generator.add_line()
		self.default_implementation_generator.add_line()

		self.assembly_implementation_generators = [
			x86.Assembler(peachpy.c.ABI('x86')),
			x64.Assembler(peachpy.c.ABI('x64-ms')),
			x64.Assembler(peachpy.c.ABI('x64-sysv'))
		]

		self.jni_implementation_generator = peachpy.codegen.CodeGenerator()
		self.jni_implementation_generator.add_c_comment(source_license)
		self.jni_implementation_generator.add_line()
		self.jni_implementation_generator.add_line("#include <jni.h>")
		self.jni_implementation_generator.add_line("#include <yep{0}.h>".format(module_name))
		self.jni_implementation_generator.add_line("#include <yepJavaPrivate.h>")
		self.jni_implementation_generator.add_empty_lines(2)

		self.java_class_generator.add_line()
		self.java_class_generator.add_line("/** @name	{0} */".format(group_comment))
		self.java_class_generator.add_line("/**@{*/")

		self.public_header_generator.add_line("/** @name	{0} */".format(group_comment))
		self.public_header_generator.add_line("/**@{*/")

		self.csharp_safe_method_generator = peachpy.codegen.CodeGenerator()
		self.csharp_safe_method_generator.add_c_comment(source_license)
		self.csharp_safe_method_generator.add_line()
		self.csharp_safe_method_generator.add_line("using System.Runtime.InteropServices;")
		self.csharp_safe_method_generator.add_line()
		self.csharp_safe_method_generator.add_line("namespace Yeppp")
		self.csharp_safe_method_generator.add_line("{").indent().add_line()
		self.csharp_safe_method_generator.add_line("public partial class {0}".format(module_name))
		self.csharp_safe_method_generator.add_line("{").indent().add_line()

		self.csharp_unsafe_method_generator = peachpy.codegen.CodeGenerator()
		self.csharp_unsafe_method_generator.add_line().indent().indent()

		self.csharp_dllimport_method_generator = peachpy.codegen.CodeGenerator()
		self.csharp_dllimport_method_generator.add_line().indent().indent()

	def generate_group_epilog(self, module_name, group_name):
		self.initialization_function_generator.add_line("return YepStatusOk;")
		self.initialization_function_generator.dedent()
		self.initialization_function_generator.add_line("}")

		self.java_class_generator.add_line("/**@}*/")
		self.java_class_generator.add_line()

		self.public_header_generator.add_line("/**@}*/")
		self.public_header_generator.add_line()

		self.dispatch_function_generator.add_line("#if defined(YEP_MSVC_COMPATIBLE_COMPILER)")
		self.dispatch_function_generator.indent().add_line("#pragma code_seg( pop )").dedent()
		self.dispatch_function_generator.add_line("#endif")

		self.csharp_dllimport_method_generator.dedent().add_line("}")
		self.csharp_dllimport_method_generator.add_line().dedent().add_line("}")
		self.csharp_dllimport_method_generator.add_line()

		with open("library/sources/{0}/{1}.disp.h".format(module_name.lower(), group_name), "w+") as dispatch_header_file:
			dispatch_header_file.write(self.dispatch_table_header_generator.get_code())
			dispatch_header_file.write(self.dispatch_pointer_header_generator.get_code())
			dispatch_header_file.write(self.initialization_function_generator.get_code())
			dispatch_header_file.write("\n")

		with open("library/sources/{0}/{1}.disp.cpp".format(module_name.lower(), group_name), "w+") as dispatch_table_file:
			dispatch_table_file.write(self.dispatch_table_generator.get_code())
			dispatch_table_file.write(self.dispatch_pointer_generator.get_code())
			dispatch_table_file.write(self.dispatch_function_generator.get_code())
			dispatch_table_file.write("\n")

		with open("library/sources/{0}/{1}.impl.cpp".format(module_name.lower(), group_name), "w+") as default_implementation_file:
			default_implementation_file.write(self.default_implementation_generator.get_code())

		with open("bindings/java/sources-jni/{0}/{1}.c".format(module_name.lower(), group_name), "w+") as jni_implementation_file:
			jni_implementation_file.write(self.jni_implementation_generator.get_code())

		with open("bindings/clr/sources-csharp/{0}/{1}.cs".format(module_name.lower(), group_name), "w+") as csharp_implementation_file:
			csharp_implementation_file.write(self.csharp_safe_method_generator.get_code())
			csharp_implementation_file.write(self.csharp_unsafe_method_generator.get_code())
			csharp_implementation_file.write(self.csharp_dllimport_method_generator.get_code())

		for assembly_implementation_generator in self.assembly_implementation_generators:
			with open('library/sources/{0}/{1}.{2}.asm'.format(module_name.lower(), group_name, assembly_implementation_generator.abi.get_name()), "w+") as assembly_implementation_file:
				assembly_implementation_file.write(str(assembly_implementation_generator))

	def generate(self, declaration):
		specialization = FunctionSpecialization(declaration)
		for assembly_implementation in self.assembly_implementations:
			for assembly_implementation_generator in self.assembly_implementation_generators:
				specialization.generate_assembly_implementation(assembly_implementation_generator, assembly_implementation)
		specialization.generate_public_header(self.public_header_generator, self.default_documentation)
		specialization.generate_dispatch_table_header(self.dispatch_table_header_generator)
		specialization.generate_dispatch_pointer_header(self.dispatch_pointer_header_generator)
		specialization.generate_dispatch_table(self.dispatch_table_generator)
		specialization.generate_initialization_function(self.initialization_function_generator)
		specialization.generate_dispatch_pointer(self.dispatch_pointer_generator)
		specialization.generate_dispatch_function(self.dispatch_function_generator)
		specialization.generate_default_implementation(self.default_implementation_generator, self.default_implementation)
		specialization.generate_jni_function(self.jni_implementation_generator)
		specialization.generate_java_method(self.java_class_generator, self.java_documentation)
		specialization.generate_fortran_interface(self.fortran_module_generator)
		specialization.generate_csharp_dllimport_method(self.csharp_dllimport_method_generator)
		specialization.generate_csharp_unsafe_method(self.csharp_unsafe_method_generator)
		specialization.generate_csharp_safe_method(self.csharp_safe_method_generator)
