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

/** @defgroup yepLibrary yepLibrary.h: library initialization, information, and support functions. */

#ifdef __cplusplus
extern "C" {
#endif

	/**
	 * @ingroup yepLibrary
	 * @brief	Initialized the @Yeppp library.
	 * @retval	#YepStatusOk	The library is successfully initialized.
	 * @retval	#YepStatusSystemError	An uncoverable error inside the OS kernel occurred during library initialization.
	 * @see	yepLibrary_Release
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_Init();
	/**
	 * @ingroup yepLibrary
	 * @brief	Deinitialized the @Yeppp library and releases the consumed system resources.
	 * @retval	#YepStatusOk	The library is successfully initialized.
	 * @retval	#YepStatusSystemError	The library failed to release some of the resources due to a failed call to the OS kernel.
	 * @see	yepLibrary_Init
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_Release();
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns basic information about the library version.
	 * @return	A pointer to a structure describing @Yeppp library version.
	 */
	YEP_PUBLIC_SYMBOL const struct YepLibraryVersion *YEPABI yepLibrary_GetVersion();
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns a string representation of an integer value in a enumeration.
	 * @param[in]	enumerationType	Indicates the type of integer value passed to the function in @a enumerationValue parameter.
	 * @param[in]	enumerationValue	The enumeration value of type specified in @a enumerationType which must be converted to string.
	 * @param[out]	buffer	An output buffer of size specified by the @a length parameter. On successfull return the buffer will contain the string representation of @a enumerationValue. The string representation does not include the terminating zero. If the function fails, the content of the buffer is not changed.
	 * @param[in,out]	length	On function call this variable must contain the length (in bytes) of the buffer. On successfull return this variable will contain the length (in bytes) of the string written to the buffer. If the function fails with YepStatusInsufficientBuffer error, on return the @a length variable will contain the required size of the buffer. In the function fails with any other error, this variable is unchanged.
	 * @retval	#YepStatusOk	The string is successfully stored in the @a buffer.
	 * @retval	#YepStatusNullPointer	Buffer or length pointer is null.
	 * @retval	#YepStatusInvalidArgument	Either @a enumerationType or @a enumerationValue contain values unknown to the library.
	 * @retval	#YepStatusInsufficientBuffer	The output buffer is too small for the string. The content of the output buffer is unchanged, and the required size of the buffer is returned in the length variable.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetString(enum YepEnumeration enumerationType, Yep32u enumerationValue, void *buffer, YepSize *length);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns information about the supported ISA extensions (excluding SIMD extensions)
	 * @param[out]	isaFeatures	Pointer to a 64-bit mask where information about the supported ISA extensions will be stored.
	 * @retval	#YepStatusOk	The information successfully stored to the mask pointed by @a isaFeatures parameter.
	 * @retval	#YepStatusNullPointer	The @a isaFeatures pointer is null.
	 * @see	yepLibrary_GetCpuSimdFeatures, yepLibrary_GetCpuSystemFeatures
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuIsaFeatures(Yep64u *isaFeatures);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns information about the supported SIMD extensions
	 * @param[out]	simdFeatures	Pointer to a 64-bit mask where information about the supported SIMD extensions will be stored.
	 * @retval	#YepStatusOk	The information successfully stored to the mask pointed by @a simdFeatures parameter.
	 * @retval	#YepStatusNullPointer	The @a simdFeatures pointer is null.
	 * @see	yepLibrary_GetCpuIsaFeatures, yepLibrary_GetCpuSystemFeatures
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuSimdFeatures(Yep64u *simdFeatures);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns information about processor features other than ISA extensions, and OS features related to CPU.
	 * @param[out]	systemFeatures	Pointer to a 64-bit mask where information about extended processor and system features will be stored.
	 * @retval	#YepStatusOk	The information successfully stored to the mask pointed by @a systemFeatures parameter.
	 * @retval	#YepStatusNullPointer	The @a systemFeatures pointer is null.
	 * @see	yepLibrary_GetCpuIsaFeatures, yepLibrary_GetCpuSimdFeatures
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuSystemFeatures(Yep64u *systemFeatures);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns information about the vendor of the processor.
	 * @param[out]	vendor	Pointer to a variable where information about the processor vendor will be stored.
	 * @retval	#YepStatusOk	The information successfully stored to the variable pointed by @a vendor parameter.
	 * @retval	#YepStatusNullPointer	The @a vendor pointer is null.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuVendor(enum YepCpuVendor *vendor);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns the type of processor architecture.
	 * @param[out]	architecture	Pointer to a variable where information about the processor architecture will be stored.
	 * @retval	#YepStatusOk	The information successfully stored to the variable pointed by @a architecture parameter.
	 * @retval	#YepStatusNullPointer	The @a architecture pointer is null.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuArchitecture(enum YepCpuArchitecture *architecture);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns the type of processor microarchitecture used.
	 * @param[out]	microarchitecture	Pointer to a variable where information about the processor microarchitecture will be stored.
	 * @retval	#YepStatusOk	The information successfully stored to the variable pointed by @a microarchitecture parameter.
	 * @retval	#YepStatusNullPointer	The @a microarchitecture pointer is null.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuMicroarchitecture(enum YepCpuMicroarchitecture *microarchitecture);
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuDataCacheSize(Yep32u level, Yep32u *cacheSize);
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuInstructionCacheSize(Yep32u level, Yep32u *cacheSize);
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetLogicalCoresCount(Yep32u *logicalCoresCount);
	/**
	 * @ingroup yepLibrary
	 * @brief	Initializes the processor cycle counter and starts counting the processor cycles.
	 * @details	In the current implementation this function can use:
	 *         	 - RDTSC or RDTSCP instructions on x86 and x86-64.
	 *         	 - ITC register on IA64.
	 *         	 - Linux perf events subsystem on ARM and MIPS. This option requires unrestricted access to perf events subsystem (file /proc/sys/kernel/perf_event_paranoid should contain 0 or -1, if this file does not exist, the kernel is compiled without perf events subsystem).
	 *         	 - PMCCNTR register on ARM if user-mode access to performance counters is enabled and the counter is properly configured. This option is intended for use with the kernel-mode driver in drivers/arm_pmu directory in @Yeppp distribution. This option provides only 32-bit cycle counter.
	 * @warning	The state is not guaranteed to be the current processor cycle counter value, and should not be used as such.
	 * @warning	This function may allocate system resources.
	 *         	To avoid resource leak, always match a successfull call to #yepLibrary_GetCpuCyclesAcquire with a call to #yepLibrary_GetCpuCyclesRelease.
	 * @warning	The cycle counters are not guaranteed to be syncronized across different processors/cores in a multiprocessor/multicore system.
	 *         	It is recommended to bind the current thread to a particular logical processor before using this function.
	 * @param[out]	state	Pointer to a variable where the state of the cycle counter will be stored.
	 *            	     	If the function fails, the value of the state variable is not changed.
	 * @retval	#YepStatusOk	The cycle counter successfully initialized and its state is stored to the variable pointed by @a state parameter.
	 * @retval	#YepStatusNullPointer	The @a state pointer is null.
	 * @retval	#YepStatusUnsupportedHardware	The processor does not have cycle counter.
	 * @retval	#YepStatusUnsupportedSoftware	The operating system does not provide access to the CPU cycle counter.
	 * @retval	#YepStatusSystemError	An attempt to initialize cycle counter failed inside the OS kernel.
	 * @see	yepLibrary_GetCpuCyclesRelease
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuCyclesAcquire(Yep64u *state);
	/**
	 * @ingroup yepLibrary
	 * @brief	Stops counting the processor cycles, releases the system resources associated with the cycle counter, and returns the number of cycles elapsed.
	 * @param[in,out]	state	Pointer to a variable with the state of the cycle counter saved by #yepLibrary_GetCpuCyclesAcquire.
	 *               	     	The cycle counter should be released only once, and the function zeroes out the state variable.
	 * @param[out]	cycles	Pointer to a variable where the number of cycles elapsed will be stored.
	 *            	      	The pointer can be the same as @a state pointer.
	 * @retval	#YepStatusOk	The number of cycles elapsed is saved to the variable pointed by @a cycles parameter, and the system resources are successfully released.
	 * @retval	#YepStatusNullPointer	Either the @a state pointer or the @a cycles pointer is null.
	 * @retval	#YepStatusInvalidState	The @a state variable does not specify a valid state of the cycle counter.
	 *        	                     	This can happen if the @a state variable was not initialized, or it was released previously.
	 * @retval	#YepStatusUnsupportedHardware	The processor does not have cycle counter.
	 * @retval	#YepStatusUnsupportedSoftware	The operating system does not provide access to the CPU cycle counter.
	 * @retval	#YepStatusSystemError	An attempt to read the cycle counter or release the OS resources failed inside the OS kernel.
	 * @see yepLibrary_GetCpuCyclesAcquire
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetCpuCyclesRelease(Yep64u *state, Yep64u *cycles);
	/**
	 * @ingroup yepLibrary
	 * @brief	Initializes the specified energy counter and starts energy measurements.
	 * @param[in]	type	The type of the energy counter to initialize.
	 * @param[out]	state	The state variable corresponding to the initialized energy counter.
	 *            	     	If the function fails, the value of the state variable is not changed.
	 *            	     	It is recommended to initialize the state variables to all zeroes before calling this function.
	 * @retval	#YepStatusOk	The energy counter successfully initialized and its state is store to the variable pointed by @a state parameter.
	 * @retval	#YepStatusNullPointer	The @a state pointer is null.
	 * @retval	#YepStatusInvalidArgument	The @a type parameter does not specify a valid energy counter type.
	 * @retval	#YepStatusUnsupportedHardware	The hardware does not support the requested energy counter type.
	 * @retval	#YepStatusUnsupportedSoftware	The operating system does not provide access to the specified energy counter.
	 * @retval	#YepStatusSystemError	An attempt to read the energy counter or release the OS resources failed inside the OS kernel.
	 * @retval	#YepStatusAccessDenied	The user does not possess the required access rights to read the energy counter.
	 * @see yepLibrary_GetEnergyCounterRelease
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetEnergyCounterAcquire(enum YepEnergyCounterType type, struct YepEnergyCounter *state);
	/**
	 * @ingroup yepLibrary
	 * @brief	Stops the energy counter, releases the system resources associated with the energy counter, and reads the counter measurement.
	 * @param[in,out]	state	Pointer to a variable with the state of the energy counter saved by #yepLibrary_GetEnergyCounterAcquire.
	 *               	     	The energy counter should be released only once, and the function zeroes out the state variable.
	 * @param[out]	measurement	Pointer to a variable where the number of cycles elapsed will be stored.
	 *            	      	The pointer can be the same as @a state pointer.
	 * @retval	#YepStatusOk	The energy counter measurement is saved to the variable pointed by @a measurement parameter, and the system resources are successfully released.
	 * @retval	#YepStatusNullPointer	Either the @a state pointer or the @a measurement pointer is null.
	 * @retval	#YepStatusInvalidState	The @a state variable does not specify a valid state of the energy counter.
	 *        	                      	This can happen if the @a state variable was not initialized, or it was released previously.
	 * @retval	#YepStatusUnsupportedHardware	The hardware does not support the requested energy counter type.
	 * @retval	#YepStatusUnsupportedSoftware	The operating system does not provide access to the specified energy counter.
	 * @retval	#YepStatusSystemError	An attempt to read the energy counter or release the OS resources failed inside the OS kernel.
	 * @retval	#YepStatusAccessDenied	The user does not possess the required access rights to read the energy counter.
	 * @see yepLibrary_GetEnergyCounterAcquire
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetEnergyCounterRelease(struct YepEnergyCounter *state, Yep64f *measurement);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns the number of ticks of the high-resolution system timer.
	 * @param[out]	ticks	Pointer to a variable where the number of timer ticks will be stored.
	 *            	     	If the function fails, the value of the variable at this address is not changed.
	 * @retval	#YepStatusOk	The number of timer ticks is successfully stored to the variable pointed by @a ticks parameter.
	 * @retval	#YepStatusNullPointer	The @a ticks pointer is null.
	 * @retval	#YepStatusSystemError	An attempt to read the high-resolution timer failed inside the OS kernel.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetTimerTicks(Yep64u *ticks);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns the number of ticks of the system timer per second.
	 * @param[out]	frequency	Pointer to a variable where the number of timer ticks per second will be stored.
	 * @retval	#YepStatusOk	The number of timer ticks is successfully stored to the variable pointed by @a frequency parameter.
	 * @retval	#YepStatusNullPointer	The @a frequency pointer is null.
	 * @retval	#YepStatusSystemError	An attempt to query the high-resolution timer parameters failed inside the OS kernel.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetTimerFrequency(Yep64u *frequency);
	/**
	 * @ingroup yepLibrary
	 * @brief	Returns the minimum time difference in nanoseconds which can be measured by the high-resolution system timer.
	 * @param[out]	accuracy	Pointer to a variable where the timer accuracy will be stored.
	 * @retval	#YepStatusOk	The accuracy of the timer is successfully stored to the variable pointed by @a accuracy parameter.
	 * @retval	#YepStatusNullPointer	The @a accuracy pointer is null.
	 * @retval	#YepStatusSystemError	An attempt to measure the accuracy of high-resolution timer failed inside the OS kernel.
	 */
	YEP_PUBLIC_SYMBOL enum YepStatus YEPABI yepLibrary_GetTimerAccuracy(Yep64u *accuracy);

#ifdef __cplusplus
}
#endif
