#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

import yeppp.module

import yeppp.library.core.x86
import yeppp.library.core.x64

def generate_add(module):
	with yeppp.module.Function(module, 'Add', 'Addition') as function:
		function.assembly_implementations.append(yeppp.library.core.x64.AddSub_VusVus_Vus_implementation)
		function.assembly_implementations.append(yeppp.library.core.x64.AddSubMulMinMax_VfVf_Vf_implementation)
	
		function.c_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s sum = x + y;
	*sumPointer++ = sum;
}
return YepStatusOk;"""
		function.generate("yepCore_Add_V8uV8u_V8u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V8uV8u_V16u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V8sV8s_V16s(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V16uV16u_V16u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V16uV16u_V32u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V16sV16s_V32s(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V32uV32u_V32u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V32uV32u_V64u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V32sV32s_V64s(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V64uV64u_V64u(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V32fV32f_V32f(xPointer, yPointer, sumPointer)")
		function.generate("yepCore_Add_V64fV64f_V64f(xPointer, yPointer, sumPointer)")
	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s sum = x + y;
# 	*sumPointer++ = sum;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Add_V8uS8u_V8u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V8uS8u_V16u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V8sS8s_V16s(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V16uS16u_V16u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V16uS16u_V32u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V16sS16s_V32s(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V32uS32u_V32u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V32uS32u_V64u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V32sS32s_V64s(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V64uS64u_V64u(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V32fS32f_V32f(xPointer, yPointer, sumPointer)")
# 		function.generate("yepCore_Add_V64fS64f_V64f(xPointer, yPointer, sumPointer)")
# 	
# 		function.c_implementation = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	x += y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Add_IV8uV8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV16uV16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV32uV32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV64uV64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV32fV32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV64fV64f_IV64f(xPointer, yPointer)")
# 	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	x += y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Add_IV8uS8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV16uS16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV32uS32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV64uS64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV32fS32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Add_IV64fS64f_IV64f(xPointer, yPointer)")

def generate_subtract(module):
	with yeppp.module.Function(module, 'Subtract', 'Subtraction') as function:
		function.assembly_implementations.append(yeppp.library.core.x64.AddSub_VusVus_Vus_implementation)
		function.assembly_implementations.append(yeppp.library.core.x64.AddSubMulMinMax_VfVf_Vf_implementation)

		function.c_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s difference = x - y;
	*differencePointer++ = difference;
}
return YepStatusOk;"""
		function.generate("yepCore_Subtract_V8uV8u_V8u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V8uV8u_V16u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V8sV8s_V16s(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V16uV16u_V16u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V16uV16u_V32u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V16sV16s_V32s(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V32uV32u_V32u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V32uV32u_V64u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V32sV32s_V64s(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V64uV64u_V64u(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V32fV32f_V32f(xPointer, yPointer, differencePointer)")
		function.generate("yepCore_Subtract_V64fV64f_V64f(xPointer, yPointer, differencePointer)")
	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s difference = x - y;
# 	*differencePointer++ = difference;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Subtract_V8uS8u_V8u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V8uS8u_V16u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V8sS8s_V16s(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V16uS16u_V16u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V16uS16u_V32u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V16sS16s_V32s(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V32uS32u_V32u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V32uS32u_V64u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V32sS32s_V64s(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V64uS64u_V64u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V32fS32f_V32f(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_V64fS64f_V64f(xPointer, yPointer, differencePointer)")
# 	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s x = *xPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	const Yep%(OutputType0)s difference = x - y;
# 	*differencePointer++ = difference;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Subtract_S8uV8u_V8u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S8uV8u_V16u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S8sV8s_V16s(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S16uV16u_V16u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S16uV16u_V32u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S16sV16s_V32s(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S32uV32u_V32u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S32uV32u_V64u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S32sV32s_V64s(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S64uV64u_V64u(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S32fV32f_V32f(xPointer, yPointer, differencePointer)")
# 		function.generate("yepCore_Subtract_S64fV64f_V64f(xPointer, yPointer, differencePointer)")
# 	
# 		function.c_implementation = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	x -= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Subtract_IV8uV8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV16uV16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV32uV32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV64uV64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV32fV32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV64fV64f_IV64f(xPointer, yPointer)")
# 	
# 		function.c_implementation = \
# """while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	Yep%(OutputType0)s y = *yPointer;
# 	y = x - y;
# 	*yPointer++ = y;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Subtract_V8uIV8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_V16uIV16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_V32uIV32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_V64uIV64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_V32fIV32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_V64fIV64f_IV64f(xPointer, yPointer)")
# 	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	x -= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Subtract_IV8uS8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV16uS16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV32uS32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV64uS64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV32fS32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_IV64fS64f_IV64f(xPointer, yPointer)")
# 	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s x = *xPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s y = *yPointer;
# 	y = x - y;
# 	*yPointer++ = y;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Subtract_S8uIV8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_S16uIV16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_S32uIV32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_S64uIV64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_S32fIV32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Subtract_S64fIV64f_IV64f(xPointer, yPointer)")

