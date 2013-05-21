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

		function.c_documentation = \
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
		function.java_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Log_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
		function.generate("yepMath_Log_V64f_V64f(xPointer, yPointer)")

def generate_exp(module):
	with yeppp.module.Function(module, 'Exp', 'Base-e exponent') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Bobcat)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_K10)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Bulldozer)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.Exp_V64f_V64f_Haswell)

		function.c_documentation = \
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
		function.java_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Exp_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
		function.generate("yepMath_Exp_V64f_V64f(xPointer, yPointer)")

def generate_sin(module):
	with yeppp.module.Function(module, 'Sin', 'Sine') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_Nehalem)
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_SandyBridge)
		function.assembly_implementations.append(yeppp.library.math.x64.Sin_V64f_V64f_Bulldozer)
	
		function.c_documentation = \
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
		function.java_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Sin_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
		function.generate("yepMath_Sin_V64f_V64f(xPointer, yPointer)")

def generate_tan(module):
	with yeppp.module.Function(module, 'Tan', 'Tangent') as function:
		function.assembly_implementations.append(yeppp.library.math.x64.Tan_V64f_V64f_Bulldozer)
	
		function.c_documentation = \
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
		function.java_documentation = \
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
		function.c_implementation = \
"""while (length-- != 0) {
	const Yep%(InputType0)s x = *xPointer++;
	const Yep%(OutputType0)s y = yepBuiltin_Tan_%(InputType0)s_%(OutputType0)s(x);
	*yPointer++ = y;
}
return YepStatusOk;"""
		function.generate("yepMath_Tan_V64f_V64f(xPointer, yPointer)")

if __name__ == '__main__':
	with yeppp.module.Module('Math', 'Vector mathematical functions') as module:
		generate_log(module)
		generate_exp(module)
		generate_sin(module)
		generate_tan(module)
# 		generate_sqrt(module)
