#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

import peachpy.codegen
import yeppp.codegen

import yeppp.library.math.x86
import yeppp.library.math.x64

def generate_log(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Log_V64f_V64f_Nehalem)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Log_V64f_V64f_K10)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Log_V64f_V64f_SandyBridge)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Log_V64f_V64f_Bobcat)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Log_V64f_V64f_Bulldozer)
	function_generator.generate_group_prolog('Math', 'Log', 'Natural Logarithm', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes logarithm on %(InputType0)s elements.
 * @param[in]	xPointer	Pointer the input array.
 * @param[out]	yPointer	Pointer the output array.
 * @param[in]	length	The length of the arrays pointed by @a xPointer and @a yPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer or @a yPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer or @a yPointer arguments is not properly aligned.
 */"""
	function_generator.java_documentation = \
"""/**
 * @brief	Computes logarithm on %(InputType0)s elements.
 * @param[in]	xArray	Input array.
 * @param[in]   xOffset Offset of the first element in @a xArray.
 * @param[out]	yArray	Output array.
 * @param[in]   yOffset Offset of the first element in @a yArray.
 * @param[in]	length	The length of the subarrays to be used in computation.
 * @throws	NullPointerException	If @a xArray or @a yArray argument is null.
 * @throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
 * @throws	NegativeArraySizeException	If the @a length argument is null.
 * @throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
 * @throws	MisalignedPointerError	If one of the arrays is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Log_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
	function_generator.generate_function("yepMath_Log_V64f_V64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("math", "Log")

def generate_exp(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Exp_V64f_V64f_Bobcat)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Exp_V64f_V64f_K10)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Exp_V64f_V64f_Nehalem)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Exp_V64f_V64f_Bulldozer)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Exp_V64f_V64f_SandyBridge)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Exp_V64f_V64f_Haswell)
	function_generator.generate_group_prolog('Math', 'Exp', 'Base-e Exponent', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes exponent on %(InputType0)s elements.
 * @param[in]	xPointer	Pointer the input array.
 * @param[out]	yPointer	Pointer the output array.
 * @param[in]	length	The length of the arrays pointed by @a xPointer and @a yPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer or @a yPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer or @a yPointer arguments is not properly aligned.
 */"""
	function_generator.java_documentation = \
"""/**
 * @brief	Computes exponent on %(InputType0)s elements.
 * @param[in]	xArray	Input array.
 * @param[in]   xOffset Offset of the first element in @a xArray.
 * @param[out]	yArray	Output array.
 * @param[in]   yOffset Offset of the first element in @a yArray.
 * @param[in]	length	The length of the subarrays to be used in computation.
 * @throws	NullPointerException	If @a xArray or @a yArray argument is null.
 * @throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
 * @throws	NegativeArraySizeException	If the @a length argument is null.
 * @throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
 * @throws	MisalignedPointerError	If one of the arrays is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Exp_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
	function_generator.generate_function("yepMath_Exp_V64f_V64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("math", "Exp")

def generate_sin(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Sin_V64f_V64f_Nehalem)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Sin_V64f_V64f_SandyBridge)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Sin_V64f_V64f_Bulldozer)
	function_generator.generate_group_prolog('Math', 'Sin', 'Sine', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes sine on %(InputType0)s elements.
 * @param[in]	xPointer	Pointer the input array.
 * @param[out]	yPointer	Pointer the output array.
 * @param[in]	length	The length of the arrays pointed by @a xPointer and @a yPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer or @a yPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer or @a yPointer arguments is not properly aligned.
 */"""
	function_generator.java_documentation = \
"""/**
 * @brief	Computes sine on %(InputType0)s elements.
 * @param[in]	xArray	Input array.
 * @param[in]   xOffset Offset of the first element in @a xArray.
 * @param[out]	yArray	Output array.
 * @param[in]   yOffset Offset of the first element in @a yArray.
 * @param[in]	length	The length of the subarrays to be used in computation.
 * @throws	NullPointerException	If @a xArray or @a yArray argument is null.
 * @throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
 * @throws	NegativeArraySizeException	If the @a length argument is null.
 * @throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
 * @throws	MisalignedPointerError	If one of the arrays is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Sin_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
	function_generator.generate_function("yepMath_Sin_V64f_V64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("math", "Sin")

def generate_tan(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	# function_generator.assembly_codegens.append(yeppp.library.math.x64.Tan_V64f_V64f_Nehalem)
	# function_generator.assembly_codegens.append(yeppp.library.math.x64.Tan_V64f_V64f_SandyBridge)
	function_generator.assembly_codegens.append(yeppp.library.math.x64.Tan_V64f_V64f_Bulldozer)
	function_generator.generate_group_prolog('Math', 'Tan', 'Tangent', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes tangent on %(InputType0)s elements.
 * @param[in]	xPointer	Pointer the input array.
 * @param[out]	yPointer	Pointer the output array.
 * @param[in]	length	The length of the arrays pointed by @a xPointer and @a yPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer or @a yPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer or @a yPointer arguments is not properly aligned.
 */"""
	function_generator.java_documentation = \
"""/**
 * @brief	Computes tangent on %(InputType0)s elements.
 * @param[in]	xArray	Input array.
 * @param[in]   xOffset Offset of the first element in @a xArray.
 * @param[out]	yArray	Output array.
 * @param[in]   yOffset Offset of the first element in @a yArray.
 * @param[in]	length	The length of the subarrays to be used in computation.
 * @throws	NullPointerException	If @a xArray or @a yArray argument is null.
 * @throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
 * @throws	NegativeArraySizeException	If the @a length argument is null.
 * @throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
 * @throws	MisalignedPointerError	If one of the arrays is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Tan_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
	function_generator.generate_function("yepMath_Tan_V64f_V64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("math", "Tan")

if __name__ == '__main__':
	header_license = """                           Yeppp! library header
                  This file is auto-generated by Peach-Py,
       Portable Efficient Assembly Code-generator in Higher-level Python,
                   part of the Yeppp! library infrastrure

This file is part of Yeppp! library and licensed under the New BSD license.

Copyright (C) 2010-2012 Marat Dukhan
Copyright (C) 2012-2013 Georgia Institute of Technology
All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Georgia Institute of Technology nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""".split("\n")

	source_license = """                      Yeppp! library implementation
                  This file is auto-generated by Peach-Py,
       Portable Efficient Assembly Code-generator in Higher-level Python,
                 part of the Yeppp! library infrastructure
This file is part of Yeppp! library and licensed under the New BSD license.
See library/LICENSE.txt for the full text of the license.""".split("\n")

	public_header_generator = peachpy.codegen.CodeGenerator()
	public_header_generator.add_c_comment(header_license)
	public_header_generator.add_line()
	public_header_generator.add_line("#pragma once")
	public_header_generator.add_line()
	public_header_generator.add_line("#include <yepPredefines.h>")
	public_header_generator.add_line("#include <yepTypes.h>")
	public_header_generator.add_line()
	public_header_generator.add_line("#ifdef __cplusplus")
	public_header_generator.indent()
	public_header_generator.add_line("extern \"C\" {")
	public_header_generator.dedent()
	public_header_generator.add_line("#endif")
	public_header_generator.add_line()
	public_header_generator.add_line("/** @defgroup yepMath yepMath.h: vector mathematical functions. */")
	public_header_generator.add_line()

	module_header_generator = peachpy.codegen.CodeGenerator()
	module_header_generator.add_c_comment(header_license)
	module_header_generator.add_line()
	module_header_generator.add_line("#pragma once")
	module_header_generator.add_line()

	module_initialization_generator = peachpy.codegen.CodeGenerator()
	module_initialization_generator.add_line()
	module_initialization_generator.add_line("inline static YepStatus _yepMath_Init() {")
	module_initialization_generator.indent()
	module_initialization_generator.add_line("YepStatus status;")

	java_class_generator = peachpy.codegen.CodeGenerator()
	java_class_generator.add_c_comment(source_license)
	java_class_generator.add_line()
	java_class_generator.add_line("package info.yeppp;")
	java_class_generator.add_line()
	java_class_generator.add_line("/** @brief\tVector mathematical functions. */")
	java_class_generator.add_line("public class Math {")
	java_class_generator.indent()
	java_class_generator.add_line("static {")
	java_class_generator.indent()
	java_class_generator.add_line("System.loadLibrary(\"yeppp\");")
	java_class_generator.add_line("System.loadLibrary(\"yeppp-jni\");")
	java_class_generator.dedent()
	java_class_generator.add_line("}")

	generate_log(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_exp(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_sin(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_tan(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	# generate_sqrt(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)

	public_header_generator.add_line("#ifdef __cplusplus")
	public_header_generator.indent().add_line("} // extern \"C\"").dedent()
	public_header_generator.add_line("#endif")

	module_initialization_generator.add_line("return YepStatusOk;")
	module_initialization_generator.dedent()
	module_initialization_generator.add_line("}")

	java_class_generator.add_line()
	java_class_generator.dedent()
	java_class_generator.add_line("}")
	java_class_generator.add_line()

	with open("library/sources/math/functions.h", "w+") as module_header_file:
		module_header_file.write(module_header_generator.get_code())
		module_header_file.write(module_initialization_generator.get_code())

	with open("library/headers/yepMath.h", "w+") as public_header_file:
		public_header_file.write(public_header_generator.get_code())

	with open("bindings/java/sources-java/info/yeppp/Math.java", "w+") as java_class_file:
		java_class_file.write(java_class_generator.get_code())