def generate_negate(module):
	with yeppp.module.Function(module, 'Negate', 'Negation') as function:
#		function_generator.assembly_implementations.append(yeppp.library.core.x86.Negate_Vf_Vf_implementation)

		function.c_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s number = *numberPointer++;
	const Yep%(OutputType0)s negatedNumber = -number;
	*negatedNumberPointer++ = negatedNumber;
}
return YepStatusOk;"""
		function.generate("yepCore_Negate_V8s_V8s(numberPointer, negatedNumberPointer)")
		function.generate("yepCore_Negate_V16s_V16s(numberPointer, negatedNumberPointer)")
		function.generate("yepCore_Negate_V32s_V32s(numberPointer, negatedNumberPointer)")
		function.generate("yepCore_Negate_V64s_V64s(numberPointer, negatedNumberPointer)")
		function.generate("yepCore_Negate_V32f_V32f(numberPointer, negatedNumberPointer)")
		function.generate("yepCore_Negate_V64f_V64f(numberPointer, negatedNumberPointer)")
	
# 		function.default_implementation = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s number = *numberPointer;
# 	number = -number;
# 	*numberPointer++ = number;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Negate_IV8s_IV8s(numberPointer)")
# 		function.generate("yepCore_Negate_IV16s_IV16s(numberPointer)")
# 		function.generate("yepCore_Negate_IV32s_IV32s(numberPointer)")
# 		function.generate("yepCore_Negate_IV64s_IV64s(numberPointer)")
# 		function.generate("yepCore_Negate_IV32f_IV32f(numberPointer)")
# 		function.generate("yepCore_Negate_IV64f_IV64f(numberPointer)")
	
def generate_multiply(module):
	with yeppp.module.Function(module, 'Multiply', 'Multiplication') as function:
		function.assembly_implementations.append(yeppp.library.core.x64.Mul_VTuVTu_VTu_implementation)
		function.assembly_implementations.append(yeppp.library.core.x64.Mul_V16usV16us_V32us_implementation)
		function.assembly_implementations.append(yeppp.library.core.x64.Mul_V32usV32us_V64us_implementation)
		function.assembly_implementations.append(yeppp.library.core.x64.AddSubMulMinMax_VfVf_Vf_implementation)
	
		function.c_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s product = x * y;
	*productPointer++ = product;
}
return YepStatusOk;"""
		function.generate("yepCore_Multiply_V8uV8u_V8u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V8uV8u_V16u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V8sV8s_V16s(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V16uV16u_V16u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V16uV16u_V32u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V16sV16s_V32s(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32uV32u_V32u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32uV32u_V64u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32sV32s_V64s(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V64uV64u_V64u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32fV32f_V32f(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V64fV64f_V64f(xPointer, yPointer, productPointer)")
	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	const Yep%(OutputType0)s x = *xPointer++;
