#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

import peachpy
import peachpy.codegen
import peachpy.c
import re

class FunctionArgument:
	def __init__(self, type_abbreviation, is_input, name, is_extra = False):
		self.is_extra_argument = is_extra
		if is_extra:
			self.type_abbreviation = None
			self.is_input = True
			self.name = name
			self.is_inplace = False
			self.is_array = False
			self.is_scalar = False
			self.is_function_parameter = True
			self.pointer_type = None
			self.parameter_type = type_abbreviation
			self.is_unsigned_integer = None
			self.is_signed_integer = None
			self.is_integer = None
			self.is_floating_point = None
			jni_type_map = {'YepSize': 'jint'}
			java_type_map = {'YepSize': 'int'}
			self.jni_type = jni_type_map[type_abbreviation]
			self.jni_base_type = self.jni_type
			self.java_type = java_type_map[type_abbreviation]
		else:
			self.type_abbreviation = type_abbreviation
			self.is_input = is_input
			self.name = name
			regexp = re.match("(I?)([VS]|(?:UppTri|LowTri|LowSym|UppSym|Rec|Dia)Mat[TC]?)((?:8|16|32|64)(?:u|s|fc|f))", type_abbreviation)
			self.is_inplace = len(regexp.group(1)) > 0
			structure_type = regexp.group(2)
			self.is_array = structure_type != 'S'
			self.is_scalar = structure_type == 'S'
			self.is_function_parameter = self.is_input or not self.is_inplace
			data_type = regexp.group(3)
			if self.is_inplace or not self.is_input:
				self.pointer_type = "Yep{0}* YEP_RESTRICT".format(data_type)
				self.variable_type = "Yep{0}".format(data_type)
			else:
				self.pointer_type = "const Yep{0}* YEP_RESTRICT".format(data_type)
				self.variable_type = "const Yep{0}".format(data_type)
			self.parameter_type = self.pointer_type
			self.data_type = "Yep" + data_type
			self.base_type = data_type
			self.is_unsigned_integer = self.base_type in ['8u', '16u', '32u', '64u']
			self.is_signed_integer = self.base_type in ['8s', '16s', '32s', '64s']
			self.is_integer = self.is_unsigned_integer or self.is_signed_integer
			self.is_floating_point = self.base_type in ['16f', '32f', '64f']
			size_map = {'8u': 8, '8s': 8, '16u': 16, '16s': 16, '16f': 16,
				'32u': 32, '32s': 32, '32f': 32, '64u': 64, '64s': 64, '64f': 64 }
			self.size = size_map[self.base_type]

			jni_base_type_map = {'8u': 'jbyte', '8s': 'jbyte', '16u': 'jshort', '16s': 'jshort',
				'32u': 'jint', '32s': 'jint', '64u': 'jlong', '64s': 'jlong',
				'32f': 'jfloat', '64f': 'jdouble' }
			self.jni_base_type = jni_base_type_map[data_type]
			self.java_base_type = self.jni_base_type[1:]
			if self.is_array:
				jni_type_map = {'8u': 'jbyteArray', '8s': 'jbyteArray', '16u': 'jshortArray', '16s': 'jshortArray',
					'32u': 'jintArray', '32s': 'jintArray', '64u': 'jlongArray', '64s': 'jlongArray',
					'32f': 'jfloatArray', '64f': 'jdoubleArray' }
				java_type_map = {'8u': 'byte[]', '8s': 'byte[]', '16u': 'short[]', '16s': 'short[]',
					'32u': 'int[]', '32s': 'int[]', '64u': 'long[]', '64s': 'long[]',
					'32f': 'float[]', '64f': 'double[]' }
				self.jni_type = jni_type_map[data_type]
				self.java_type = java_type_map[data_type]
			else:
				self.jni_type = jni_base_type_map[data_type]
				java_type_map = {'8u': 'byte', '8s': 'byte', '16u': 'short', '16s': 'short',
					'32u': 'int', '32s': 'int', '64u': 'long', '64s': 'long',
					'32f': 'float', '64f': 'double' }
				self.java_type = java_type_map[data_type]

	def get_java_parameter_name(self):
		if self.is_array:
			return self.name[:-len("Pointer")] + "Array"
		elif self.is_extra_argument:
			return self.name
		else:
			return self.name[:-len("Pointer")]

	def get_jni_parameter_name(self):
		if self.is_array:
			return self.name[:-len("Pointer")] + "Array"
		elif self.is_extra_argument:
			return self.name
		else:
			return self.name[:-len("Pointer")]

	def get_jni_call_parameter_name(self):
		if self.is_array:
			return "&" + self.name + "[" + self.name[:-len("Pointer")] + "Offset]"
		elif self.is_extra_argument:
			return self.name
		else:
			return "&" + self.name[:-len("Pointer")]

	def get_jni_pointer_name(self):
		return self.name

	def get_jni_array_name(self):
		return self.name[:-len("Pointer")] + "Array"

