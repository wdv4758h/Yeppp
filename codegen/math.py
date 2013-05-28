#
#                      Yeppp! library implementation
#
# This file is part of Yeppp! library and licensed under the New BSD license.
# See library/LICENSE.txt for the full text of the license.
#

import yeppp.module

import yeppp.library.math.x86
import yeppp.library.math.x64

def generate_log(module):
	with yeppp.module.Function(module, 'Log', 'Natural logarithm') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Log_V64f_V64f_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.Log_V64f_V64f_K10)
		function.assembly_implementations.append(yeppp.library.math.x64.Log_V64f_V64f_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.Log_V64f_V64f_Bobcat)
		function.assembly_implementations.append(yeppp.library.math.x64.Log_V64f_V64f_Bulldozer)

		function.c_documentation = """
@brief	Computes logarithm on %(InputType0)s elements.
@param[in]	x	Pointer the input array.
@param[out]	y	Pointer the output array.
@param[in]	length	The length of the arrays pointed by @a x and @a y.
@retval	#YepStatusOk	The computations finished successfully.
@retval	#YepStatusNullPointer	One of the @a xPointer or @a yPointer arguments is null.
@retval	#YepStatusMisalignedPointer	One of the @a xPointer or @a yPointer arguments is not properly aligned.
"""
		function.java_documentation = """
@brief	Computes logarithm on %(InputType0)s elements.
@param[in]	xArray	Input array.
@param[in]   xOffset Offset of the first element in @a xArray.
@param[out]	yArray	Output array.
@param[in]   yOffset Offset of the first element in @a yArray.
@param[in]	length	The length of the subarrays to be used in computation.
@throws	NullPointerException	If @a xArray or @a yArray argument is null.
@throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
@throws	NegativeArraySizeException	If the @a length argument is null.
@throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
@throws	MisalignedPointerError	If one of the arrays is not properly aligned.
"""
		function.c_implementation = """
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Log_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;
"""
		function.generate("yepMath_Log_V64f_V64f(x, y, YepSize length)")

def generate_exp(module):
	with yeppp.module.Function(module, 'Exp', 'Base-e exponent') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Bobcat)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_K10)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Bulldozer)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Haswell)

		function.c_documentation = """
@brief	Computes exponent on %(InputType0)s elements.
@param[in]	x	Pointer the input array.
@param[out]	y	Pointer the output array.
@param[in]	length	The length of the arrays pointed by @a x and @a y.
@retval	#YepStatusOk	The computations finished successfully.
@retval	#YepStatusNullPointer	One of the @a x or @a y arguments is null.
@retval	#YepStatusMisalignedPointer	One of the @a x or @a y arguments is not properly aligned.
"""
		function.java_documentation = """
@brief	Computes exponent on %(InputType0)s elements.
@param[in]	xArray	Input array.
@param[in]   xOffset Offset of the first element in @a xArray.
@param[out]	yArray	Output array.
@param[in]   yOffset Offset of the first element in @a yArray.
@param[in]	length	The length of the subarrays to be used in computation.
@throws	NullPointerException	If @a xArray or @a yArray argument is null.
@throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
@throws	NegativeArraySizeException	If the @a length argument is null.
@throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
@throws	MisalignedPointerError	If one of the arrays is not properly aligned.
"""
		function.c_implementation = """
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Exp_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;
"""
		function.generate("yepMath_Exp_V64f_V64f(x, y, YepSize length)")

def generate_sin(module):
	with yeppp.module.Function(module, 'Sin', 'Sine') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_Bulldozer)
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_Haswell)

		function.c_documentation = """
@brief	Computes sine on %(InputType0)s elements.
@param[in]	x	Pointer the input array.
@param[out]	y	Pointer the output array.
@param[in]	length	The length of the arrays pointed by @a x and @a y.
@retval	#YepStatusOk	The computations finished successfully.
@retval	#YepStatusNullPointer	One of the @a x or @a y arguments is null.
@retval	#YepStatusMisalignedPointer	One of the @a x or @a y arguments is not properly aligned.
"""
		function.java_documentation = """
@brief	Computes sine on %(InputType0)s elements.
@param[in]	xArray	Input array.
@param[in]   xOffset Offset of the first element in @a xArray.
@param[out]	yArray	Output array.
@param[in]   yOffset Offset of the first element in @a yArray.
@param[in]	length	The length of the subarrays to be used in computation.
@throws	NullPointerException	If @a xArray or @a yArray argument is null.
@throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
@throws	NegativeArraySizeException	If the @a length argument is null.
@throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
@throws	MisalignedPointerError	If one of the arrays is not properly aligned.
"""
		function.c_implementation = """
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Sin_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;
"""
		function.generate("yepMath_Sin_V64f_V64f(x, y, YepSize length)")