# 	const Yep%(OutputType0)s product = x * y;
# 	*productPointer++ = product;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Multiply_V8uS8u_V8u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V8uS8u_V16u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V8sS8s_V16s(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V16uS16u_V16u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V16uS16u_V32u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V16sS16s_V32s(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V32uS32u_V32u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V32uS32u_V64u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V32sS32s_V64s(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V64uS64u_V64u(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V32fS32f_V32f(xPointer, yPointer, productPointer)")
# 		function.generate("yepCore_Multiply_V64fS64f_V64f(xPointer, yPointer, productPointer)")
# 	
# 		function.c_implementation = \
# """while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	const Yep%(OutputType0)s y = *yPointer++;
# 	x *= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Multiply_IV8uV8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV16uV16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV32uV32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV64uV64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV32fV32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV64fV64f_IV64f(xPointer, yPointer)")
# 	
# 		function.c_implementation = \
# """const Yep%(OutputType0)s y = *yPointer;
# while (length-- != 0) {
# 	Yep%(OutputType0)s x = *xPointer;
# 	x *= y;
# 	*xPointer++ = x;
# }
# return YepStatusOk;"""
# 		function.generate("yepCore_Multiply_IV8uS8u_IV8u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV16uS16u_IV16u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV32uS32u_IV32u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV64uS64u_IV64u(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV32fS32f_IV32f(xPointer, yPointer)")
# 		function.generate("yepCore_Multiply_IV64fS64f_IV64f(xPointer, yPointer)")

def generate_multiply_add(module):
	with yeppp.module.Function(module, 'MultiplyAdd', 'Multiplication and addition') as function:

		function.c_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s z = *zPointer++;
	const Yep%(OutputType0)s mac = x * y + z;
	*macPointer++ = mac;
}
return YepStatusOk;"""
		function.generate("yepCore_MultiplyAdd_V32fV32fV32f_V32f(xPointer, yPointer, zPointer, macPointer)")
		function.generate("yepCore_MultiplyAdd_V64fV64fV64f_V64f(xPointer, yPointer, zPointer, macPointer)")

		function.c_documentation = \
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
		function.c_implementation = \
"""
const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	Yep%(OutputType0)s z = *zPointer;
	z = x * y + z;
	*zPointer++ = z;
}
return YepStatusOk;"""
		function.generate("yepCore_MultiplyAdd_V32fS32fIV32f_IV32f(xPointer, yPointer, zPointer)")
		function.generate("yepCore_MultiplyAdd_V64fS64fIV64f_IV64f(xPointer, yPointer, zPointer)")

		function.c_documentation = None
		function.c_implementation = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s product = x * y;
	*productPointer++ = product;
}
return YepStatusOk;"""
		function.generate("yepCore_Multiply_V8uS8u_V8u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V8uS8u_V16u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V8sS8s_V16s(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V16uS16u_V16u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V16uS16u_V32u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V16sS16s_V32s(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32uS32u_V32u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32uS32u_V64u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32sS32s_V64s(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V64uS64u_V64u(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V32fS32f_V32f(xPointer, yPointer, productPointer)")
		function.generate("yepCore_Multiply_V64fS64f_V64f(xPointer, yPointer, productPointer)")