class FunctionGenerator:
	def __init__(self):
		self.code = []
		self.extra_arguments = [('YepSize', 'length')]
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
		self.assembly_implementation_generators = dict()
		self.assembly_codegens = list()

	def generate_group_prolog(self, module_name, group_name, group_comment, header_license, source_license):
		import yeppp.codegen as codegen
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
		self.dispatch_table_generator.add_line("#if defined(YEP_MICROSOFT_COMPILER) || defined(YEP_INTEL_COMPILER_FOR_WINDOWS)")
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
		self.dispatch_function_generator.add_line("#if defined(YEP_MICROSOFT_COMPILER) || defined(YEP_INTEL_COMPILER_FOR_WINDOWS)")
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

		self.assembly_implementation_generators = dict()
		for abi_name in ['x86', 'x64-ms', 'x64-sysv']:
			abi = peachpy.c.ABI(abi_name)
			if abi_name == 'x86':
				assembly_implementation_generator = x86.Assembler(abi)
			elif abi_name in ['x64-ms', 'x64-sysv']:
				assembly_implementation_generator = x64.Assembler(abi)
			self.assembly_implementation_generators[abi_name] = assembly_implementation_generator

		self.jni_implementation_generator = peachpy.codegen.CodeGenerator()
		self.jni_implementation_generator.add_c_comment(source_license)
		self.jni_implementation_generator.add_line()
		self.jni_implementation_generator.add_line("#include <jni.h>")
		self.jni_implementation_generator.add_line("#include <yep{0}.h>".format(module_name))
		self.jni_implementation_generator.add_line()
		self.jni_implementation_generator.add_line()

		self.java_class_generator.add_line()
		self.java_class_generator.add_line("/** @name	{0} */".format(group_comment))
		self.java_class_generator.add_line("/**@{*/")

		self.public_header_generator.add_line("/** @name	{0} */".format(group_comment))
		self.public_header_generator.add_line("/**@{*/")

	def generate_group_epilog(self, module_name, group_name):
		self.initialization_function_generator.add_line("return YepStatusOk;")
		self.initialization_function_generator.dedent()
		self.initialization_function_generator.add_line("}")

		self.java_class_generator.add_line("/**@}*/")
		self.java_class_generator.add_line()

		self.public_header_generator.add_line("/**@}*/")
		self.public_header_generator.add_line()

		self.dispatch_function_generator.add_line("#if defined(YEP_MICROSOFT_COMPILER) || defined(YEP_INTEL_COMPILER_FOR_WINDOWS)")
		self.dispatch_function_generator.indent()
		self.dispatch_function_generator.add_line("#pragma code_seg( pop )")
		self.dispatch_function_generator.dedent()
		self.dispatch_function_generator.add_line("#endif")

		with open("library/sources/{0}/{1}.disp.h".format(module_name, group_name), "w+") as dispatch_header_file:
			dispatch_header_file.write(self.dispatch_table_header_generator.get_code())
			dispatch_header_file.write(self.dispatch_pointer_header_generator.get_code())
			dispatch_header_file.write(self.initialization_function_generator.get_code())
			dispatch_header_file.write("\n")

		with open("library/sources/{0}/{1}.disp.cpp".format(module_name, group_name), "w+") as dispatch_table_file:
			dispatch_table_file.write(self.dispatch_table_generator.get_code())
			dispatch_table_file.write(self.dispatch_pointer_generator.get_code())
			dispatch_table_file.write(self.dispatch_function_generator.get_code())
			dispatch_table_file.write("\n")

		with open("library/sources/{0}/{1}.impl.cpp".format(module_name, group_name), "w+") as default_implementation_file:
			default_implementation_file.write(self.default_implementation_generator.get_code())

		with open("bindings/java/sources-jni/{0}/{1}.c".format(module_name, group_name), "w+") as jni_implementation_file:
			jni_implementation_file.write(self.jni_implementation_generator.get_code())

		for (abi, assembly_implementation_generator) in self.assembly_implementation_generators.iteritems():
			with open('library/sources/{0}/{1}.{2}.asm'.format(module_name, group_name, abi), "w+") as assembly_implementation_file:
				assembly_implementation_file.write(str(assembly_implementation_generator))

	def generate_function(self, function_abbreviation):
		regexp = re.match("(yep([A-Za-z]+)_([A-Za-z]+)_([A-Za-z0-9]*)_([A-Za-z0-9]*)(?:_Alg[A-Za-z0-9]+)?)\\(([A-Za-z0-9_, ]+)\\)", function_abbreviation)
		function_signature = regexp.group(1)
		module = regexp.group(2)
		function = regexp.group(3)
		inputs = regexp.group(4)
		outputs = regexp.group(5)
		arguments = regexp.group(6)

		arguments = self.parse_arguments(inputs, outputs, arguments)
		argument_names = [argument.name for argument in arguments if argument.is_function_parameter]
		argument_names_list = ", ".join(argument_names)
		named_arguments = ["{0} {1}".format(argument.parameter_type, argument.name) for argument in arguments if argument.is_function_parameter]
		named_arguments_list = ", ".join(named_arguments)
		unnamed_arguments_list = ", ".join([argument.parameter_type for argument in arguments if argument.is_function_parameter])

		input_element_types = [argument.base_type for argument in arguments if argument.is_input and not argument.is_extra_argument]
		output_element_types = [argument.base_type for argument in arguments if not argument.is_input and not argument.is_extra_argument]

		yeppp_to_c_type_map = {'Yep8u': 'uint8_t', 'Yep16u': 'uint16_t', 'Yep32u': 'uint32_t', 'Yep64u': 'uint64_t',
		                       'Yep8s':  'int8_t', 'Yep16s':  'int16_t', 'Yep32s':  'int32_t', 'Yep64s':  'int64_t',
		                       'Yep16f': 'half',     'Yep32f': 'float',    'Yep64f': 'double'}
		parameters = list()
		for argument in arguments:
			if argument.parameter_type == "YepSize":
				parameters.append(peachpy.c.Parameter(argument.name, peachpy.c.Type("size_t")))
			elif argument.is_inplace:
				parameters.append(peachpy.c.Parameter(argument.name, peachpy.c.Type(yeppp_to_c_type_map[argument.data_type] + "*")))
			else:
				parameters.append(peachpy.c.Parameter(argument.name, peachpy.c.Type("const " + yeppp_to_c_type_map[argument.data_type] + "*")))

		assembly_functions_map = dict()
		for abi in self.assembly_implementation_generators.iterkeys():
			assembly_functions_map[abi] = list()
		for asm_codegen in self.assembly_codegens:
			for (abi_name, assembly_implementation_generator) in self.assembly_implementation_generators.iteritems():
				if assembly_implementation_generator:
					assembly_function = asm_codegen(assembly_implementation_generator, function_signature, module, function, inputs, outputs, parameters)
					if assembly_function:
						assembly_functions_map[abi_name].append(assembly_function)

		description_map = {'8u': 'unsigned 8-bit integer',   '8s': 'signed 8-bit integer',
		                   '16u': 'unsigned 16-bit integer', '16s': 'signed 16-bit integer',
		                   '32u': 'unsigned 32-bit integer', '32s': 'signed 32-bit integer',
		                   '64u': 'unsigned 64-bit integer', '64s': 'signed 64-bit integer',
		                   '32f': 'single-precision (32-bit) floating-point',
		                   '64f': 'double-precision (64-bit) floating-point'}

		type_map = dict()
		documentation_map = {'ModuleName': module}
		for input_index in range(len(input_element_types)):
			type_map["InputType" + str(input_index)] = input_element_types[input_index]
			documentation_map["InputType" + str(input_index)] = description_map[input_element_types[input_index]]

		for output_index in range(len(output_element_types)):
			type_map["OutputType" + str(output_index)] = output_element_types[output_index]
			documentation_map["OutputType" + str(output_index)] = description_map[output_element_types[output_index]]

		if self.public_header_generator != None:
			if hasattr(self, "default_documentation"):
				documentation_lines = (self.default_documentation % documentation_map).split("\n")
				self.public_header_generator.add_lines(documentation_lines[:-1])
				if assembly_functions_map['x86'] or assembly_functions_map['x64-sysv']:
					self.public_header_generator.add_line(" * @par\tOptimized implementations")
					self.public_header_generator.add_line(" * \t\t<table>")
					self.public_header_generator.add_line(" * \t\t\t<tr><th>Architecture</th><th>Target microarchitecture</th><th>Required instruction extensions</th></tr>")
					for assembly_function in assembly_functions_map['x86']:
						isa_extensions = [isa_extension for isa_extension in assembly_function.get_isa_extensions() if isa_extension]
						self.public_header_generator.add_line(" * \t\t\t<tr><td>x86</td><td>{0}</td><td>{1}</td></tr>".format(assembly_function.microarchitecture, ", ".join(isa_extensions)))
					for assembly_function in sorted(assembly_functions_map['x64-sysv'], key = lambda function: function.microarchitecture.get_number()):
						isa_extensions = [isa_extension for isa_extension in assembly_function.get_isa_extensions() if isa_extension]
						isa_extensions = sorted(isa_extensions, key = lambda isa_extension: peachpy.x64.supported_isa_extensions.index(isa_extension))
						self.public_header_generator.add_line(" * \t\t\t<tr><td>x86-64</td><td>{0}</td><td>{1}</td></tr>".format(assembly_function.microarchitecture, ", ".join(isa_extensions)))
					self.public_header_generator.add_line(" * \t\t</table>")
				self.public_header_generator.add_line(documentation_lines[-1])
			self.public_header_generator.add_line("YEP_PUBLIC_SYMBOL enum YepStatus YEPABI {0}({1});".format(function_signature, named_arguments_list))

		if self.dispatch_table_header_generator != None:
			self.dispatch_table_header_generator.add_line("extern \"C\" YEP_PRIVATE_SYMBOL const FunctionDescriptor<YepStatus (YEPABI*)({0})> _dispatchTable_{1}[];".format(unnamed_arguments_list, function_signature))

		if self.dispatch_pointer_header_generator != None:
			self.dispatch_pointer_header_generator.add_line("extern \"C\" YEP_PRIVATE_SYMBOL YepStatus (YEPABI* _{0})({1});".format(function_signature, named_arguments_list))

		if self.dispatch_table_generator != None:
			self.dispatch_table_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI _{0}_Default({1});".format(function_signature, named_arguments_list))
			self.dispatch_table_generator.add_line("#if defined(YEP_X86_CPU)")
			for assembly_function in assembly_functions_map['x86']:
				self.dispatch_table_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI {0}({1});".format(assembly_function.symbol_name, named_arguments_list))
			self.dispatch_table_generator.add_line("#endif // YEP_X86_CPU")

			self.dispatch_table_generator.add_line("#if defined(YEP_X64_CPU) && defined(YEP_MICROSOFT_X64_ABI)")
			for assembly_function in assembly_functions_map['x64-ms']:
				self.dispatch_table_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI {0}({1});".format(assembly_function.symbol_name, named_arguments_list))
			self.dispatch_table_generator.add_line("#endif // YEP_X64_CPU && YEP_MICROSOFT_X64_ABI")

			self.dispatch_table_generator.add_line("#if defined(YEP_X64_CPU) && defined(YEP_SYSTEMV_X64_ABI)")
			for assembly_function in assembly_functions_map['x64-sysv']:
				self.dispatch_table_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI {0}({1});".format(assembly_function.symbol_name, named_arguments_list))
			self.dispatch_table_generator.add_line("#endif // YEP_X64_CPU && YEP_SYSTEMV_X64_ABI")

			self.dispatch_table_generator.add_line("YEP_USE_CONST_SECTION(DispatchTable) const FunctionDescriptor<YepStatus (YEPABI*)({0})> _dispatchTable_{1}[] = ".format(unnamed_arguments_list, function_signature));
			self.dispatch_table_generator.add_line("{")
			self.dispatch_table_generator.indent()
			self.dispatch_table_generator.add_line("#if defined(YEP_X86_CPU)")
			for assembly_function in assembly_functions_map['x86']:
				(isa_features, simd_features, system_features) = assembly_function.get_yeppp_isa_extensions()
				isa_features = " | ".join(isa_features)
				simd_features = " | ".join(simd_features)
				system_features = " | ".join(system_features)
				self.dispatch_table_generator.add_line("YEP_DESCRIBE_FUNCTION_IMPLEMENTATION({0}, {1}, {2}, {3}, YepCpuMicroarchitecture{4}, \"asm\", YEP_NULL_POINTER, YEP_NULL_POINTER),".
					format(assembly_function.symbol_name, isa_features, simd_features, system_features, assembly_function.microarchitecture.get_name()))
			self.dispatch_table_generator.add_line("#endif // YEP_X86_CPU")
			self.dispatch_table_generator.add_line("#if defined(YEP_X64_CPU) && defined(YEP_MICROSOFT_X64_ABI)")
			for assembly_function in assembly_functions_map['x64-ms']:
				(isa_features, simd_features, system_features) = assembly_function.get_yeppp_isa_extensions()
				isa_features = " | ".join(isa_features)
				simd_features = " | ".join(simd_features)
				system_features = " | ".join(system_features)
				self.dispatch_table_generator.add_line("YEP_DESCRIBE_FUNCTION_IMPLEMENTATION({0}, {1}, {2}, {3}, YepCpuMicroarchitecture{4}, \"asm\", YEP_NULL_POINTER, YEP_NULL_POINTER),".
					format(assembly_function.symbol_name, isa_features, simd_features, system_features, assembly_function.microarchitecture.get_name()))
			self.dispatch_table_generator.add_line("#endif // YEP_X64_CPU && YEP_MICROSOFT_X64_ABI")
			self.dispatch_table_generator.add_line("#if defined(YEP_X64_CPU) && defined(YEP_SYSTEMV_X64_ABI)")
			for assembly_function in assembly_functions_map['x64-sysv']:
				(isa_features, simd_features, system_features) = assembly_function.get_yeppp_isa_extensions()
				isa_features = " | ".join(isa_features)
				simd_features = " | ".join(simd_features)
				system_features = " | ".join(system_features)
				self.dispatch_table_generator.add_line("YEP_DESCRIBE_FUNCTION_IMPLEMENTATION({0}, {1}, {2}, {3}, YepCpuMicroarchitecture{4}, \"asm\", YEP_NULL_POINTER, YEP_NULL_POINTER),".
					format(assembly_function.symbol_name, isa_features, simd_features, system_features, assembly_function.microarchitecture.get_name()))
			self.dispatch_table_generator.add_line("#endif // YEP_X64_CPU && YEP_SYSTEMV_X64_ABI")
			self.dispatch_table_generator.add_line("#if defined(YEP_IA64_CPU)")
			self.dispatch_table_generator.add_line("#endif // YEP_IA64_CPU")
			self.dispatch_table_generator.add_line("#if defined(YEP_ARM_CPU)")
			self.dispatch_table_generator.add_line("#endif // YEP_ARM_CPU")
			self.dispatch_table_generator.add_line("YEP_DESCRIBE_FUNCTION_IMPLEMENTATION(_{0}_Default, YepIsaFeaturesDefault, YepSimdFeaturesDefault, YepSystemFeaturesDefault, YepCpuMicroarchitectureUnknown, \"c++\", \"Naive\", \"None\")".format(function_signature))
			self.dispatch_table_generator.dedent()
			self.dispatch_table_generator.add_line("};")
			self.dispatch_table_generator.add_line()

		if self.initialization_function_generator != None:
			self.initialization_function_generator.add_line("*reinterpret_cast<FunctionPointer*>(&_{0}) = _yepLibrary_InitFunction((const FunctionDescriptor<YepStatus (*)()>*)_dispatchTable_{0});".format(function_signature))

		if self.dispatch_pointer_generator != None:
			self.dispatch_pointer_generator.add_line("YEP_USE_DATA_SECTION(FunctionPointer) YepStatus (YEPABI*_{0})({1}) = YEP_NULL_POINTER;".format(function_signature, unnamed_arguments_list))

		if self.dispatch_function_generator != None:
			self.dispatch_function_generator.add_line("YEP_USE_CODE_SECTION(DispatchFunction) YepStatus YEPABI {0}({1}) {{".format(function_signature, named_arguments_list))
			self.dispatch_function_generator.indent()
			self.dispatch_function_generator.add_line("return _{0}({1});".format(function_signature, argument_names_list));
			self.dispatch_function_generator.dedent()
			self.dispatch_function_generator.add_line("}")
			self.dispatch_function_generator.add_line()

		if self.default_implementation_generator != None:
			self.default_implementation_generator.add_line("extern \"C\" YEP_LOCAL_SYMBOL YepStatus _{0}_Default({1}) {{".format(function_signature, named_arguments_list))
			self.default_implementation_generator.indent()
			self.default_implementation_generator.add_lines((self.default_implementation_code % type_map).split("\n"))
			self.default_implementation_generator.dedent()
			self.default_implementation_generator.add_line("}")
			self.default_implementation_generator.add_line()

		if self.jni_implementation_generator != None:
			mangled_function_name = "Java_info_yeppp_" + module + "_" + function + "_1" + inputs + "_1" + outputs
			jni_named_arguments = []
			return_argument = None
			for argument in arguments:
				if argument.is_function_parameter:
					if argument.is_scalar and not argument.is_input and return_argument is None:
						name = argument.name
						if name.endswith('Pointer'):
							name = name[:-len('Pointer')]
						return_argument = (argument.java_type, argument.jni_type, argument.data_type, name)
						continue
					jni_named_arguments.append((argument.jni_type, argument.get_jni_parameter_name()))
					if not argument.is_extra_argument:
						name = argument.name
						if name.endswith('Pointer'):
							name = name[:-len('Pointer')]
						name = name + 'Offset'
						jni_named_arguments.append(('jint', name))
			jni_named_arguments_list = ", ".join([str(type) + " " + str(name) for (type, name) in jni_named_arguments])
			jni_arguments_list = ", ".join([argument.get_jni_call_parameter_name() for argument in arguments if argument.is_function_parameter])
			if return_argument:
				self.jni_implementation_generator.add_line("JNIEXPORT {0} JNICALL {1}(JNIEnv *env, jclass class, {2}) {{".format(list(return_argument)[1], mangled_function_name, jni_named_arguments_list))
			else:
				self.jni_implementation_generator.add_line("JNIEXPORT void JNICALL {0}(JNIEnv *env, jclass class, {1}) {{".format(mangled_function_name, jni_named_arguments_list))
			self.jni_implementation_generator.indent()
			self.jni_implementation_generator.add_line("enum YepStatus status;")
			if return_argument:
				(java_type, jni_type, data_type, name) = return_argument
				self.jni_implementation_generator.add_line(str(data_type) + " " + str(name) + ";")
			for argument in arguments:
				if argument.is_array and (argument.is_input or not argument.is_inplace):
					self.jni_implementation_generator.add_line("{0}* {1} = NULL;".format(argument.jni_base_type, argument.get_jni_pointer_name()))
			self.jni_implementation_generator.add_line()
			for argument in arguments:
				if argument.is_array and (argument.is_input or not argument.is_inplace):
					#~ self.jni_implementation_generator.add_line("{1} = (*env)->Get{2}ArrayElements(env, {0}, NULL);".format(argument.get_jni_array_name(), argument.get_jni_pointer_name(), string.capwords(argument.java_base_type)))
					self.jni_implementation_generator.add_line("{1} = (*env)->GetPrimitiveArrayCritical(env, {0}, NULL);".format(argument.get_jni_array_name(), argument.get_jni_pointer_name()))
			self.jni_implementation_generator.add_line()
			self.jni_implementation_generator.add_line("status = {0}({1});".format(function_signature, jni_arguments_list))
			self.jni_implementation_generator.add_line()
			for argument in arguments:
				if argument.is_array and (argument.is_input or not argument.is_inplace):
					#~ self.jni_implementation_generator.add_line("(*env)->Release{2}ArrayElements(env, {0}, {1}, {3});".format(argument.get_jni_array_name(), argument.get_jni_pointer_name(), string.capwords(argument.java_base_type), "0" if not argument.is_input or argument.is_inplace else "JNI_ABORT"))
					self.jni_implementation_generator.add_line("(*env)->ReleasePrimitiveArrayCritical(env, {0}, {1}, {2});".format(argument.get_jni_array_name(), argument.get_jni_pointer_name(), "0" if not argument.is_input or argument.is_inplace else "JNI_ABORT"))
			if return_argument:
				(java_type, jni_type, data_type, name) = return_argument
				self.jni_implementation_generator.add_line()
				self.jni_implementation_generator.add_line("return " + str(name) + ";")
			self.jni_implementation_generator.dedent()
			self.jni_implementation_generator.add_line("}")
			self.jni_implementation_generator.add_line()

		if self.java_class_generator != None:
			mangled_function_name = function + "_" + inputs + "_" + outputs
			java_named_arguments = []
			return_type = None
			for argument in arguments:
				if argument.is_function_parameter:
					if argument.is_scalar and not argument.is_input and return_type is None:
						name = argument.name
						if name.endswith('Pointer'):
							name = name[:-len('Pointer')]
						return_type = argument.java_type
						continue
					java_named_arguments.append((argument.java_type, argument.get_java_parameter_name()))
					if not argument.is_extra_argument:
						name = argument.name
						if name.endswith('Pointer'):
							name = name[:-len('Pointer')]
						name = name + 'Offset'
						java_named_arguments.append(('int', name))
			java_named_arguments_list = ", ".join([str(type) + " " + str(name) for (type, name) in java_named_arguments])
			if hasattr(self, "java_documentation"):
				documentation_lines = (self.java_documentation % documentation_map).split("\n")
				self.java_class_generator.add_lines(documentation_lines)
			if return_type:
				self.java_class_generator.add_line("public static native {0} {1}({2});".format(return_type, mangled_function_name, java_named_arguments_list))
			else:
				self.java_class_generator.add_line("public static native void {0}({1});".format(mangled_function_name, java_named_arguments_list))

	def parse_arguments(self, inputs, outputs, arguments):
		type_abbreviation_regexp = "I?(?:[VS]|(?:UppTri|LowTri|LowSym|UppSym|Rec|Dia)Mat[TC]?)(?:8|16|32|64)(?:u|s|fc|f)"
		input_type_abbreviations = re.findall(type_abbreviation_regexp, inputs)
		output_type_abbreviations = re.findall(type_abbreviation_regexp, outputs)
		input_arguments = [FunctionArgument(type, True, None) for type in input_type_abbreviations]
		output_arguments = [FunctionArgument(type, False, None) for type in output_type_abbreviations]
		argument_names = re.split(", *", arguments)
		for i in range(len(input_arguments)):
			input_arguments[i].name = argument_names[i]
		input_output_names = list()
		for argument in input_arguments:
			if argument.is_inplace:
				input_output_names.append(argument.name)
		output_name_index = len(input_arguments)
		input_output_name_index = 0
		for argument in output_arguments:
			if argument.is_inplace:
				argument.name = input_output_names[input_output_name_index]
				input_output_name_index += 1
			else:
				argument.name = argument_names[output_name_index]
				output_name_index += 1
		return input_arguments + output_arguments + [FunctionArgument(type, True, name, True) for (type, name) in self.extra_arguments]


	def get_pointer_type(self, type_abbreviation, is_input):
		regexp = re.match("(I?)(?:[VS]|(?:UppTri|LowTri|LowSym|UppSym|Rec|Dia)Mat[TC]?)((?:8|16|32|64)(?:u|s|fc|f))", type_abbreviation)
		is_inplace = len(regexp.group(1)) > 0
		type = regexp.group(2)
		if is_inplace or not is_input:
			return "Yep{0}* YEP_RESTRICT".format(type)
		else:
			return "const Yep{0}* YEP_RESTRICT".format(type)

	def get_jni_type(self, type_abbreviation):
		regexp = re.match("(?:I?)([VS]|(?:UppTri|LowTri|LowSym|UppSym|Rec|Dia)Mat[TC]?)((?:8|16|32|64)(?:u|s|fc|f))", type_abbreviation)
		structure_type = regexp.group(1)
		data_type = regexp.group(2)
		is_scalar = structure_type == 'S'
		if is_scalar:
			jni_type_map = {'8u': 'jbyte', '8s': 'jbyte', '16u': 'jshort', '16s': 'jshort',
				'32u': 'jint', '32s': 'jint', '64u': 'jlong', '64s': 'jlong',
				'32f': 'jfloat', '64f': 'jdouble' }
			return jni_type_map[data_type]
		else:
			jni_type_map = {'8u': 'jbyteArray', '8s': 'jbyteArray', '16u': 'jshortArray', '16s': 'jshortArray',
				'32u': 'jintArray', '32s': 'jintArray', '64u': 'jlongArray', '64s': 'jlongArray',
				'32f': 'jfloatArray', '64f': 'jdoubleArray' }
			return jni_type_map[data_type]

	def get_jni_name(self, name):
		if name.endswith("Pointer"):
			name = name[:-len("Pointer")] + "Array"
		return name

	def get_variable_type(self, type_abbreviation, is_input):
		regexp = re.match("(I?)(?:[VS]|(?:UppTri|LowTri|LowSym|UppSym|Rec|Dia)Mat[TC]?)((?:8|16|32|64)(?:u|s|fc|f))", type_abbreviation)
		is_inplace = len(regexp.group(1)) > 0
		type = regexp.group(2)
		if is_inplace or not is_input:
			return "Yep{0}".format(type)
		else:
			return "const Yep{0}".format(type)