def generate_cos(module):
	with yeppp.module.Function(module, 'Cos', 'Cosine') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Cos_V64f_V64f_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.Cos_V64f_V64f_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.Cos_V64f_V64f_Bulldozer)
		function.assembly_implementations.append(yeppp.library.math.x64.Cos_V64f_V64f_Haswell)

		function.c_documentation = """
@brief	Computes cosine on %(InputType0)s elements.
@param[in]	x	Pointer the input array.
@param[out]	y	Pointer the output array.
@param[in]	length	The length of the arrays pointed by @a x and @a y.
@retval	#YepStatusOk	The computations finished successfully.
@retval	#YepStatusNullPointer	One of the @a x or @a y arguments is null.
@retval	#YepStatusMisalignedPointer	One of the @a x or @a y arguments is not properly aligned.
"""
		function.java_documentation = """
@brief	Computes cosine on %(InputType0)s elements.
@param[in]	xArray	Input array.
@param[in]   xOffset Offset of the first element in @a xArray.
@param[out]	yArray	Output array.
@param[in]   yOffset Offset of the first element in @a yArray.
@param[in]	length	The length of the subarrays to be used in computation.
@throws	NullPointerException	If @a xArray or @a yArray argument is null.
@throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
@throws	NegativeArraySizeException	If the @a length argument is null.
@throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
@throws	MisalignedPointerError	If one of the arrays is not properly aligned.
"""
		function.c_implementation = """
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Cos_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;
"""
		function.generate("yepMath_Cos_V64f_V64f(x, y, YepSize length)")

def generate_tan(module):
	with yeppp.module.Function(module, 'Tan', 'Tangent') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Tan_V64f_V64f_Bulldozer)
	
		function.c_documentation = """
@brief	Computes tangent on %(InputType0)s elements.
@param[in]	x	Pointer the array of elements to compute tangent on.
@param[out]	y	Pointer the output array.
@param[in]	length	The length of the arrays pointed by @a x and @a y.
@retval	#YepStatusOk	The computations finished successfully.
@retval	#YepStatusNullPointer	One of the @a x or @a y arguments is null.
@retval	#YepStatusMisalignedPointer	One of the @a x or @a y arguments is not properly aligned.
"""
		function.java_documentation = """
@brief	Computes tangent on %(InputType0)s elements.
@param[in]	xArray	Input array.
@param[in]   xOffset Offset of the first element in @a xArray.
@param[out]	yArray	Output array.
@param[in]   yOffset Offset of the first element in @a yArray.
@param[in]	length	The length of the subarrays to be used in computation.
@throws	NullPointerException	If @a xArray or @a yArray argument is null.
@throws	InvalidArgumentException	If the @a xOffset or @a yOffset argument is negative.
@throws	NegativeArraySizeException	If the @a length argument is null.
@throws  IndexOutOfBoundsException If @a xOffset + @a length exceeds the length of @a xArray array or @a yOffset + @a length exceeds the length of @a yArray array.
@throws	MisalignedPointerError	If one of the arrays is not properly aligned.
"""
		function.c_implementation = """
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Tan_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;
"""
		function.generate("yepMath_Tan_V64f_V64f(x, y, YepSize length)")

def generate_evaluate_polynomial(module):
	with yeppp.module.Function(module, 'EvaluatePolynomial', 'Polynomial evaluation') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_VfVf_Vf_SSE2)
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_V64fV64f_V64f_Bonnell)
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_V32fV32f_V32f_Bonnell)
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_VfVf_Vf_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_VfVf_Vf_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_VfVf_Vf_Bulldozer)
		function.assembly_implementations.append(yeppp.library.math.x64.EvaluatePolynomial_VfVf_Vf_Haswell)

		function.c_documentation = """
@brief	Evaluates polynomial with %(InputType0)s coefficients on an array of %(InputType0)s elements.
@param[in]	x	Pointer to the array of elements on which the polynomial will be evaluated.
@param[in]	coef	Pointer to the array of polynomial coefficients.
@param[out]	y	Pointer the array where the result of polynomial evaluation will be stored.
@param[in]	coefCount	Number of polynomial coefficients. This should equal the polynomial degree plus one.
@param[in]	length	Number of elements in the arrays specified by @a x and @a y.
@retval	#YepStatusOk	The computations finished successfully.
@retval	#YepStatusNullPointer	Either @a x or @a y arguments is null.
@retval	#YepStatusMisalignedPointer	Either @a x or @a y arguments is not properly aligned.
"""
		function.c_implementation = """
if YEP_UNLIKELY(coefCount == 0) {
	return YepStatusInvalidArgument;
}
while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	Yep%(OutputType0)s y = coefPointer[coefCount - 1];
	for (YepSize coefIndex = coefCount - 1; coefIndex != 0; coefIndex--) {
		const Yep%(InputType0)s coef = coefPointer[coefIndex - 1];
		y = yepBuiltin_MultiplyAdd_%(OutputType0)s%(InputType1)s%(InputType0)s_%(OutputType0)s(y, x, coef);
	}
	*yPointer++ = y;
}
return YepStatusOk;
"""
		function.generate("yepMath_EvaluatePolynomial_V32fV32f_V32f(coef[coefCount], x, y, YepSize coefCount, YepSize length)")
		function.generate("yepMath_EvaluatePolynomial_V64fV64f_V64f(coef[coefCount], x, y, YepSize coefCount, YepSize length)")

if __name__ == '__main__':
	with yeppp.module.Module('Math', 'Vector mathematical functions') as module:
		generate_log(module)
		generate_exp(module)
		generate_sin(module)
		generate_cos(module)
		generate_tan(module)
		generate_evaluate_polynomial(module)
# 		generate_sqrt(module)