def generate_divide(module):
	with yeppp.module.Function(module, 'Divide', 'Division') as function:
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s fraction = x / y;
	*fractionPointer++ = fraction;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_V32fV32f_V32f(xPointer, yPointer, fractionPointer)")
		function.generate("yepCore_Divide_V64fV64f_V64f(xPointer, yPointer, fractionPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s fraction = x / y;
	*fractionPointer++ = fraction;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_V32fS32f_V32f(xPointer, yPointer, fractionPointer)")
		function.generate("yepCore_Divide_V64fS64f_V64f(xPointer, yPointer, fractionPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s x = *xPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s fraction = x / y;
	*fractionPointer++ = fraction;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_S32fV32f_V32f(xPointer, yPointer, fractionPointer)")
		function.generate("yepCore_Divide_S64fV64f_V64f(xPointer, yPointer, fractionPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	const Yep%(OutputType0)s y = *yPointer++;
	x /= y;
	*xPointer++ = x;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_IV32fV32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Divide_IV64fV64f_IV64f(xPointer, yPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	Yep%(OutputType0)s y = *yPointer;
	y = x / y;
	*yPointer++ = y;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_V32fIV32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Divide_V64fIV64f_IV64f(xPointer, yPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	x /= y;
	*xPointer++ = x;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_IV32fS32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Divide_IV64fS64f_IV64f(xPointer, yPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s x = *xPointer;
while (length-- != 0) {
	Yep%(OutputType0)s y = *yPointer;
	y = x / y;
	*yPointer++ = y;
}
return YepStatusOk;"""
		function.generate("yepCore_Divide_S32fIV32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Divide_S64fIV64f_IV64f(xPointer, yPointer)")
	
def generate_copy(module):
	with yeppp.module.Function(module, 'Copy', 'Memory copy') as function:
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s element = *sourcePointer++;
	*destinationPointer++ = element;
}
return YepStatusOk;"""
		function.generate("yepCore_Copy_V8u_V8u(sourcePointer, destinationPointer)")

def generate_zero(module):
	with yeppp.module.Function(module, 'Zero', 'Zero copy') as function:
		function.c_implementation = \
"""while (length-- != 0) {
	*destinationPointer++ = Yep%(OutputType0)s(0);
}
return YepStatusOk;"""
		function.generate("yepCore_Zero__V8u(destinationPointer)")

def generate_reciprocal(module):
	with yeppp.module.Function(module, 'Reciprocal', 'Reciprocal') as function:
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s number = *numberPointer++;
	const Yep%(OutputType0)s reciprocal = Yep%(OutputType0)s(1) / number;
	*reciprocalPointer++ = reciprocal;
}
return YepStatusOk;"""
		function.generate("yepCore_Reciprocal_V32f_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V64f_V64f(numberPointer, reciprocalPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(InputType0)s number = *numberPointer++;
	const Yep%(OutputType0)s reciprocal = Yep%(OutputType0)s(1) / yepBuiltin_Convert_%(InputType0)s_%(OutputType0)s(number);
	*reciprocalPointer++ = reciprocal;
}
return YepStatusOk;"""
		function.generate("yepCore_Reciprocal_V8u_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V8s_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V16u_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V16s_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V32u_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V32s_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V64u_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V64s_V32f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V8u_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V8s_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V16u_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V16s_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V32u_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V32s_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V64u_V64f(numberPointer, reciprocalPointer)")
		function.generate("yepCore_Reciprocal_V64s_V64f(numberPointer, reciprocalPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s number = *numberPointer;
	const Yep%(OutputType0)s reciprocal = Yep%(OutputType0)s(1) / number;
	*numberPointer++ = reciprocal;
}
return YepStatusOk;"""
		function.generate("yepCore_Reciprocal_IV32f_IV32f(numberPointer)")
		function.generate("yepCore_Reciprocal_IV64f_IV64f(numberPointer)")

def generate_convert(module):
	with yeppp.module.Function(module, 'Convert', 'Type conversion') as function:
		
		function.c_implementation = \
"""while (length-- != 0) {
const Yep%(OutputType0)s inputElement = *inputPointer++;
const Yep%(OutputType0)s outputElement = yepBuiltin_Convert_%(InputType0)s_%(OutputType0)s(inputElement);
*outputPointer++ = outputElement;
}
return YepStatusOk;"""
		function.generate("yepCore_Convert_V8s_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V8u_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V16s_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V16u_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V32s_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V32u_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V64s_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V64u_V32f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V8s_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V8u_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V16s_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V16u_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V32s_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V32u_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V64s_V64f(inputPointer, outputPointer)")
		function.generate("yepCore_Convert_V64u_V64f(inputPointer, outputPointer)")

def generate_min(module):
	with yeppp.module.Function(module, 'Min', 'Minimum') as function:

		function.c_implementation = \
"""Yep%(InputType0)s minElement = *arrayPointer++;
while (--length != 0) {
	const Yep%(InputType0)s arrayElement = *arrayPointer++;
	minElement = yepBuiltin_Min_%(InputType0)s%(InputType0)s_%(InputType0)s(arrayElement, minElement);
}
*minPointer++ = minElement;
return YepStatusOk;"""
		function.generate("yepCore_Min_V8s_S8s(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V8u_S8u(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V16s_S16s(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V16u_S16u(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V32s_S32s(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V32u_S32u(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V64s_S64s(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V64u_S64u(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V32f_S32f(arrayPointer, minPointer)")
		function.generate("yepCore_Min_V64f_S64f(arrayPointer, minPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s minimum = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*minPointer++ = minimum;
}
return YepStatusOk;"""
		function.generate("yepCore_Min_V8sV8s_V8s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V8uV8u_V8u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V16sV16s_V16s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V16uV16u_V16u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V32sV32s_V32s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V32uV32u_V32u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V64sV32s_V64s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V64uV32u_V64u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V32fV32f_V32f(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V64fV64f_V64f(xPointer, yPointer, minPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s minimum = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*minPointer++ = minimum;
}
return YepStatusOk;"""
		function.generate("yepCore_Min_V8sS8s_V8s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V8uS8u_V8u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V16sS16s_V16s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V16uS16u_V16u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V32sS32s_V32s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V32uS32u_V32u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V64sS32s_V64s(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V64uS32u_V64u(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V32fS32f_V32f(xPointer, yPointer, minPointer)")
		function.generate("yepCore_Min_V64fS64f_V64f(xPointer, yPointer, minPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	const Yep%(OutputType0)s y = *yPointer++;
	x = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
		function.generate("yepCore_Min_IV8sV8s_IV8s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV8uV8u_IV8u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV16sV16s_IV16s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV16uV16u_IV16u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV32sV32s_IV32s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV32uV32u_IV32u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV64sV32s_IV64s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV64uV32u_IV64u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV32fV32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Min_IV64fV64f_IV64f(xPointer, yPointer)")
	
		function.c_implementation = \
	"""const Yep%(OutputType0)s y = *yPointer;
	while (length-- != 0) {
		Yep%(OutputType0)s x = *xPointer;
		x = yepBuiltin_Min_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
		*xPointer++ = x;
	}
	return YepStatusOk;"""
		function.generate("yepCore_Min_IV8sS8s_IV8s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV8uS8u_IV8u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV16sS16s_IV16s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV16uS16u_IV16u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV32sS32s_IV32s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV32uS32u_IV32u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV64sS32s_IV64s(xPointer, yPointer)")
		function.generate("yepCore_Min_IV64uS32u_IV64u(xPointer, yPointer)")
		function.generate("yepCore_Min_IV32fS32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Min_IV64fS64f_IV64f(xPointer, yPointer)")

def generate_max(module):
	with yeppp.module.Function(module, 'Max', 'Maximum') as function:
	
		function.c_implementation = \
"""Yep%(InputType0)s maxElement = *arrayPointer++;
while (--length != 0) {
	const Yep%(InputType0)s arrayElement = *arrayPointer++;
	maxElement = yepBuiltin_Max_%(InputType0)s%(InputType0)s_%(InputType0)s(arrayElement, maxElement);
}
*maxPointer = maxElement;
return YepStatusOk;"""
		function.generate("yepCore_Max_V8s_S8s(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V8u_S8u(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V16s_S16s(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V16u_S16u(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V32s_S32s(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V32u_S32u(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V64s_S64s(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V64u_S64u(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V32f_S32f(arrayPointer, maxPointer)")
		function.generate("yepCore_Max_V64f_S64f(arrayPointer, maxPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = *yPointer++;
	const Yep%(OutputType0)s maximum = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*maxPointer++ = maximum;
}
return YepStatusOk;"""
		function.generate("yepCore_Max_V8sV8s_V8s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V8uV8u_V8u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V16sV16s_V16s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V16uV16u_V16u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V32sV32s_V32s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V32uV32u_V32u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V64sV32s_V64s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V64uV32u_V64u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V32fV32f_V32f(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V64fV64f_V64f(xPointer, yPointer, maxPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	const Yep%(OutputType0)s x = *xPointer++;
	const Yep%(OutputType0)s maximum = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*maxPointer++ = maximum;
}
return YepStatusOk;"""
		function.generate("yepCore_Max_V8sS8s_V8s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V8uS8u_V8u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V16sS16s_V16s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V16uS16u_V16u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V32sS32s_V32s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V32uS32u_V32u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V64sS32s_V64s(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V64uS32u_V64u(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V32fS32f_V32f(xPointer, yPointer, maxPointer)")
		function.generate("yepCore_Max_V64fS64f_V64f(xPointer, yPointer, maxPointer)")
	
		function.c_implementation = \
"""while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	const Yep%(OutputType0)s y = *yPointer++;
	x = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
		function.generate("yepCore_Max_IV8sV8s_IV8s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV8uV8u_IV8u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV16sV16s_IV16s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV16uV16u_IV16u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV32sV32s_IV32s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV32uV32u_IV32u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV64sV32s_IV64s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV64uV32u_IV64u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV32fV32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Max_IV64fV64f_IV64f(xPointer, yPointer)")
	
		function.c_implementation = \
"""const Yep%(OutputType0)s y = *yPointer;
while (length-- != 0) {
	Yep%(OutputType0)s x = *xPointer;
	x = yepBuiltin_Max_%(OutputType0)s%(OutputType0)s_%(OutputType0)s(x, y);
	*xPointer++ = x;
}
return YepStatusOk;"""
		function.generate("yepCore_Max_IV8sS8s_IV8s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV8uS8u_IV8u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV16sS16s_IV16s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV16uS16u_IV16u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV32sS32s_IV32s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV32uS32u_IV32u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV64sS32s_IV64s(xPointer, yPointer)")
		function.generate("yepCore_Max_IV64uS32u_IV64u(xPointer, yPointer)")
		function.generate("yepCore_Max_IV32fS32f_IV32f(xPointer, yPointer)")
		function.generate("yepCore_Max_IV64fS64f_IV64f(xPointer, yPointer)")

def generate_sum(module):
	with yeppp.module.Function(module, 'Sum', 'Sum of vector elements') as function:

		function.c_implementation = \
"""Yep%(InputType0)s sum = Yep%(InputType0)s(0);
while (length-- != 0) {
const Yep%(InputType0)s arrayElement = *arrayPointer++;
sum += arrayElement;
}
*sumPointer = sum;
return YepStatusOk;"""
		function.generate("yepCore_Sum_V8s_S8s(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V8u_S8u(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V16s_S16s(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V16u_S16u(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V32s_S32s(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V32u_S32u(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V64s_S64s(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V64u_S64u(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V32f_S32f(arrayPointer, sumPointer)")
		function.generate("yepCore_Sum_V64f_S64f(arrayPointer, sumPointer)")

def generate_sum_squares(module):
	with yeppp.module.Function(module, 'SumSquares', 'Sum of squares (squared L2 norm)') as function:
		function.assembly_implementations.append(yeppp.library.core.x64.SumSquares_Vf_Sf_implementation_Nehalem)
		function.assembly_implementations.append(yeppp.library.core.x64.SumSquares_Vf_Sf_implementation_SandyBridge)
		function.assembly_implementations.append(yeppp.library.core.x64.SumSquares_Vf_Sf_implementation_Bulldozer)

		function.c_documentation = \
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
		function.c_implementation = \
"""Yep%(InputType0)s sum = Yep%(InputType0)s(0);
while (length-- != 0) {
	const Yep%(InputType0)s number = *numberPointer++;
	sum += number * number;
}
*sumSquaresPointer = sum;
return YepStatusOk;"""
		function.generate("yepCore_SumSquares_V32f_S32f(numberPointer, sumSquaresPointer)")
		function.generate("yepCore_SumSquares_V64f_S64f(numberPointer, sumSquaresPointer)")

def generate_dotproduct(module):
	with yeppp.module.Function(module, 'DotProduct', 'Dot product') as function:
		function.assembly_implementations.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_Nehalem)
		function.assembly_implementations.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_SandyBridge)
		function.assembly_implementations.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_Haswell)
		function.assembly_implementations.append(yeppp.library.core.x64.DotProduct_VfVf_Sf_implementation_Bulldozer)
#		function.assembly_implementations.append(yeppp.library.core.x64.DotProduct_V64fV64f_S64f_implementation_Bonnell)

		function.c_documentation = \
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
		function.c_implementation = \
"""Yep%(InputType0)s dotProduct = Yep%(InputType0)s(0);
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(InputType0)s y = *yPointer++;
	dotProduct += x * y;
}
*dotProductPointer = dotProduct;
return YepStatusOk;"""
		function.generate("yepCore_DotProduct_V32fV32f_S32f(xPointer, yPointer, dotProductPointer)")
		function.generate("yepCore_DotProduct_V64fV64f_S64f(xPointer, yPointer, dotProductPointer)")

def generate_gather(module):
	with yeppp.module.Function(module, 'Gather', 'Gather') as function:

		function.c_implementation = \
"""while (length-- != 0) {
	const YepSize index = YepSize(*indexPointer++);
	const Yep%(InputType0)s element = sourcePointer[index];
	*destinationPointer++ = element;
}
return YepStatusOk;"""
		function.generate("yepCore_Gather_V8uV8u_V8u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V8uV16u_V8u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V8uV32u_V8u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V8uV64u_V8u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V16uV8u_V16u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V16uV16u_V16u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V16uV32u_V16u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V16uV64u_V16u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V32uV8u_V32u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V32uV16u_V32u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V32uV32u_V32u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V32uV64u_V32u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V64uV8u_V64u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V64uV16u_V64u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V64uV32u_V64u(sourcePointer, indexPointer, destinationPointer)")
		function.generate("yepCore_Gather_V64uV64u_V64u(sourcePointer, indexPointer, destinationPointer)")

def generate_scatter_increment(module):
	with yeppp.module.Function(module, 'ScatterIncrement', 'Scatter-increment') as function:

		function.c_implementation = \
"""while (length-- != 0) {
	const YepSize index = YepSize(*indexPointer++);
	basePointer[index] += 1;
}
return YepStatusOk;"""
		function.generate("yepCore_ScatterIncrement_IV8uV8u_IV8u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV16uV8u_IV16u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV32uV8u_IV32u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV64uV8u_IV64u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV8uV16u_IV8u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV16uV16u_IV16u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV32uV16u_IV32u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV64uV16u_IV64u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV8uV32u_IV8u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV16uV32u_IV16u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV32uV32u_IV32u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV64uV32u_IV64u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV8uV64u_IV8u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV16uV64u_IV16u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV32uV64u_IV32u(basePointer, indexPointer)")
		function.generate("yepCore_ScatterIncrement_IV64uV64u_IV64u(basePointer, indexPointer)")

def generate_scatter_add(module):
	with yeppp.module.Function(module, 'ScatterAdd', 'Scatter-add') as function:

		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(InputType0)s weight = *weightPointer++;
	const YepSize index = YepSize(*indexPointer++);
	basePointer[index] += weight;
}
return YepStatusOk;"""
		function.generate("yepCore_ScatterAdd_IV8uV8uV8u_IV8u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV8uV8u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV8uV16u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV8uV8u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV8uV16u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV8uV32u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV8uV8u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV8uV16u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV8uV32u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV8uV64u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV8uV16uV8u_IV8u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV16uV8u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV16uV16u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV16uV8u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV16uV16u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV16uV32u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV16uV8u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV16uV16u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV16uV32u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV16uV64u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV8uV32uV8u_IV8u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV32uV8u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV32uV16u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV32uV8u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV32uV16u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV32uV32u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV32uV8u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV32uV16u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV32uV32u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV32uV64u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV8uV64uV8u_IV8u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV64uV8u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV16uV64uV16u_IV16u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV64uV8u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV64uV16u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV32uV64uV32u_IV32u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV64uV8u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV64uV16u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV64uV32u_IV64u(basePointer, indexPointer, weightPointer)")
		function.generate("yepCore_ScatterAdd_IV64uV64uV64u_IV64u(basePointer, indexPointer, weightPointer)")

if __name__ == '__main__':
	with yeppp.module.Module('Core', 'Basic arithmetic operations') as module:
# 		generate_copy(module)
# 		generate_zero(module)
		generate_add(module)
		generate_subtract(module)
# 		generate_negate(module)
		generate_multiply(module)
# 		generate_multiply_add(module)
		generate_dotproduct(module)
# 		generate_divide(module)
# 		generate_reciprocal(module)
# 		generate_convert(module)
# 		generate_min(module)
# 		generate_max(module)
# 		generate_sum(module)
		generate_sum_squares(module)
# 		generate_gather(module)
# 		generate_scatter_increment(module)
# 		generate_scatter_add(module)

