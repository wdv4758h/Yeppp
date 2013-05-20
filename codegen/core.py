#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

import peachpy.codegen
import yeppp.codegen

import yeppp.library.core.x86
import yeppp.library.core.x64

def generate_add(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.AddSub_VusVus_Vus_implementation)
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.AddSubMulMinMax_VfVf_Vf_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.AddSub_VusVus_Vus_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.AddSubMulMinMax_VfVf_Vf_implementation)
	function_generator.generate_group_prolog('Core', 'Add', 'Vector addition', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes pairwise sums of %(InputType0)s elements in two arrays, producing an array of %(OutputType0)s elements.
 * @param[in]	xPointer	Pointer the first input array of %(InputType0)s elements to be added.
 * @param[in]	yPointer	Pointer the second input array of %(InputType1)s elements to be added.
 * @param[out]	sumPointer	Pointer the output array of %(OutputType0)s elements of the pairwise sums.
 * @param[in]	length	The length of the arrays pointed by @a xPointer, @a yPointer, and @a sumPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer, @a yPointer, or @a sumPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer, @a yPointer, or @a sumPointer arguments is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s sum = x + y;
	*sumPointer++ = sum;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Add_V8uV8u_V8u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V8uV8u_V16u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V8sV8s_V16s(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V16uV16u_V16u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V16uV16u_V32u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V16sV16s_V32s(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V32uV32u_V32u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V32uV32u_V64u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V32sV32s_V64s(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V64uV64u_V64u(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V32fV32f_V32f(xPointer, yPointer, sumPointer)")
	function_generator.generate_function("yepCore_Add_V64fV64f_V64f(xPointer, yPointer, sumPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s sum = x + y;
# 	*sumPointer++ = sum;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Add_V8uS8u_V8u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V8uS8u_V16u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V8sS8s_V16s(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V16uS16u_V16u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V16uS16u_V32u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V16sS16s_V32s(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V32uS32u_V32u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V32uS32u_V64u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V32sS32s_V64s(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V64uS64u_V64u(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V32fS32f_V32f(xPointer, yPointer, sumPointer)")
# 	function_generator.generate_function("yepCore_Add_V64fS64f_V64f(xPointer, yPointer, sumPointer)")

# 	function_generator.default_implementation_code = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	x += y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Add_IV8uV8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV16uV16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV32uV32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV64uV64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV32fV32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV64fV64f_IV64f(xPointer, yPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	x += y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Add_IV8uS8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV16uS16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV32uS32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV64uS64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV32fS32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Add_IV64fS64f_IV64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("core", "Add")

def generate_subtract(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.AddSub_VusVus_Vus_implementation)
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.AddSubMulMinMax_VfVf_Vf_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.AddSub_VusVus_Vus_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.AddSubMulMinMax_VfVf_Vf_implementation)
	function_generator.generate_group_prolog('Core', 'Subtract', 'Vector subtraction', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes pairwise differences of %(InputType0)s elements in two arrays, producing an array of %(OutputType0)s elements.
 * @param[in]	xPointer	Pointer the first input array of %(InputType0)s elements to be subtracted from.
 * @param[in]	yPointer	Pointer the second input array of %(InputType1)s elements to be subtracted.
 * @param[out]	differencePointer	Pointer the output array of %(OutputType0)s elements of the pairwise differences.
 * @param[in]	length	The length of the arrays pointed by @a xPointer, @a yPointer, and @a differencePointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer, @a yPointer, or @a differencePointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer, @a yPointer, or @a differencePointer arguments is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s difference = x - y;
	*differencePointer++ = difference;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Subtract_V8uV8u_V8u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V8uV8u_V16u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V8sV8s_V16s(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V16uV16u_V16u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V16uV16u_V32u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V16sV16s_V32s(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V32uV32u_V32u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V32uV32u_V64u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V32sV32s_V64s(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V64uV64u_V64u(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V32fV32f_V32f(xPointer, yPointer, differencePointer)")
	function_generator.generate_function("yepCore_Subtract_V64fV64f_V64f(xPointer, yPointer, differencePointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s difference = x - y;
# 	*differencePointer++ = difference;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Subtract_V8uS8u_V8u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V8uS8u_V16u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V8sS8s_V16s(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V16uS16u_V16u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V16uS16u_V32u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V16sS16s_V32s(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V32uS32u_V32u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V32uS32u_V64u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V32sS32s_V64s(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V64uS64u_V64u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V32fS32f_V32f(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_V64fS64f_V64f(xPointer, yPointer, differencePointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s x = *xPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	const Yep%(OutputType0)s difference = x - y;
# 	*differencePointer++ = difference;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Subtract_S8uV8u_V8u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S8uV8u_V16u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S8sV8s_V16s(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S16uV16u_V16u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S16uV16u_V32u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S16sV16s_V32s(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S32uV32u_V32u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S32uV32u_V64u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S32sV32s_V64s(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S64uV64u_V64u(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S32fV32f_V32f(xPointer, yPointer, differencePointer)")
# 	function_generator.generate_function("yepCore_Subtract_S64fV64f_V64f(xPointer, yPointer, differencePointer)")

# 	function_generator.default_implementation_code = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	x -= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Subtract_IV8uV8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV16uV16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV32uV32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV64uV64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV32fV32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV64fV64f_IV64f(xPointer, yPointer)")

# 	function_generator.default_implementation_code = \
# """while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	Yep%(OutputType0)s y = *yPointer;
# 	y = x - y;
# 	*yPointer++ = y;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Subtract_V8uIV8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_V16uIV16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_V32uIV32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_V64uIV64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_V32fIV32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_V64fIV64f_IV64f(xPointer, yPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	x -= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Subtract_IV8uS8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV16uS16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV32uS32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV64uS64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV32fS32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_IV64fS64f_IV64f(xPointer, yPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s x = *xPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s y = *yPointer;
# 	y = x - y;
# 	*yPointer++ = y;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Subtract_S8uIV8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_S16uIV16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_S32uIV32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_S64uIV64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_S32fIV32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Subtract_S64fIV64f_IV64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("core", "Subtract")

def generate_negate(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.Negate_Vf_Vf_implementation)
	function_generator.generate_group_prolog('Core', 'Negate', 'Vector negation', header_license, source_license)

	function_generator.default_documentation =\
	"""/**
	 * @ingroup	yep%(ModuleName)s
	 * @brief	Negates a vector of %(InputType0)s elements, producing an array of %(OutputType0)s elements.
	 * @param[in]	numberPointer	Pointer the input array of %(InputType0)s elements to be negated from.
	 * @param[out]	negatedNumberPointer	Pointer the output array of %(OutputType0)s negated elements.
	 * @param[in]	length	The length of the arrays pointed by @a numberPointer and @a negatedNumberPointer.
	 * @retval	#YepStatusOk	The computations finished successfully.
	 * @retval	#YepStatusNullPointer	One of the @a numberPointer or @a negatedNumberPointer arguments is null.
	 * @retval	#YepStatusMisalignedPointer	One of the @a numberPointer or @a negatedNumberPointer arguments is not properly aligned.
	 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s number = *numberPointer++;
	const Yep%(OutputType0)s negatedNumber = -number;
	*negatedNumberPointer++ = negatedNumber;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Negate_V8s_V8s(numberPointer, negatedNumberPointer)")
	function_generator.generate_function("yepCore_Negate_V16s_V16s(numberPointer, negatedNumberPointer)")
	function_generator.generate_function("yepCore_Negate_V32s_V32s(numberPointer, negatedNumberPointer)")
	function_generator.generate_function("yepCore_Negate_V64s_V64s(numberPointer, negatedNumberPointer)")
	function_generator.generate_function("yepCore_Negate_V32f_V32f(numberPointer, negatedNumberPointer)")
	function_generator.generate_function("yepCore_Negate_V64f_V64f(numberPointer, negatedNumberPointer)")

# 	function_generator.default_implementation_code = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s number = *numberPointer;
# 	number = -number;
# 	*numberPointer++ = number;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Negate_IV8s_IV8s(numberPointer)")
# 	function_generator.generate_function("yepCore_Negate_IV16s_IV16s(numberPointer)")
# 	function_generator.generate_function("yepCore_Negate_IV32s_IV32s(numberPointer)")
# 	function_generator.generate_function("yepCore_Negate_IV64s_IV64s(numberPointer)")
# 	function_generator.generate_function("yepCore_Negate_IV32f_IV32f(numberPointer)")
# 	function_generator.generate_function("yepCore_Negate_IV64f_IV64f(numberPointer)")

	function_generator.generate_group_epilog("core", "Negate")

def generate_multiply(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.AddSub_VusVus_Vus_implementation)
	# function_generator.assembly_codegens.append(yeppp.library.core.x86.AddSubMulMinMax_VfVf_Vf_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.Mul_VTuVTu_VTu_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.Mul_V16usV16us_V32us_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.Mul_V32usV32us_V64us_implementation)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.AddSubMulMinMax_VfVf_Vf_implementation)
	function_generator.generate_group_prolog('Core', 'Multiply', 'Vector elementwise multiplication', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes pairwise products of %(InputType0)s elements in two arrays, producing an array of %(OutputType0)s elements.
 * @param[in]	xPointer	Pointer the first input array of %(InputType0)s elements to be multiplied.
 * @param[in]	yPointer	Pointer the second input array of %(InputType1)s elements to be multiplied.
 * @param[out]	productPointer	Pointer the output array of %(OutputType0)s elements of the pairwise products.
 * @param[in]	length	The length of the arrays pointed by @a xPointer, @a yPointer, and @a productPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer, @a yPointer, or @a productPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer, @a yPointer, or @a productPointer arguments is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s product = x * y;
	*productPointer++ = product;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Multiply_V8uV8u_V8u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V8uV8u_V16u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V8sV8s_V16s(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V16uV16u_V16u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V16uV16u_V32u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V16sV16s_V32s(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V32uV32u_V32u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V32uV32u_V64u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V32sV32s_V64s(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V64uV64u_V64u(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V32fV32f_V32f(xPointer, yPointer, productPointer)")
	function_generator.generate_function("yepCore_Multiply_V64fV64f_V64f(xPointer, yPointer, productPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s product = x * y;
# 	*productPointer++ = product;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Multiply_V8uS8u_V8u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V8uS8u_V16u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V8sS8s_V16s(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V16uS16u_V16u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V16uS16u_V32u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V16sS16s_V32s(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32uS32u_V32u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32uS32u_V64u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32sS32s_V64s(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V64uS64u_V64u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32fS32f_V32f(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V64fS64f_V64f(xPointer, yPointer, productPointer)")

# 	function_generator.default_implementation_code = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	x *= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Multiply_IV8uV8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV16uV16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV32uV32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV64uV64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV32fV32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV64fV64f_IV64f(xPointer, yPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	x *= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Multiply_IV8uS8u_IV8u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV16uS16u_IV16u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV32uS32u_IV32u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV64uS64u_IV64u(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV32fS32f_IV32f(xPointer, yPointer)")
# 	function_generator.generate_function("yepCore_Multiply_IV64fS64f_IV64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("core", "Multiply")

def generate_multiply_add(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'MultiplyAdd', 'Vector elementwise multiplication and addition', header_license, source_license)

	function_generator.default_documentation =\
	"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes pairwise products of %(InputType0)s elements in two arrays and then adds the third %(InputType2)s array to the result, producing an array of %(OutputType0)s elements.
 * @param[in]	xPointer	Pointer the first input array of %(InputType0)s elements to be multiplied.
 * @param[in]	yPointer	Pointer the second input array of %(InputType1)s elements to be multiplied.
 * @param[in]	zPointer	Pointer the input array of %(InputType2)s elements to be added to the intermediate multiplication result.
 * @param[out]	macPointer	Pointer the output array of %(OutputType0)s elements.
 * @param[in]	length	The length of the arrays pointed by @a xPointer, @a yPointer, @a zPointer, and @a macPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer, @a yPointer, @a zPointer, or @a macPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer, @a yPointer, @a zPointer, or @a macPointer arguments is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s z = *zPointer++;
	const Yep%(OutputType0)s mac = x * y + z;
	*macPointer++ = mac;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_MultiplyAdd_V32fV32fV32f_V32f(xPointer, yPointer, zPointer, macPointer)")
	function_generator.generate_function("yepCore_MultiplyAdd_V64fV64fV64f_V64f(xPointer, yPointer, zPointer, macPointer)")

	function_generator.default_documentation =\
	"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes pairwise products of %(InputType0)s elements in two arrays and then adds the third %(InputType2)s array to the result, overwriting the third array.
 * @param[in]	xPointer	Pointer the first input array of %(InputType0)s elements to be multiplied.
 * @param[in]	yPointer	Pointer the second input array of %(InputType1)s elements to be multiplied.
 * @param[in,out]	zPointer	Pointer the input/output array of %(InputType2)s elements to be added to the intermediate multiplication result.
 * @param[in]	length	The length of the arrays pointed by @a xPointer, @a yPointer, and @a zPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer, @a yPointer, or @a zPointer arguments is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer, @a yPointer, or @a zPointer arguments is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""
const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	Yep%(OutputType0)s z = *zPointer;
	z = x * y + z;
	*zPointer++ = z;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_MultiplyAdd_V32fS32fIV32f_IV32f(xPointer, yPointer, zPointer)")
	function_generator.generate_function("yepCore_MultiplyAdd_V64fS64fIV64f_IV64f(xPointer, yPointer, zPointer)")

# 	function_generator.default_implementation_code = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s product = x * y;
# 	*productPointer++ = product;
# }
# return YepStatusOk;"""
# 	function_generator.generate_function("yepCore_Multiply_V8uS8u_V8u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V8uS8u_V16u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V8sS8s_V16s(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V16uS16u_V16u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V16uS16u_V32u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V16sS16s_V32s(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32uS32u_V32u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32uS32u_V64u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32sS32s_V64s(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V64uS64u_V64u(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V32fS32f_V32f(xPointer, yPointer, productPointer)")
# 	function_generator.generate_function("yepCore_Multiply_V64fS64f_V64f(xPointer, yPointer, productPointer)")

	function_generator.generate_group_epilog("core", "MultiplyAdd")

def generate_divide(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Divide', 'Division', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s fraction = x / y;
	*fractionPointer++ = fraction;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_V32fV32f_V32f(xPointer, yPointer, fractionPointer)")
	function_generator.generate_function("yepCore_Divide_V64fV64f_V64f(xPointer, yPointer, fractionPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s fraction = x / y;
	*fractionPointer++ = fraction;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_V32fS32f_V32f(xPointer, yPointer, fractionPointer)")
	function_generator.generate_function("yepCore_Divide_V64fS64f_V64f(xPointer, yPointer, fractionPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s x = *xPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s fraction = x / y;
	*fractionPointer++ = fraction;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_S32fV32f_V32f(xPointer, yPointer, fractionPointer)")
	function_generator.generate_function("yepCore_Divide_S64fV64f_V64f(xPointer, yPointer, fractionPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	const Yep%(OutputType0)s y = *yPointer++;
	x /= y;
	*xPointer++ = x;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_IV32fV32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Divide_IV64fV64f_IV64f(xPointer, yPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	Yep%(OutputType0)s y = *yPointer;
	y = x / y;
	*yPointer++ = y;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_V32fIV32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Divide_V64fIV64f_IV64f(xPointer, yPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	x /= y;
	*xPointer++ = x;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_IV32fS32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Divide_IV64fS64f_IV64f(xPointer, yPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s x = *xPointer;
while (length-- != 0) {
	Yep%(OutputType0)s y = *yPointer;
	y = x / y;
	*yPointer++ = y;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Divide_S32fIV32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Divide_S64fIV64f_IV64f(xPointer, yPointer)")

	function_generator.generate_group_epilog("core", "Divide")

def generate_copy(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Copy', 'Copy memory', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s element = *sourcePointer++;
	*destinationPointer++ = element;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Copy_V8u_V8u(sourcePointer, destinationPointer)")

	function_generator.generate_group_epilog("core", "Copy")

def generate_zero(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Zero', 'Zero memory', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	*destinationPointer++ = Yep%(OutputType0)s(0);
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Zero__V8u(destinationPointer)")

	function_generator.generate_group_epilog("core", "Zero")

def generate_reciprocal(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Reciprocal', 'Reciprocal', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s number = *numberPointer++;
	const Yep%(OutputType0)s reciprocal = Yep%(OutputType0)s(1) / number;
	*reciprocalPointer++ = reciprocal;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Reciprocal_V32f_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V64f_V64f(numberPointer, reciprocalPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(InputType0)s number = *numberPointer++;
	const Yep%(OutputType0)s reciprocal = Yep%(OutputType0)s(1) / yepBuiltin_Convert_%(InputType0)s_%(OutputType0)s(number);
	*reciprocalPointer++ = reciprocal;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Reciprocal_V8u_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V8s_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V16u_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V16s_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V32u_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V32s_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V64u_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V64s_V32f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V8u_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V8s_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V16u_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V16s_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V32u_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V32s_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V64u_V64f(numberPointer, reciprocalPointer)")
	function_generator.generate_function("yepCore_Reciprocal_V64s_V64f(numberPointer, reciprocalPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s number = *numberPointer;
	const Yep%(OutputType0)s reciprocal = Yep%(OutputType0)s(1) / number;
	*numberPointer++ = reciprocal;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Reciprocal_IV32f_IV32f(numberPointer)")
	function_generator.generate_function("yepCore_Reciprocal_IV64f_IV64f(numberPointer)")

	function_generator.generate_group_epilog("core", "Reciprocal")

def generate_convert(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Convert', 'Convert', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s inputElement = *inputPointer++;
	const Yep%(OutputType0)s outputElement = yepBuiltin_Convert_%(InputType0)s_%(OutputType0)s(inputElement);
	*outputPointer++ = outputElement;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Convert_V8s_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V8u_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V16s_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V16u_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V32s_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V32u_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V64s_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V64u_V32f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V8s_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V8u_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V16s_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V16u_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V32s_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V32u_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V64s_V64f(inputPointer, outputPointer)")
	function_generator.generate_function("yepCore_Convert_V64u_V64f(inputPointer, outputPointer)")

	function_generator.generate_group_epilog("core", "Convert")

def generate_min(public_header_generator, module_header_generator, module_initialization_generator):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Min', 'Minimum', header_license, source_license)

	function_generator.default_implementation_code = \
"""Yep%(InputType0)s minElement = *arrayPointer++;
while (--length != 0) {
	const Yep%(InputType0)s arrayElement = *arrayPointer++;
	minElement = yepBuiltin_Min_%(InputType0)s%(InputType0)s_%(InputType0)s(arrayElement, minElement);
}
*minPointer++ = minElement;
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Min_V8s_S8s(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V8u_S8u(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V16s_S16s(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V16u_S16u(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32s_S32s(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32u_S32u(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64s_S64s(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64u_S64u(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32f_S32f(arrayPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64f_S64f(arrayPointer, minPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s minimum = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*minPointer++ = minimum;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Min_V8sV8s_V8s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V8uV8u_V8u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V16sV16s_V16s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V16uV16u_V16u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32sV32s_V32s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32uV32u_V32u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64sV32s_V64s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64uV32u_V64u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32fV32f_V32f(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64fV64f_V64f(xPointer, yPointer, minPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s minimum = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*minPointer++ = minimum;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Min_V8sS8s_V8s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V8uS8u_V8u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V16sS16s_V16s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V16uS16u_V16u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32sS32s_V32s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32uS32u_V32u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64sS32s_V64s(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64uS32u_V64u(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V32fS32f_V32f(xPointer, yPointer, minPointer)")
	function_generator.generate_function("yepCore_Min_V64fS64f_V64f(xPointer, yPointer, minPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	const Yep%(OutputType0)s y = *yPointer++;
	x = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Min_IV8sV8s_IV8s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV8uV8u_IV8u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV16sV16s_IV16s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV16uV16u_IV16u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV32sV32s_IV32s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV32uV32u_IV32u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV64sV32s_IV64s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV64uV32u_IV64u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV32fV32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV64fV64f_IV64f(xPointer, yPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	x = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Min_IV8sS8s_IV8s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV8uS8u_IV8u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV16sS16s_IV16s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV16uS16u_IV16u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV32sS32s_IV32s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV32uS32u_IV32u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV64sS32s_IV64s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV64uS32u_IV64u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV32fS32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Min_IV64fS64f_IV64f(xPointer, yPointer)")

	function_generator.generate_group_epilog('core', 'Min')

def generate_max(public_header_generator, module_header_generator, module_initialization_generator):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Max', 'Maximum', header_license, source_license)

	function_generator.default_implementation_code = \
"""Yep%(InputType0)s maxElement = *arrayPointer++;
while (--length != 0) {
	const Yep%(InputType0)s arrayElement = *arrayPointer++;
	maxElement = yepBuiltin_Max_%(InputType0)s%(InputType0)s_%(InputType0)s(arrayElement, maxElement);
}
*maxPointer = maxElement;
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Max_V8s_S8s(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V8u_S8u(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V16s_S16s(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V16u_S16u(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32s_S32s(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32u_S32u(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64s_S64s(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64u_S64u(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32f_S32f(arrayPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64f_S64f(arrayPointer, maxPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s maximum = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*maxPointer++ = maximum;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Max_V8sV8s_V8s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V8uV8u_V8u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V16sV16s_V16s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V16uV16u_V16u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32sV32s_V32s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32uV32u_V32u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64sV32s_V64s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64uV32u_V64u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32fV32f_V32f(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64fV64f_V64f(xPointer, yPointer, maxPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s maximum = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*maxPointer++ = maximum;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Max_V8sS8s_V8s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V8uS8u_V8u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V16sS16s_V16s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V16uS16u_V16u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32sS32s_V32s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32uS32u_V32u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64sS32s_V64s(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64uS32u_V64u(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V32fS32f_V32f(xPointer, yPointer, maxPointer)")
	function_generator.generate_function("yepCore_Max_V64fS64f_V64f(xPointer, yPointer, maxPointer)")

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	const Yep%(OutputType0)s y = *yPointer++;
	x = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Max_IV8sV8s_IV8s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV8uV8u_IV8u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV16sV16s_IV16s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV16uV16u_IV16u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV32sV32s_IV32s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV32uV32u_IV32u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV64sV32s_IV64s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV64uV32u_IV64u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV32fV32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV64fV64f_IV64f(xPointer, yPointer)")

	function_generator.default_implementation_code = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	x = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Max_IV8sS8s_IV8s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV8uS8u_IV8u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV16sS16s_IV16s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV16uS16u_IV16u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV32sS32s_IV32s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV32uS32u_IV32u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV64sS32s_IV64s(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV64uS32u_IV64u(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV32fS32f_IV32f(xPointer, yPointer)")
	function_generator.generate_function("yepCore_Max_IV64fS64f_IV64f(xPointer, yPointer)")

	function_generator.generate_group_epilog('core', 'Max')

def generate_sum(public_header_generator, module_header_generator, module_initialization_generator):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Sum', 'Summation', header_license, source_license)

	function_generator.default_implementation_code = \
"""Yep%(InputType0)s sum = Yep%(InputType0)s(0);
while (length-- != 0) {
	const Yep%(InputType0)s arrayElement = *arrayPointer++;
	sum += arrayElement;
}
*sumPointer = sum;
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Sum_V8s_S8s(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V8u_S8u(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V16s_S16s(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V16u_S16u(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V32s_S32s(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V32u_S32u(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V64s_S64s(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V64u_S64u(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V32f_S32f(arrayPointer, sumPointer)")
	function_generator.generate_function("yepCore_Sum_V64f_S64f(arrayPointer, sumPointer)")

	function_generator.generate_group_epilog('core', 'Sum')

def generate_sum_squares(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.assembly_codegens.append(yeppp.library.core.x64.SumSquares_Vf_Sf_implementation_Nehalem)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.SumSquares_Vf_Sf_implementation_SandyBridge)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.SumSquares_Vf_Sf_implementation_Bulldozer)
	function_generator.generate_group_prolog('Core', 'SumSquares', 'Summation of squares (squared L2 norm)', header_license, source_license)

	function_generator.default_documentation =\
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes the sum of squares of %(InputType0)s elements in the input array.
 * @param[in]	numberPointer	Pointer the input array of %(InputType0)s elements.
 * @param[out]	sumSquaresPointer	Pointer the %(OutputType0)s element to hold the sum of squares.
 * @param[in]	length	The length of the array pointed by @a numberPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	@a numberPointer or @a sumSquaresPointer argument is null.
 * @retval	#YepStatusMisalignedPointer	@a numberPointer or @a sumSquaresPointer argument is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""Yep%(InputType0)s sum = Yep%(InputType0)s(0);
while (length-- != 0) {
	const Yep%(InputType0)s number = *numberPointer++;
	sum += number * number;
}
*sumSquaresPointer = sum;
return YepStatusOk;"""
	function_generator.generate_function("yepCore_SumSquares_V32f_S32f(numberPointer, sumSquaresPointer)")
	function_generator.generate_function("yepCore_SumSquares_V64f_S64f(numberPointer, sumSquaresPointer)")

	function_generator.generate_group_epilog('core', 'SumSquares')

def generate_dotproduct(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license):
	function_generator = yeppp.codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.assembly_codegens.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_Nehalem)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_SandyBridge)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_Haswell)
	function_generator.assembly_codegens.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_Bulldozer)
# 	function_generator.assembly_codegens.append(yeppp.library.core.x64.DotProduct_V64fV64f_S64f_implementation_Bonnell)
	function_generator.generate_group_prolog('Core', 'DotProduct', 'Dot product', header_license, source_license)

	function_generator.default_documentation = \
"""/**
 * @ingroup	yep%(ModuleName)s
 * @brief	Computes the dot product of %(InputType0)s elements in two arrays.
 * @param[in]	xPointer	Pointer the first input vector of %(InputType0)s elements.
 * @param[in]	yPointer	Pointer the second input vector of %(InputType1)s elements.
 * @param[out]	dotProductPointer	Pointer the output %(OutputType0)s variable.
 * @param[in]	length	The length of the arrays pointed by @a xPointer and @a yPointer.
 * @retval	#YepStatusOk	The computations finished successfully.
 * @retval	#YepStatusNullPointer	One of the @a xPointer, @a yPointer, or @a dotProductPointer pointers is null.
 * @retval	#YepStatusMisalignedPointer	One of the @a xPointer, @a yPointer, or @a dotProductPointer pointers is not properly aligned.
 */"""
	function_generator.default_implementation_code = \
"""Yep%(InputType0)s dotProduct = Yep%(InputType0)s(0);
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(InputType0)s y = *yPointer++;
	dotProduct += x * y;
}
*dotProductPointer = dotProduct;
return YepStatusOk;"""
	function_generator.generate_function("yepCore_DotProduct_V32fV32f_S32f(xPointer, yPointer, dotProductPointer)")
	function_generator.generate_function("yepCore_DotProduct_V64fV64f_S64f(xPointer, yPointer, dotProductPointer)")

	function_generator.generate_group_epilog('core', 'DotProduct')

def generate_gather(public_header_generator, module_header_generator, module_initialization_generator):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'Gather', 'Gather', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const YepSize index = YepSize(*indexPointer++);
	const Yep%(InputType0)s element = sourcePointer[index];
	*destinationPointer++ = element;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_Gather_V8uV8u_V8u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V8uV16u_V8u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V8uV32u_V8u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V8uV64u_V8u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V16uV8u_V16u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V16uV16u_V16u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V16uV32u_V16u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V16uV64u_V16u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V32uV8u_V32u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V32uV16u_V32u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V32uV32u_V32u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V32uV64u_V32u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V64uV8u_V64u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V64uV16u_V64u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V64uV32u_V64u(sourcePointer, indexPointer, destinationPointer)")
	function_generator.generate_function("yepCore_Gather_V64uV64u_V64u(sourcePointer, indexPointer, destinationPointer)")

	function_generator.generate_group_epilog('core', 'Gather')

def generate_scatter_increment(public_header_generator, module_header_generator, module_initialization_generator):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'ScatterIncrement', 'Scatter-increment', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const YepSize index = YepSize(*indexPointer++);
	basePointer[index] += 1;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_ScatterIncrement_IV8uV8u_IV8u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV16uV8u_IV16u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV32uV8u_IV32u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV64uV8u_IV64u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV8uV16u_IV8u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV16uV16u_IV16u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV32uV16u_IV32u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV64uV16u_IV64u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV8uV32u_IV8u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV16uV32u_IV16u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV32uV32u_IV32u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV64uV32u_IV64u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV8uV64u_IV8u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV16uV64u_IV16u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV32uV64u_IV32u(basePointer, indexPointer)")
	function_generator.generate_function("yepCore_ScatterIncrement_IV64uV64u_IV64u(basePointer, indexPointer)")

	function_generator.generate_group_epilog('core', 'ScatterIncrement')

def generate_scatter_add(public_header_generator, module_header_generator, module_initialization_generator):
	function_generator = codegen.FunctionGenerator()
	function_generator.public_header_generator = public_header_generator
	function_generator.module_header_generator = module_header_generator
	function_generator.module_initialization_generator = module_initialization_generator
	function_generator.java_class_generator = java_class_generator
	function_generator.generate_group_prolog('Core', 'ScatterAdd', 'Scatter-add', header_license, source_license)

	function_generator.default_implementation_code = \
"""while (length-- != 0) {
	const Yep%(InputType0)s weight = *weightPointer++;
	const YepSize index = YepSize(*indexPointer++);
	basePointer[index] += weight;
}
return YepStatusOk;"""
	function_generator.generate_function("yepCore_ScatterAdd_IV8uV8uV8u_IV8u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV8uV8u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV8uV16u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV8uV8u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV8uV16u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV8uV32u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV8uV8u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV8uV16u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV8uV32u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV8uV64u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV8uV16uV8u_IV8u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV16uV8u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV16uV16u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV16uV8u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV16uV16u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV16uV32u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV16uV8u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV16uV16u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV16uV32u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV16uV64u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV8uV32uV8u_IV8u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV32uV8u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV32uV16u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV32uV8u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV32uV16u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV32uV32u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV32uV8u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV32uV16u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV32uV32u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV32uV64u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV8uV64uV8u_IV8u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV64uV8u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV16uV64uV16u_IV16u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV64uV8u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV64uV16u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV32uV64uV32u_IV32u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV64uV8u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV64uV16u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV64uV32u_IV64u(basePointer, indexPointer, weightPointer)")
	function_generator.generate_function("yepCore_ScatterAdd_IV64uV64uV64u_IV64u(basePointer, indexPointer, weightPointer)")

	function_generator.generate_group_epilog('core', 'ScatterAdd')

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
	public_header_generator.add_line("/** @defgroup yepCore yepCore.h: basic arithmetic operations. */")
	public_header_generator.add_line()

	module_header_generator = peachpy.codegen.CodeGenerator()
	module_header_generator.add_c_comment(header_license)
	module_header_generator.add_line()
	module_header_generator.add_line("#pragma once")
	module_header_generator.add_line()

	module_initialization_generator = peachpy.codegen.CodeGenerator()
	module_initialization_generator.add_line()
	module_initialization_generator.add_line("inline static YepStatus _yepCore_Init() {")
	module_initialization_generator.indent()
	module_initialization_generator.add_line("YepStatus status;")

	java_class_generator = peachpy.codegen.CodeGenerator()
	java_class_generator.add_c_comment(source_license)
	java_class_generator.add_line()
	java_class_generator.add_line("package info.yeppp;")
	java_class_generator.add_line()
	java_class_generator.add_line("/** @brief\tBasic arithmetic operations. */")
	java_class_generator.add_line("public class Core {")
	java_class_generator.indent()
	java_class_generator.add_line("static {")
	java_class_generator.indent()
	java_class_generator.add_line("System.loadLibrary(\"yeppp\");")
	java_class_generator.add_line("System.loadLibrary(\"yeppp-jni\");")
	java_class_generator.dedent()
	java_class_generator.add_line("}")

#	generate_copy(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
#	generate_zero(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_add(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_subtract(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
# 	generate_negate(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_multiply(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
# 	generate_multiply_add(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
	generate_dotproduct(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
#	generate_divide(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
#	generate_reciprocal(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
#	generate_convert(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
#	generate_min(public_header_generator, module_header_generator, module_initialization_generator, header_license, source_license)
#	generate_max(public_header_generator, module_header_generator, module_initialization_generator, header_license, source_license)
#	generate_sum(public_header_generator, module_header_generator, module_initialization_generator, header_license, source_license)
	generate_sum_squares(public_header_generator, module_header_generator, module_initialization_generator, java_class_generator, header_license, source_license)
#	generate_gather(public_header_generator, module_header_generator, module_initialization_generator, header_license, source_license)
#	generate_scatter_increment(public_header_generator, module_header_generator, module_initialization_generator, header_license, source_license)
#	generate_scatter_add(public_header_generator, module_header_generator, module_initialization_generator, header_license, source_license)

	public_header_generator.add_line("#ifdef __cplusplus")
	public_header_generator.indent()
	public_header_generator.add_line("} // extern \"C\"")
	public_header_generator.dedent()
	public_header_generator.add_line("#endif")

	module_initialization_generator.add_line("return YepStatusOk;")
	module_initialization_generator.dedent()
	module_initialization_generator.add_line("}")

	java_class_generator.add_line()
	java_class_generator.dedent()
	java_class_generator.add_line("}")
	java_class_generator.add_line()

	with open("library/sources/core/functions.h", "w+") as module_header_file:
		module_header_file.write(module_header_generator.get_code())
		module_header_file.write(module_initialization_generator.get_code())

	with open("library/headers/yepCore.h", "w+") as public_header_file:
		public_header_file.write(public_header_generator.get_code())

	with open("bindings/java/sources-java/info/yeppp/Core.java", "w+") as java_class_file:
		java_class_file.write(java_class_generator.get_code())

