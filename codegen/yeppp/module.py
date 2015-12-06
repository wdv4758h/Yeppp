import yeppp.codegen
import marshal

class Module:
	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.public_header_generator = None
		self.module_header_generator = None
		self.module_initialization_generator = None
		self.java_class_generator = None
		self.fortran_module_generator = None
		self.csharp_namespace_generator = None

	def __str__(self):
		return self.name

	def __enter__(self):
		self.public_header_generator = yeppp.codegen.CodeGenerator()
		self.public_header_generator.add_c_comment(yeppp.License.header_license)
		self.public_header_generator.add_line()
		self.public_header_generator.add_line("#pragma once")
		self.public_header_generator.add_line()
		self.public_header_generator.add_line("#include <yepPredefines.h>")
		self.public_header_generator.add_line("#include <yepTypes.h>")
		self.public_header_generator.add_line()
		self.public_header_generator.add_line("#ifdef __cplusplus")
		self.public_header_generator.indent().add_line("extern \"C\" {").dedent()
		self.public_header_generator.add_line("#endif")
		self.public_header_generator.add_line()
		self.public_header_generator.add_line("/** @defgroup yep{0} yep{0}.h: {1}. */".format(self.name, self.description.lower()))
		self.public_header_generator.add_line()

		self.module_header_generator = yeppp.codegen.CodeGenerator()
		self.module_header_generator.add_c_comment(yeppp.License.header_license)
		self.module_header_generator.add_line()
		self.module_header_generator.add_line("#pragma once")
		self.module_header_generator.add_line()

		self.module_initialization_generator = yeppp.codegen.CodeGenerator()
		self.module_initialization_generator.add_line()
		self.module_initialization_generator.add_line("inline static YepStatus _yep{0}_Init() {{".format(self.name))
		self.module_initialization_generator.indent()
		self.module_initialization_generator.add_line("YepStatus status;")

		self.java_class_generator = yeppp.codegen.CodeGenerator()
		self.java_class_generator.add_c_comment(yeppp.License.source_license)
		self.java_class_generator.add_line()
		self.java_class_generator.add_line("package info.yeppp;")
		self.java_class_generator.add_line()
		self.java_class_generator.add_line("/** @brief\t{0}. */".format(self.description))
		self.java_class_generator.add_line("public class {0} {{".format(self.name))
		self.java_class_generator.indent()
		self.java_class_generator.add_line("static {")
		self.java_class_generator.indent()
		self.java_class_generator.add_line("Library.load();")
		self.java_class_generator.dedent()
		self.java_class_generator.add_line("}")

		self.fortran_module_generator = yeppp.codegen.CodeGenerator(use_tabs = False)
		self.fortran_module_generator.add_fortran90_comment(yeppp.License.source_license)
		self.fortran_module_generator.add_line()
		self.fortran_module_generator.add_fortran90_comment("@defgroup yep{0} yep{0}: {1}.".format(self.name, self.description.lower()), doxygen = True)
		self.fortran_module_generator.add_line("MODULE yep{0}".format(self.name))
		self.fortran_module_generator.indent()
		self.fortran_module_generator.add_line("INTERFACE")
		self.fortran_module_generator.indent()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type is None:
			self.public_header_generator.add_line("#ifdef __cplusplus")
			self.public_header_generator.indent().add_line("} // extern \"C\"").dedent()
			self.public_header_generator.add_line("#endif")

			self.module_initialization_generator.add_line("return YepStatusOk;")
			self.module_initialization_generator.dedent()
			self.module_initialization_generator.add_line("}")

			self.java_class_generator.add_line()
			self.java_class_generator.dedent()
			self.java_class_generator.add_line("}")
			self.java_class_generator.add_line()

			self.fortran_module_generator.dedent()
			self.fortran_module_generator.add_line("END INTERFACE")
			self.fortran_module_generator.dedent()
			self.fortran_module_generator.add_line("END MODULE yep{0}".format(self.name))
			self.fortran_module_generator.add_line()

			with open("library/sources/{0}/functions.h".format(self.name.lower()), "w+") as module_header_file:
				module_header_file.write(self.module_header_generator.get_code())
				module_header_file.write(self.module_initialization_generator.get_code())

			with open("library/headers/yep{0}.h".format(self.name), "w+") as public_header_file:
				public_header_file.write(self.public_header_generator.get_code())

			with open("bindings/java/sources-java/info/yeppp/{0}.java".format(self.name), "w+") as java_class_file:
				java_class_file.write(self.java_class_generator.get_code())

			with open("bindings/fortran/sources/yep{0}.f90".format(self.name), "w+") as fortran_module_file:
				fortran_module_file.write(self.fortran_module_generator.get_code())

		return False

class Function:
	def __init__(self, module, name, description):
		self.module = module
		self.name = name
		self.description = description
		self.function_generator = None
		self.c_implementation = None
		self.c_documentation = None
		self.java_documentation = None
		self.unit_test = None

	def __str__(self):
		return self.name

	def __enter__(self):
		self.function_generator = yeppp.codegen.FunctionGenerator()
		self.function_generator.public_header_generator = self.module.public_header_generator
		self.function_generator.module_header_generator = self.module.module_header_generator
		self.function_generator.module_initialization_generator = self.module.module_initialization_generator
		self.function_generator.java_class_generator = self.module.java_class_generator
		self.function_generator.fortran_module_generator = self.module.fortran_module_generator
		self.function_generator.generate_group_prolog(str(self.module), self.module.description, self.name, self.description, yeppp.License.header_license, yeppp.License.source_license)
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type is None:
			self.function_generator.generate_group_epilog(self.module.name, self.name)
		return False

	def generate(self, declaration):
		self.function_generator.c_documentation = self.c_documentation
		self.function_generator.java_documentation = self.java_documentation
		self.function_generator.default_cpp_implementation = self.c_implementation
		self.function_generator.unit_test = self.unit_test
		self.function_generator.generate(declaration)
