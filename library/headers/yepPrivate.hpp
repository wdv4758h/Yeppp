/*
 *                          Yeppp! library header
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 *
 * Copyright (C) 2010-2012 Marat Dukhan
 * Copyright (C) 2012-2013 Georgia Institute of Technology
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the Georgia Institute of Technology nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#pragma once

#include <yepPredefines.h>
#include <yepTypes.h>

#if defined(YEP_PRIVATE_SYMBOL) && defined(YEP_LOCAL_SYMBOL) && defined(YEP_EXPORT_SYMBOL) && defined(YEP_IMPORT_SYMBOL) && defined(YEP_PUBLIC_SYMBOL)
	#undef YEP_PRIVATE_SYMBOL
	#undef YEP_LOCAL_SYMBOL
	#undef YEP_EXPORT_SYMBOL
	#undef YEP_IMPORT_SYMBOL
	#undef YEP_PUBLIC_SYMBOL
	#if defined(__ELF__)
		#if defined(YEP_STATIC_LIBRARY)
			#define YEP_PRIVATE_SYMBOL __attribute__((visibility ("internal")))
			#define YEP_LOCAL_SYMBOL   __attribute__((visibility ("hidden")))
			#define YEP_EXPORT_SYMBOL  __attribute__((visibility ("hidden")))
			#define YEP_IMPORT_SYMBOL  __attribute__((visibility ("hidden")))
		#else
			#define YEP_PRIVATE_SYMBOL __attribute__((visibility ("internal")))
			#define YEP_LOCAL_SYMBOL   __attribute__((visibility ("hidden")))
			#define YEP_EXPORT_SYMBOL  __attribute__((visibility ("default")))
			#define YEP_IMPORT_SYMBOL  __attribute__((visibility ("default")))
		#endif
	#elif defined(YEP_WINDOWS_OS)
		#if defined(YEP_STATIC_LIBRARY)
			#define YEP_PRIVATE_SYMBOL
			#define YEP_LOCAL_SYMBOL
			#define YEP_EXPORT_SYMBOL
			#define YEP_IMPORT_SYMBOL
		#else
			#define YEP_PRIVATE_SYMBOL
			#define YEP_LOCAL_SYMBOL
			#define YEP_EXPORT_SYMBOL __declspec(dllexport)
			#define YEP_IMPORT_SYMBOL __declspec(dllimport)
		#endif
	#else
		#error "Unsupported output format"
	#endif
	#if defined(YEP_BUILD_LIBRARY)
		#define YEP_PUBLIC_SYMBOL YEP_EXPORT_SYMBOL
	#else
		#define YEP_PUBLIC_SYMBOL YEP_IMPORT_SYMBOL
	#endif
#else
	#error "Visibility symbols are not defined"
#endif

#if defined(YEP_DESCRIBE_FUNCTION_IMPLEMENTATION)
	#error "YEP_DESCRIBE_FUNCTION_IMPLEMENTATION macro defined twice"
#else
	#if defined(YEP_DEBUG_LIBRARY)
		#define YEP_DESCRIBE_FUNCTION_IMPLEMENTATION(symbolName, isaFeatures, simdFeatures, systemFeatures, microarchitecture, sourceLanguage, algorithm, optimization) \
			{ symbolName, isaFeatures, simdFeatures, systemFeatures, microarchitecture, sourceLanguage, algorithm, optimization }
	#else
		#define YEP_DESCRIBE_FUNCTION_IMPLEMENTATION(symbolName, isaFeatures, simdFeatures, systemFeatures, microarchitecture, sourceLanguage, algorithm, optimization) \
			{ symbolName, isaFeatures, simdFeatures, systemFeatures, microarchitecture }
	#endif
#endif

typedef YepStatus (*FunctionPointer)();

template <typename Function>
struct FunctionDescriptor {
	Function function;
	Yep64u isaFeatures;
	Yep64u simdFeatures;
	Yep64u systemFeatures;
	YepCpuMicroarchitecture microarchitecture;
#if defined(YEP_DEBUG_LIBRARY)
	const char language[4];
	const char* algorithm;
	const char* optimizations;
#endif
};

template <typename Function>
struct DispatchTableDescriptor {
	const FunctionDescriptor<Function>* table;
#if defined(YEP_DEBUG_LIBRARY)
	const char* name;
#endif
};
