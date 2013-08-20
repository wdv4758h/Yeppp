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

#ifndef YEP_PREPROCESS_TO_XML
	#pragma once
#endif

#define YEP_MAJOR_VERSION 0
#define YEP_MINOR_VERSION 9
#define YEP_PATCH_VERSION 9
#define YEP_BUILD_VERSION 0
#define YEP_RELEASE_NAME "Beta 3"

#define YEP_PREPROCESSOR_NUMBER_AS_STRING_HELPER(number) #number
#define YEP_PREPROCESSOR_NUMBER_AS_STRING(number) YEP_PREPROCESSOR_NUMBER_AS_STRING_HELPER(number)

#define YEP_MAJOR_VERSION_STR       YEP_PREPROCESSOR_NUMBER_AS_STRING(YEP_MAJOR_VERSION)
#define YEP_MINOR_VERSION_STR       YEP_PREPROCESSOR_NUMBER_AS_STRING(YEP_MINOR_VERSION)
#define YEP_PATCH_VERSION_STR       YEP_PREPROCESSOR_NUMBER_AS_STRING(YEP_PATCH_VERSION)
#define YEP_BUILD_VERSION_STR       YEP_PREPROCESSOR_NUMBER_AS_STRING(YEP_BUILD_VERSION)

#define YEP_FULL_VERSION_STR YEP_MAJOR_VERSION_STR "." YEP_MINOR_VERSION_STR "." YEP_PATCH_VERSION_STR "." YEP_BUILD_VERSION_STR " (" YEP_RELEASE_NAME ")"
