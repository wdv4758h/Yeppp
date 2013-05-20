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

/**
 * @mainpage Yeppp! library documentation for C programmers
 *
 * @section Introduction	Introduction
 *
 * @Yeppp library is a collection of low-level functions optimized for modern CPU microarchitectures.
 * Each library function has several versions optimized for different processor microarchitectures.
 * During initialization @Yeppp library detects the processor it is running on, and chooses the optimal function implementations.
 *
 * Additionally, the library provides information about the CPU, such as processor vendor and microarchitecture,
 * and an OS- and hardware-independent interface to processor cycle counters, and high-resolution timers.
 *
 * @section Platforms	Supported Platforms
 *
 * In this release @Yeppp library supports the following hardware and software platforms:
 *  - x86 on Windows, Linux, and Android.
 *  - x86-64 on Windows and Linux.
 *  - ARM on Linux and Android.
 *  - MIPS on Android.
 *
 * @example CpuInfo.c
 *
 * This example shows how to use @Yeppp library to get information about processor and supported instruction extensions:
 *
 * @example SystemTimer.c
 *
 * This example shows how to use @Yeppp library to do cross-platform measurements of execution time using high-frequency system timer:
 *
 * @example CpuCycles.c
 *
 * This example shows how to use @Yeppp library to measure the execution time in CPU cycles:
 *
 * @example Entropy.c
 *
 * This example shows how to use @Yeppp library to compute the entropy of a distribution given by its probabilities:
 *
 */


#include <yepPredefines.h>
#include <stddef.h>

typedef unsigned char      Yep8u;
typedef unsigned short     Yep16u;
typedef unsigned int       Yep32u;
typedef unsigned long long Yep64u;

typedef signed char        Yep8s;
typedef signed short       Yep16s;
typedef signed int         Yep32s;
typedef signed long long   Yep64s;

typedef float              Yep32f;
typedef double             Yep64f;
#if defined(YEP_X86_CPU) || defined(YEP_X64_CPU)
	#if defined(YEP_GCC_COMPATIBLE_COMPILER) || (defined(YEP_INTEL_COMPILER_FOR_WINDOWS) && (__LONG_DOUBLE_SIZE__ == 80))
		#define YEP_COMPILER_SUPPORTS_YEP80F_TYPE
		typedef long double Yep80f;
	#endif
#endif

typedef size_t             YepSize;

#ifndef __cplusplus
	#if defined(YEP_MICROSOFT_COMPILER)
		/* OMG! I can't believe it still doesn't have stdbool.h in 2012! */
		typedef unsigned char      YepBoolean;
		#define YepBooleanTrue     1
		#define YepBooleanFalse    0
	#else
		#include <stdbool.h>
		typedef bool               YepBoolean;
		#define YepBooleanTrue     true
		#define YepBooleanFalse    false
	#endif
#else
	typedef bool                       YepBoolean;
	const YepBoolean YepBooleanTrue  = true;
	const YepBoolean YepBooleanFalse = false;
#endif

typedef Yep16u Yep16f;

#pragma pack(push, 1)

struct Yep16fc {
	Yep16f re;
	Yep16f im;
};

struct Yep32fc {
	Yep32f re;
	Yep32f im;
};

struct Yep64fc {
	Yep64f re;
	Yep64f im;
};

struct Yep32df {
	Yep32f high;
	Yep32f low;
};

struct Yep64df {
	Yep64f high;
	Yep64f low;
};

#if defined(YEP_LITTLE_ENDIAN_BYTE_ORDER)
	typedef struct {
		Yep64u low;
		Yep64u high;
	} Yep128u;

	typedef struct {
		Yep64u low;
		Yep64s high;
	} Yep128s;
#elif defined(YEP_BIG_ENDIAN_BYTE_ORDER)
	typedef struct {
		Yep64u high;
		Yep64u low;
	} Yep128u;

	typedef struct {
		Yep64s high;
		Yep64u low;
	} Yep128s;
#else
	#error "Unknown or supported byte order"
#endif

#pragma pack(pop)

/**
 * @ingroup	yepLibrary
 * @brief	Contains information about @Yeppp library version.
 * @see	yepLibrary_GetVersion
 */
struct YepLibraryVersion {
	/** @brief The major version. Library releases with the same major versions are guaranteed to be API- and ABI-compatible. */
	Yep32u major;
	/** @brief The minor version. A change in minor versions indicates addition of new features, and major bug-fixes. */
	Yep32u minor;
	/** @brief The patch level. A version with a higher patch level indicates minor bug-fixes. */
	Yep32u patchLevel;
	/** @brief The build number. The build number is unique for the fixed combination of major, minor, and patch-level versions. */
	Yep32u build;
	/** @brief A UTF-8 string with a human-readable name of this release. May contain non-ASCII characters. */
	const char* releaseName;
};

/**
 * @ingroup	yepLibrary
 * @brief	Indicates success or failure of @Yeppp functions.
 */
enum YepStatus {
	/** @brief Operation finished successfully. */
	YepStatusOk = 0,
	/** @brief Function call failed because one of the pointer arguments is null. */
	YepStatusNullPointer = 1,
	/** @brief Function call failed because one of the pointer arguments is not properly aligned. */
	YepStatusMisalignedPointer = 2,
	/** @brief Function call failed because one of the integer arguments has unsupported value. */
	YepStatusInvalidArgument = 3,
	/** @brief Function call failed because some of the data passed to the function has invalid format or values. */
	YepStatusInvalidData = 4,
	/** @brief Function call failed because one of the state objects passed is corrupted. */
	YepStatusInvalidState = 5,
	/** @brief Function call failed because the system hardware does not support the requested operation. */
	YepStatusUnsupportedHardware = 6,
	/** @brief Function call failed because the operating system does not support the requested operation. */
	YepStatusUnsupportedSoftware = 7,
	/** @brief Function call failed because the provided output buffer is too small or exhausted. */
	YepStatusInsufficientBuffer = 8,
	/** @brief Function call failed because the library could not allocate the memory. */
	YepStatusOutOfMemory = 9,
	/** @brief Function call failed because some of the system calls inside the function failed. */
	YepStatusSystemError = 10,
	/** @brief Function call failed because access to the requested resource is not allowed for this user. */
	YepStatusAccessDenied = 11
};

/**
 * @ingroup	yepLibrary
 * @brief	The basic instruction set architecture of the processor.
 * @details	The ISA is always known at compile-time.
 * @see	yepLibrary_GetCpuArchitecture
 */
enum YepCpuArchitecture {
	/** @brief	Instruction set architecture is not known to the library. */
	/** @details	This value is never returned on supported architectures. */
	YepCpuArchitectureUnknown = 0,
	/** @brief	x86 or x86-64 ISA. */
	YepCpuArchitectureX86 = 1,
	/** @brief	ARM ISA. */
	YepCpuArchitectureARM = 2,
	/** @brief	MIPS ISA. */
	YepCpuArchitectureMIPS = 3,
	/** @brief	PowerPC ISA. */
	YepCpuArchitecturePowerPC = 4,
	/** @brief	IA64 ISA. */
	YepCpuArchitectureIA64 = 5,
	/** @brief	SPARC ISA. */
	YepCpuArchitectureSPARC = 6
};

/**
 * @ingroup	yepLibrary
 * @brief	The company which designed the processor microarchitecture.
 * @see	yepLibrary_GetCpuVendor
 */
enum YepCpuVendor {
	/** @brief	Processor vendor is not known to the library, or the library failed to get vendor information from the OS. */
	YepCpuVendorUnknown = 0,
	
	/* x86/x86-64 CPUs */
	
	/** @brief	Intel Corporation. Vendor of x86, x86-64, IA64, and ARM processor microarchitectures. */
	/** @details	Sold its ARM design subsidiary in 2006. The last ARM processor design was released in 2004. */
	YepCpuVendorIntel = 1,
	/** @brief	Advanced Micro Devices, Inc. Vendor of x86 and x86-64 processor microarchitectures. */
	YepCpuVendorAMD = 2,
	/** @brief	VIA Technologies, Inc. Vendor of x86 and x86-64 processor microarchitectures. */
	/** @details	Processors are designed by Centaur Technology, a subsidiary of VIA Technologies. */
	YepCpuVendorVIA = 3,
	/** @brief	Transmeta Corporation. Vendor of x86 processor microarchitectures. */
	/** @details	Now defunct. The last processor design was released in 2004. */
	/**         	Transmeta processors implemented VLIW ISA and used binary translation to execute x86 code. */
	YepCpuVendorTransmeta = 4,
	/** @brief	Cyrix Corporation. Vendor of x86 processor microarchitectures. */
	/** @details	Now defunct. The last processor design was released in 1996. */
	YepCpuVendorCyrix = 5,
	/** @brief	Rise Technology. Vendor of x86 processor microarchitectures. */
	/** @details	Now defunct. The last processor design was released in 1999. */
	YepCpuVendorRise = 6,
	/** @brief	National Semiconductor. Vendor of x86 processor microarchitectures. */
	/** @details	Sold its x86 design subsidiary in 1999. The last processor design was released in 1998. */
	YepCpuVendorNSC = 7,
	/** @brief	Silicon Integrated Systems. Vendor of x86 processor microarchitectures. */
	/** @details	Sold its x86 design subsidiary in 2001. The last processor design was released in 2001. */
	YepCpuVendorSiS = 8,
	/** @brief	NexGen. Vendor of x86 processor microarchitectures. */
	/** @details	Now defunct. The last processor design was released in 1994. */
	/**         	NexGen designed the first x86 microarchitecture which decomposed x86 instructions into simple microoperations. */
	YepCpuVendorNexGen = 9,
	/** @brief	United Microelectronics Corporation. Vendor of x86 processor microarchitectures. */
	/** @details	Ceased x86 in the early 1990s. The last processor design was released in 1991. */
	/**         	Designed U5C and U5D processors. Both are 486 level. */
	YepCpuVendorUMC = 10,
	/** @brief	RDC Semiconductor Co., Ltd. Vendor of x86 processor microarchitectures. */
	/** @details	Designes embedded x86 CPUs. */
	YepCpuVendorRDC = 11,
	/** @brief	DM&P Electronics Inc. Vendor of x86 processor microarchitectures. */
	/** @details	Mostly embedded x86 designs. */
	YepCpuVendorDMP = 12,
	
	/* ARM CPUs */
	
	/** @brief	ARM Holdings plc. Vendor of ARM processor microarchitectures. */
	YepCpuVendorARM       = 20,
	/** @brief	Marvell Technology Group Ltd. Vendor of ARM processor microarchitectures. */
	YepCpuVendorMarvell   = 21,
	/** @brief	Qualcomm Incorporated. Vendor of ARM processor microarchitectures. */
	YepCpuVendorQualcomm  = 22,
	/** @brief	Digital Equipment Corporation. Vendor of ARM processor microarchitecture. */
	/** @details	Sold its ARM designs in 1997. The last processor design was released in 1997. */
	YepCpuVendorDEC       = 23,
	/** @brief	Texas Instruments Inc. Vendor of ARM processor microarchitectures. */
	YepCpuVendorTI        = 24,
	/** @brief	Apple Inc. Vendor of ARM processor microarchitectures. */
	YepCpuVendorApple     = 25,
	
	/* MIPS CPUs */
	
	/** @brief	Ingenic Semiconductor. Vendor of MIPS processor microarchitectures. */
	YepCpuVendorIngenic   = 40,
	/** @brief	Institute of Computing Technology of the Chinese Academy of Sciences. Vendor of MIPS processor microarchitectures. */
	YepCpuVendorICT       = 41,
	/** @brief	MIPS Technologies, Inc. Vendor of MIPS processor microarchitectures. */
	YepCpuVendorMIPS      = 42,
	
	/* PowerPC CPUs */
	
	/** @brief	International Business Machines Corporation. Vendor of PowerPC processor microarchitectures. */
	YepCpuVendorIBM       = 50,
	/** @brief	Motorola, Inc. Vendor of PowerPC and ARM processor microarchitectures. */
	YepCpuVendorMotorola  = 51,
	/** @brief	P. A. Semi. Vendor of PowerPC processor microarchitectures. */
	/** @details	Now defunct. The last processor design was released in 2007. */
	YepCpuVendorPASemi    = 52,
	
	/* SPARC CPUs */
	
	/** @brief	Sun Microsystems, Inc. Vendor of SPARC processor microarchitectures. */
	/** @details	Now defunct. The last processor design was released in 2008. */
	YepCpuVendorSun       = 60,
	/** @brief	Oracle Corporation. Vendor of SPARC processor microarchitectures. */
	YepCpuVendorOracle    = 61,
	/** @brief	Fujitsu Limited. Vendor of SPARC processor microarchitectures. */
	YepCpuVendorFujitsu   = 62,
	/** @brief	Moscow Center of SPARC Technologies CJSC. Vendor of SPARC processor microarchitectures. */
	YepCpuVendorMCST      = 63
};

/**
 * @ingroup	yepLibrary
 * @brief	Type of processor microarchitecture.
 * @details	Low-level instruction performance characteristics, such as latency and throughput, are constant within microarchitecture.
 *         	Processors of the same microarchitecture can differ in supported instruction sets and other extensions.
 * @see	yepLibrary_GetCpuMicroarchitecture
 */
enum YepCpuMicroarchitecture {
	/** @brief Microarchitecture is unknown, or the library failed to get information about the microarchitecture from OS */
	YepCpuMicroarchitectureUnknown       = 0,
	
	/** @brief Pentium and Pentium MMX microarchitecture. */
	YepCpuMicroarchitectureP5            = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0001,
	/** @brief Pentium Pro, Pentium II, and Pentium III. */
	YepCpuMicroarchitectureP6            = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0002,
	/** @brief Pentium 4 with Willamette, Northwood, or Foster cores. */
	YepCpuMicroarchitectureWillamette    = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0003,
	/** @brief Pentium 4 with Prescott and later cores. */
	YepCpuMicroarchitecturePrescott      = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0004,
	/** @brief Pentium M. */
	YepCpuMicroarchitectureDothan        = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0005,
	/** @brief Intel Core microarchitecture. */
	YepCpuMicroarchitectureYonah         = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0006,
	/** @brief Intel Core 2 microarchitecture on 65 nm process. */
	YepCpuMicroarchitectureConroe        = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0007,
	/** @brief Intel Core 2 microarchitecture on 45 nm process. */
	YepCpuMicroarchitecturePenryn        = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0008,
	/** @brief Intel Atom on 45 nm process. */
	YepCpuMicroarchitectureBonnell       = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0009,
	/** @brief Intel Nehalem and Westmere microarchitectures (Core i3/i5/i7 1st gen). */
	YepCpuMicroarchitectureNehalem       = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x000A,
	/** @brief Intel Sandy Bridge microarchitecture (Core i3/i5/i7 2nd gen). */
	YepCpuMicroarchitectureSandyBridge   = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x000B,
	/** @brief Intel Atom on 32 nm process. */
	YepCpuMicroarchitectureSaltwell      = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x000C,
	/** @brief Intel Ivy Bridge microarchitecture (Core i3/i5/i7 3rd gen). */
	YepCpuMicroarchitectureIvyBridge     = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x000D,
	/** @brief Intel Haswell microarchitecture (Core i3/i5/i7 4th gen). */
	YepCpuMicroarchitectureHaswell       = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x000E,
	/** @brief Intel Silvermont microarchitecture (22 nm out-of-order Atom). */
	YepCpuMicroarchitectureSilvermont    = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x000F,
	
	/** @brief Intel Knights Ferry HPC boards. */
	YepCpuMicroarchitectureKnightsFerry  = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0100,
	/** @brief Intel Knights Corner HPC boards (aka Xeon Phi). */
	YepCpuMicroarchitectureKnightsCorner = (YepCpuArchitectureX86 << 24) + (YepCpuVendorIntel << 16) + 0x0101,
	
	/** @brief AMD K5. */
	YepCpuMicroarchitectureK5            = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0001,
	/** @brief AMD K6 and alike. */
	YepCpuMicroarchitectureK6            = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0002,
	/** @brief AMD Athlon and Duron. */
	YepCpuMicroarchitectureK7            = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0003,
	/** @brief AMD Geode GX and LX. */
	YepCpuMicroarchitectureGeode         = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0004,
	/** @brief AMD Athlon 64, Opteron 64. */
	YepCpuMicroarchitectureK8            = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0005,
	/** @brief AMD K10 (Barcelona, Istambul, Magny-Cours). */
	YepCpuMicroarchitectureK10           = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0006,
	/** @brief AMD Bobcat mobile microarchitecture. */
	YepCpuMicroarchitectureBobcat        = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0007,
	/** @brief AMD Bulldozer microarchitecture (1st gen K15). */
	YepCpuMicroarchitectureBulldozer     = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0008,
	/** @brief AMD Piledriver microarchitecture (2nd gen K15). */
	YepCpuMicroarchitecturePiledriver    = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x0009,
	/** @brief AMD Jaguar mobile microarchitecture. */
	YepCpuMicroarchitectureJaguar        = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x000A,
	/** @brief AMD Steamroller microarchitecture (3rd gen K15). */
	YepCpuMicroarchitectureSteamroller   = (YepCpuArchitectureX86 << 24) + (YepCpuVendorAMD   << 16) + 0x000B,
	
	/** @brief DEC/Intel StrongARM processors. */
	YepCpuMicroarchitectureStrongARM     = (YepCpuArchitectureARM << 24) + (YepCpuVendorIntel   << 16) + 0x0001,
	/** @brief Intel/Marvell XScale processors. */
	YepCpuMicroarchitectureXScale        = (YepCpuArchitectureARM << 24) + (YepCpuVendorIntel   << 16) + 0x0002,
	
	/** @brief ARM7 series. */
	YepCpuMicroarchitectureARM7          = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0001,
	/** @brief ARM9 series. */
	YepCpuMicroarchitectureARM9          = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0002,
	/** @brief ARM 1136, ARM 1156, ARM 1176, or ARM 11MPCore. */
	YepCpuMicroarchitectureARM11         = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0003,
	/** @brief ARM Cortex-A5. */
	YepCpuMicroarchitectureCortexA5      = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0004,
	/** @brief ARM Cortex-A7. */
	YepCpuMicroarchitectureCortexA7      = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0005,
	/** @brief ARM Cortex-A8. */
	YepCpuMicroarchitectureCortexA8      = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0006,
	/** @brief ARM Cortex-A9. */
	YepCpuMicroarchitectureCortexA9      = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0007,
	/** @brief ARM Cortex-A15. */
	YepCpuMicroarchitectureCortexA15     = (YepCpuArchitectureARM << 24) + (YepCpuVendorARM     << 16) + 0x0008,
	
	/** @brief Qualcomm Scorpion. */
	YepCpuMicroarchitectureScorpion      = (YepCpuArchitectureARM << 24) + (YepCpuVendorQualcomm << 16) + 0x0001,
	/** @brief Qualcomm Krait. */
	YepCpuMicroarchitectureKrait         = (YepCpuArchitectureARM << 24) + (YepCpuVendorQualcomm << 16) + 0x0002,
	
	/** @brief Marvell Sheeva PJ1. */
	YepCpuMicroarchitecturePJ1           = (YepCpuArchitectureARM << 24) + (YepCpuVendorMarvell << 16) + 0x0001,
	/** @brief Marvell Sheeva PJ4. */
	YepCpuMicroarchitecturePJ4           = (YepCpuArchitectureARM << 24) + (YepCpuVendorMarvell << 16) + 0x0002,
	
	/** @brief Apple A6 and A6X processors. */
	YepCpuMicroarchitectureSwift         = (YepCpuArchitectureARM << 24) + (YepCpuVendorApple   << 16) + 0x0001,

	/** @brief Intel Itanium. */
	YepCpuMicroarchitectureItanium       = (YepCpuArchitectureIA64 << 24) + (YepCpuVendorIntel << 16) + 0x0001,
	/** @brief Intel Itanium 2. */
	YepCpuMicroarchitectureItanium2      = (YepCpuArchitectureIA64 << 24) + (YepCpuVendorIntel << 16) + 0x0002,
	
	/** @brief MIPS 24K. */
	YepCpuMicroarchitectureMIPS24K       = (YepCpuArchitectureMIPS << 24) + (YepCpuVendorMIPS << 16) + 0x0001,
	/** @brief MIPS 34K. */
	YepCpuMicroarchitectureMIPS34K       = (YepCpuArchitectureMIPS << 24) + (YepCpuVendorMIPS << 16) + 0x0002,
	/** @brief MIPS 74K. */
	YepCpuMicroarchitectureMIPS74K       = (YepCpuArchitectureMIPS << 24) + (YepCpuVendorMIPS << 16) + 0x0003,
	
	/** @brief Ingenic XBurst. */
	YepCpuMicroarchitectureXBurst        = (YepCpuArchitectureMIPS << 24) + (YepCpuVendorIngenic << 16) + 0x0001,
	/** @brief Ingenic XBurst 2. */
	YepCpuMicroarchitectureXBurst2       = (YepCpuArchitectureMIPS << 24) + (YepCpuVendorIngenic << 16) + 0x0002
};

#ifdef __cplusplus
	const Yep64u YepIsaFeaturesDefault        = 0x0000000000000000ull;
	const Yep64u YepSimdFeaturesDefault       = 0x0000000000000000ull;
	const Yep64u YepSystemFeaturesDefault     = 0x0000000000000000ull;

	const Yep64u YepSystemFeatureCycleCounter      = 0x0000000000000001ull;
	const Yep64u YepSystemFeatureCycleCounter64Bit = 0x0000000000000002ull;
	const Yep64u YepSystemFeatureAddressSpace64Bit = 0x0000000000000004ull;
	const Yep64u YepSystemFeatureGPRegisters64Bit  = 0x0000000000000008ull;
	const Yep64u YepSystemFeatureMisalignedAccess  = 0x0000000000000010ull;
	const Yep64u YepSystemFeatureSingleThreaded    = 0x0000000000000020ull;

	/* x86/x86-64 ISA Extensions */
	const Yep64u YepX86IsaFeatureFPU          = 0x0000000000000001ull;
	const Yep64u YepX86IsaFeatureCpuid        = 0x0000000000000002ull;
	const Yep64u YepX86IsaFeatureRdtsc        = 0x0000000000000004ull;
	const Yep64u YepX86IsaFeatureCMOV         = 0x0000000000000008ull;
	const Yep64u YepX86IsaFeatureSYSENTER     = 0x0000000000000010ull;
	const Yep64u YepX86IsaFeatureSYSCALL      = 0x0000000000000020ull;
	const Yep64u YepX86IsaFeatureMSR          = 0x0000000000000040ull;
	const Yep64u YepX86IsaFeatureClflush      = 0x0000000000000080ull;
	const Yep64u YepX86IsaFeatureMONITOR      = 0x0000000000000100ull;
	const Yep64u YepX86IsaFeatureFXSAVE       = 0x0000000000000200ull;
	const Yep64u YepX86IsaFeatureXSAVE        = 0x0000000000000400ull;
	const Yep64u YepX86IsaFeatureCmpxchg8b    = 0x0000000000000800ull;
	const Yep64u YepX86IsaFeatureCmpxchg16b   = 0x0000000000001000ull;
	const Yep64u YepX86IsaFeatureX64          = 0x0000000000002000ull;
	const Yep64u YepX86IsaFeatureLahfSahf64   = 0x0000000000004000ull;
	const Yep64u YepX86IsaFeatureFsGsBase     = 0x0000000000008000ull;
	const Yep64u YepX86IsaFeatureMovbe        = 0x0000000000010000ull;
	const Yep64u YepX86IsaFeaturePopcnt       = 0x0000000000020000ull;
	const Yep64u YepX86IsaFeatureLzcnt        = 0x0000000000040000ull;
	const Yep64u YepX86IsaFeatureBMI          = 0x0000000000080000ull;
	const Yep64u YepX86IsaFeatureBMI2         = 0x0000000000100000ull;
	const Yep64u YepX86IsaFeatureTBM          = 0x0000000000200000ull;
	const Yep64u YepX86IsaFeatureRdrand       = 0x0000000000400000ull;
	const Yep64u YepX86IsaFeatureACE          = 0x0000000000800000ull;
	const Yep64u YepX86IsaFeatureACE2         = 0x0000000001000000ull;
	const Yep64u YepX86IsaFeatureRNG          = 0x0000000002000000ull;
	const Yep64u YepX86IsaFeaturePHE          = 0x0000000004000000ull;
	const Yep64u YepX86IsaFeaturePMM          = 0x0000000008000000ull;
	const Yep64u YepX86IsaFeatureAES          = 0x0000000010000000ull;
	const Yep64u YepX86IsaFeaturePclmulqdq    = 0x0000000020000000ull;
	const Yep64u YepX86IsaFeatureRdtscp       = 0x0000000040000000ull;
	const Yep64u YepX86IsaFeatureLWP          = 0x0000000080000000ull;
	const Yep64u YepX86IsaFeatureHLE          = 0x0000000100000000ull;
	const Yep64u YepX86IsaFeatureRTM          = 0x0000000200000000ull;
	const Yep64u YepX86IsaFeatureXtest        = 0x0000000400000000ull;
	const Yep64u YepX86IsaFeatureRdseed       = 0x0000000800000000ull;
	const Yep64u YepX86IsaFeatureADX          = 0x0000001000000000ull;

	const Yep64u YepX86SimdFeatureMMX                  = 0x0000000000000001ull;
	const Yep64u YepX86SimdFeatureMMXPlus              = 0x0000000000000002ull;
	const Yep64u YepX86SimdFeatureEMMX                 = 0x0000000000000004ull;
	const Yep64u YepX86SimdFeature3dnow                = 0x0000000000000008ull;
	const Yep64u YepX86SimdFeature3dnowPlus            = 0x0000000000000010ull;
	const Yep64u YepX86SimdFeature3dnowPrefetch        = 0x0000000000000020ull;
	const Yep64u YepX86SimdFeature3dnowGeode           = 0x0000000000000040ull;
	const Yep64u YepX86SimdFeatureSSE                  = 0x0000000000000080ull;
	const Yep64u YepX86SimdFeatureSSE2                 = 0x0000000000000100ull;
	const Yep64u YepX86SimdFeatureSSE3                 = 0x0000000000000200ull;
	const Yep64u YepX86SimdFeatureSSSE3                = 0x0000000000000400ull;
	const Yep64u YepX86SimdFeatureSSE4_1               = 0x0000000000000800ull;
	const Yep64u YepX86SimdFeatureSSE4_2               = 0x0000000000001000ull;
	const Yep64u YepX86SimdFeatureSSE4A                = 0x0000000000002000ull;
	const Yep64u YepX86SimdFeatureAVX                  = 0x0000000000004000ull;
	const Yep64u YepX86SimdFeatureAVX2                 = 0x0000000000008000ull;
	const Yep64u YepX86SimdFeatureXOP                  = 0x0000000000010000ull;
	const Yep64u YepX86SimdFeatureF16C                 = 0x0000000000020000ull;
	const Yep64u YepX86SimdFeatureFMA3                 = 0x0000000000040000ull;
	const Yep64u YepX86SimdFeatureFMA4                 = 0x0000000000080000ull;
	const Yep64u YepX86SimdFeatureKNF                  = 0x0000000000100000ull;
	const Yep64u YepX86SimdFeatureKNC                  = 0x0000000000200000ull;

	const Yep64u YepX86SystemFeatureFPU                = 0x0000000100000000ull;
	const Yep64u YepX86SystemFeatureSSE                = 0x0000000200000000ull;
	const Yep64u YepX86SystemFeatureAVX                = 0x0000000400000000ull;
	const Yep64u YepX86SystemFeatureMisalignedSSE      = 0x0000000800000000ull;
	const Yep64u YepX86SystemFeatureACE                = 0x0000001000000000ull;
	const Yep64u YepX86SystemFeatureACE2               = 0x0000002000000000ull;
	const Yep64u YepX86SystemFeatureRNG                = 0x0000004000000000ull;
	const Yep64u YepX86SystemFeaturePHE                = 0x0000008000000000ull;
	const Yep64u YepX86SystemFeaturePMM                = 0x0000010000000000ull;
	const Yep64u YepX86SystemFeatureMIC                = 0x0000020000000000ull;

	/* IA64 ISA Extensions */
	const Yep64u YepIA64IsaFeatureBrl                  = 0x0000000000000001ull;
	const Yep64u YepIA64IsaFeatureAtomic128            = 0x0000000000000002ull;
	const Yep64u YepIA64IsaFeatureClz                  = 0x0000000000000004ull;
	const Yep64u YepIA64IsaFeatureMpy4                 = 0x0000000000000008ull;

	/* ARM ISA Extensions */
	const Yep64u YepARMIsaFeatureV4                    = 0x0000000000000001ull;
	const Yep64u YepARMIsaFeatureV5                    = 0x0000000000000002ull;
	const Yep64u YepARMIsaFeatureV5E                   = 0x0000000000000004ull;
	const Yep64u YepARMIsaFeatureV6                    = 0x0000000000000008ull;
	const Yep64u YepARMIsaFeatureV6K                   = 0x0000000000000010ull;
	const Yep64u YepARMIsaFeatureV7                    = 0x0000000000000020ull;
	const Yep64u YepARMIsaFeatureV7MP                  = 0x0000000000000040ull;
	const Yep64u YepARMIsaFeatureThumb                 = 0x0000000000000080ull;
	const Yep64u YepARMIsaFeatureThumb2                = 0x0000000000000100ull;
	const Yep64u YepARMIsaFeatureThumbEE               = 0x0000000000000200ull;
	const Yep64u YepARMIsaFeatureJazelle               = 0x0000000000000400ull;
	const Yep64u YepARMIsaFeatureFPA                   = 0x0000000000000800ull;
	const Yep64u YepARMIsaFeatureVFP                   = 0x0000000000001000ull;
	const Yep64u YepARMIsaFeatureVFP2                  = 0x0000000000002000ull;
	const Yep64u YepARMIsaFeatureVFP3                  = 0x0000000000004000ull;
	const Yep64u YepARMIsaFeatureVFPd32                = 0x0000000000008000ull;
	const Yep64u YepARMIsaFeatureVFP3HP                = 0x0000000000010000ull;
	const Yep64u YepARMIsaFeatureVFP4                  = 0x0000000000020000ull;
	const Yep64u YepARMIsaFeatureDiv                   = 0x0000000000040000ull;
	const Yep64u YepARMIsaFeatureArmada                = 0x0000000000080000ull;

	const Yep64u YepARMSimdFeatureXScale               = 0x0000000000000001ull;
	const Yep64u YepARMSimdFeatureWMMX                 = 0x0000000000000002ull;
	const Yep64u YepARMSimdFeatureWMMX2                = 0x0000000000000004ull;
	const Yep64u YepARMSimdFeatureNEON                 = 0x0000000000000008ull;
	const Yep64u YepARMSimdFeatureNEONHP               = 0x0000000000000010ull;
	const Yep64u YepARMSimdFeatureNEON2                = 0x0000000000000020ull;

	const Yep64u YepARMSystemFeatureVFPVectorMode      = 0x0000000100000000ull;

	/* MIPS ISA Extensions */
	const Yep64u YepMIPSIsaFeatureR2            = 0x0000000000000001ull;
	const Yep64u YepMIPSIsaFeatureMicroMIPS     = 0x0000000000000002ull;
	const Yep64u YepMIPSIsaFeatureFPU           = 0x0000000000000004ull;
	const Yep64u YepMIPSIsaFeatureMT            = 0x0000000000000008ull;
	const Yep64u YepMIPSIsaFeatureMIPS16        = 0x0000000000000010ull;
	const Yep64u YepMIPSIsaFeatureSmartMIPS     = 0x0000000000000020ull;

	const Yep64u YepMIPSSimdFeatureMDMX         = 0x0000000000000001ull;
	const Yep64u YepMIPSSimdFeatureMIPS3D       = 0x0000000000000002ull;
	const Yep64u YepMIPSSimdFeaturePairedSingle = 0x0000000000000004ull;
	const Yep64u YepMIPSSimdFeatureDSP          = 0x0000000000000008ull;
	const Yep64u YepMIPSSimdFeatureDSP2         = 0x0000000000000010ull;
	const Yep64u YepMIPSSimdFeatureGodsonMMX    = 0x0000000000000020ull;
	const Yep64u YepMIPSSimdFeatureIMX          = 0x0000000000000040ull;

#else
	#define YepIsaFeaturesDefault                 0x0000000000000000ull
	#define YepSimdFeaturesDefault                0x0000000000000000ull
	#define YepSystemFeaturesDefault              0x0000000000000000ull

	/** @name	Common CPU and System Features
	 *  @see	yepLibrary_GetCpuSystemFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief The processor has a built-in cycle counter, and the operating system provides a way to access it. */
	#define YepSystemFeatureCycleCounter       0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief The processor has a 64-bit cycle counter, or the operating system provides an abstraction of a 64-bit cycle counter. */
	#define YepSystemFeatureCycleCounter64Bit  0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief The processor and the operating system allows to use 64-bit pointers. */
	#define YepSystemFeatureAddressSpace64Bit  0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief The processor and the operating system allows to do 64-bit arithmetical operations on general-purpose registers. */
	#define YepSystemFeatureGPRegisters64Bit   0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief The processor and the operating system allows misaligned memory reads and writes. */
	#define YepSystemFeatureMisalignedAccess   0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief The processor or the operating system support at most one hardware thread. */
	#define YepSystemFeatureSingleThreaded     0x0000000000000020ull
	/**@}*/


	/** @name	x86 and x86-64 ISA Extensions
	 *  @see	yepLibrary_GetCpuIsaFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief x87 FPU integrated on chip. */
	#define YepX86IsaFeatureFPU                   0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief x87 CPUID instruction. */
	#define YepX86IsaFeatureCpuid                 0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief RDTSC instruction. */
	#define YepX86IsaFeatureRdtsc                 0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief CMOV, FCMOV, and FCOMI/FUCOMI instructions. */
	#define YepX86IsaFeatureCMOV                  0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief SYSENTER and SYSEXIT instructions. */
	#define YepX86IsaFeatureSYSENTER              0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief SYSCALL and SYSRET instructions. */
	#define YepX86IsaFeatureSYSCALL               0x0000000000000020ull
	/** @ingroup yepLibrary */
	/** @brief RDMSR and WRMSR instructions. */
	#define YepX86IsaFeatureMSR                   0x0000000000000040ull
	/** @ingroup yepLibrary */
	/** @brief CLFLUSH instruction. */
	#define YepX86IsaFeatureClflush               0x0000000000000080ull
	/** @ingroup yepLibrary */
	/** @brief MONITOR and MWAIT instructions. */
	#define YepX86IsaFeatureMONITOR               0x0000000000000100ull
	/** @ingroup yepLibrary */
	/** @brief FXSAVE and FXRSTOR instructions. */
	#define YepX86IsaFeatureFXSAVE                0x0000000000000200ull
	/** @ingroup yepLibrary */
	/** @brief XSAVE, XRSTOR, XGETBV, and XSETBV instructions. */
	#define YepX86IsaFeatureXSAVE                 0x0000000000000400ull
	/** @ingroup yepLibrary */
	/** @brief CMPXCHG8B instruction. */
	#define YepX86IsaFeatureCmpxchg8b             0x0000000000000800ull
	/** @ingroup yepLibrary */
	/** @brief CMPXCHG16B instruction. */
	#define YepX86IsaFeatureCmpxchg16b            0x0000000000001000ull
	/** @ingroup yepLibrary */
	/** @brief Support for 64-bit mode. */
	#define YepX86IsaFeatureX64                   0x0000000000002000ull
	/** @ingroup yepLibrary */
	/** @brief Support for LAHF and SAHF instructions in 64-bit mode. */
	#define YepX86IsaFeatureLahfSahf64            0x0000000000004000ull
	/** @ingroup yepLibrary */
	/** @brief RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions. */
	#define YepX86IsaFeatureFsGsBase              0x0000000000008000ull
	/** @ingroup yepLibrary */
	/** @brief MOVBE instruction. */
	#define YepX86IsaFeatureMovbe                 0x0000000000010000ull
	/** @ingroup yepLibrary */
	/** @brief POPCNT instruction. */
	#define YepX86IsaFeaturePopcnt                0x0000000000020000ull
	/** @ingroup yepLibrary */
	/** @brief LZCNT instruction. */
	#define YepX86IsaFeatureLzcnt                 0x0000000000040000ull
	/** @ingroup yepLibrary */
	/** @brief BMI instruction set. */
	#define YepX86IsaFeatureBMI                   0x0000000000080000ull
	/** @ingroup yepLibrary */
	/** @brief BMI 2 instruction set. */
	#define YepX86IsaFeatureBMI2                  0x0000000000100000ull
	/** @ingroup yepLibrary */
	/** @brief TBM instruction set. */
	#define YepX86IsaFeatureTBM                   0x0000000000200000ull
	/** @ingroup yepLibrary */
	/** @brief RDRAND instruction. */
	#define YepX86IsaFeatureRdrand                0x0000000000400000ull
	/** @ingroup yepLibrary */
	/** @brief Padlock Advanced Cryptography Engine on chip. */
	#define YepX86IsaFeatureACE                   0x0000000000800000ull
	/** @ingroup yepLibrary */
	/** @brief Padlock Advanced Cryptography Engine 2 on chip. */
	#define YepX86IsaFeatureACE2                  0x0000000001000000ull
	/** @ingroup yepLibrary */
	/** @brief Padlock Random Number Generator on chip. */
	#define YepX86IsaFeatureRNG                   0x0000000002000000ull
	/** @ingroup yepLibrary */
	/** @brief Padlock Hash Engine on chip. */
	#define YepX86IsaFeaturePHE                   0x0000000004000000ull
	/** @ingroup yepLibrary */
	/** @brief Padlock Montgomery Multiplier on chip. */
	#define YepX86IsaFeaturePMM                   0x0000000008000000ull
	/** @ingroup yepLibrary */
	/** @brief AES instruction set. */
	#define YepX86IsaFeatureAES                   0x0000000010000000ull
	/** @ingroup yepLibrary */
	/** @brief PCLMULQDQ instruction. */
	#define YepX86IsaFeaturePclmulqdq             0x0000000020000000ull
	/** @ingroup yepLibrary */
	/** @brief RDTSCP instruction. */
	#define YepX86IsaFeatureRdtscp                0x0000000040000000ull
	/** @ingroup yepLibrary */
	/** @brief Lightweight Profiling extension. */
	#define YepX86IsaFeatureLWP                   0x0000000080000000ull
	/** @ingroup yepLibrary */
	/** @brief Hardware Lock Elision extension. */
	#define YepX86IsaFeatureHLE                   0x0000000100000000ull
	/** @ingroup yepLibrary */
	/** @brief Restricted Transactional Memory extension. */
	#define YepX86IsaFeatureRTM                   0x0000000200000000ull
	/** @ingroup yepLibrary */
	/** @brief XTEST instruction. */
	#define YepX86IsaFeatureXtest                 0x0000000400000000ull
	/** @ingroup yepLibrary */
	/** @brief RDSEED instruction. */
	#define YepX86IsaFeatureRdseed                0x0000000800000000ull
	/** @ingroup yepLibrary */
	/** @brief ADCX and ADOX instructions. */
	#define YepX86IsaFeatureADX                   0x0000001000000000ull
	/**@}*/

	/** @name	x86 and x86-64 SIMD Extensions
	 *  @see	yepLibrary_GetCpuSimdFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief MMX instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_MMX_EXTENSION */
	#define YepX86SimdFeatureMMX                  0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief MMX+ instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_MMXPLUS_EXTENSION */
	#define YepX86SimdFeatureMMXPlus              0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief EMMX instruction set. */
	#define YepX86SimdFeatureEMMX                 0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief 3dnow! instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_3DNOW_EXTENSION */
	#define YepX86SimdFeature3dnow                0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief 3dnow!+ instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_3DNOWPLUS_EXTENSION */
	#define YepX86SimdFeature3dnowPlus            0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief 3dnow! prefetch instructions. */
	#define YepX86SimdFeature3dnowPrefetch        0x0000000000000020ull
	/** @ingroup yepLibrary */
	/** @brief Geode 3dnow! instructions. */
	#define YepX86SimdFeature3dnowGeode           0x0000000000000040ull
	/** @ingroup yepLibrary */
	/** @brief SSE instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSE_EXTENSION */
	#define YepX86SimdFeatureSSE                  0x0000000000000080ull
	/** @ingroup yepLibrary */
	/** @brief SSE 2 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSE2_EXTENSION */
	#define YepX86SimdFeatureSSE2                 0x0000000000000100ull
	/** @ingroup yepLibrary */
	/** @brief SSE 3 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSE3_EXTENSION */
	#define YepX86SimdFeatureSSE3                 0x0000000000000200ull
	/** @ingroup yepLibrary */
	/** @brief SSSE 3 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSSE3_EXTENSION */
	#define YepX86SimdFeatureSSSE3                0x0000000000000400ull
	/** @ingroup yepLibrary */
	/** @brief SSE 4.1 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSE4_1_EXTENSION */
	#define YepX86SimdFeatureSSE4_1               0x0000000000000800ull
	/** @ingroup yepLibrary */
	/** @brief SSE 4.2 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSE4_2_EXTENSION */
	#define YepX86SimdFeatureSSE4_2               0x0000000000001000ull
	/** @ingroup yepLibrary */
	/** @brief SSE 4A instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_SSE4A_EXTENSION */
	#define YepX86SimdFeatureSSE4A                0x0000000000002000ull
	/** @ingroup yepLibrary */
	/** @brief AVX instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_AVX_EXTENSION */
	#define YepX86SimdFeatureAVX                  0x0000000000004000ull
	/** @ingroup yepLibrary */
	/** @brief AVX 2 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_AVX2_EXTENSION */
	#define YepX86SimdFeatureAVX2                 0x0000000000008000ull
	/** @ingroup yepLibrary */
	/** @brief XOP instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_XOP_EXTENSION */
	#define YepX86SimdFeatureXOP                  0x0000000000010000ull
	/** @ingroup yepLibrary */
	/** @brief F16C instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_F16C_EXTENSION */
	#define YepX86SimdFeatureF16C                 0x0000000000020000ull
	/** @ingroup yepLibrary */
	/** @brief FMA3 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_FMA3_EXTENSION */
	#define YepX86SimdFeatureFMA3                 0x0000000000040000ull
	/** @ingroup yepLibrary */
	/** @brief FMA4 instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_FMA4_EXTENSION */
	#define YepX86SimdFeatureFMA4                 0x0000000000080000ull
	/** @ingroup yepLibrary */
	/** @brief Knights Ferry (aka Larrabee) instruction set. */
	#define YepX86SimdFeatureKNF                  0x0000000000100000ull
	/** @ingroup yepLibrary */
	/** @brief Knights Corner (aka Xeon Phi) instruction set. */
	/** @see YEP_COMPILER_SUPPORTS_X86_KNC_EXTENSION */
	#define YepX86SimdFeatureKNC                  0x0000000000200000ull
	/**@}*/

	/** @name	x86 CPU and System Features
	 *  @see	yepLibrary_GetCpuSystemFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief The CPU has x87 FPU registers, and the operating systems preserves them during context switch. */
	#define YepX86SystemFeatureFPU                0x0000000100000000ull
	/** @ingroup yepLibrary */
	/** @brief The CPU has SSE registers, and the operating systems preserves them during context switch. */
	#define YepX86SystemFeatureSSE                0x0000000200000000ull
	/** @ingroup yepLibrary */
	/** @brief The CPU has AVX registers, and the operating systems preserves them during context switch. */
	#define YepX86SystemFeatureAVX                0x0000000400000000ull
	/** @ingroup yepLibrary */
	/** @brief Processor allows to use misaligned memory operands in SSE instructions other than loads and stores. */
	#define YepX86SystemFeatureMisalignedSSE      0x0000000800000000ull
	/** @ingroup yepLibrary */
	/** @brief Processor and the operating system support the Padlock Advanced Cryptography Engine. */
	#define YepX86SystemFeatureACE                0x0000001000000000ull
	/** @ingroup yepLibrary */
	/** @brief Processor and the operating system support the Padlock Advanced Cryptography Engine 2. */
	#define YepX86SystemFeatureACE2               0x0000002000000000ull
	/** @ingroup yepLibrary */
	/** @brief Processor and the operating system support the Padlock Random Number Generator. */
	#define YepX86SystemFeatureRNG                0x0000004000000000ull
	/** @ingroup yepLibrary */
	/** @brief Processor and the operating system support the Padlock Hash Engine. */
	#define YepX86SystemFeaturePHE                0x0000008000000000ull
	/** @ingroup yepLibrary */
	/** @brief Processor and the operating system support the Padlock Montgomery Multiplier. */
	#define YepX86SystemFeaturePMM                0x0000010000000000ull
	/** @ingroup yepLibrary */
	/** @brief The CPU has MIC registers, and the operating system preserves them during context switch. */
	#define YepX86SystemFeatureMIC                0x0000020000000000ull
	/**@}*/

	/** @name	IA64 ISA Extensions
	 *  @see	yepLibrary_GetCpuIsaFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief Long branch instruction. */
	#define YepIA64IsaFeatureBrl                  0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief Atomic 128-bit (16-byte) loads, stores, and CAS. */
	#define YepIA64IsaFeatureAtomic128            0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief CLZ (count leading zeros) instruction. */
	#define YepIA64IsaFeatureClz                  0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief MPY4 and MPYSHL4 (Truncated 32-bit multiplication) instructions. */
	#define YepIA64IsaFeatureMpy4                 0x0000000000000008ull
	/**@}*/

	/** @name	ARM ISA Extensions
	 *  @see	yepLibrary_GetCpuIsaFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief ARMv4 instruction set. */
	#define YepARMIsaFeatureV4                    0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief ARMv5 instruciton set. */
	#define YepARMIsaFeatureV5                    0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief ARMv5 DSP instructions. */
	#define YepARMIsaFeatureV5E                   0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief ARMv6 instruction set. */
	#define YepARMIsaFeatureV6                    0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief ARMv6 Multiprocessing extensions. */
	#define YepARMIsaFeatureV6K                   0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief ARMv7 instruction set. */
	#define YepARMIsaFeatureV7                    0x0000000000000020ull
	/** @ingroup yepLibrary */
	/** @brief ARMv7 Multiprocessing extensions. */
	#define YepARMIsaFeatureV7MP                  0x0000000000000040ull
	/** @ingroup yepLibrary */
	/** @brief Thumb mode. */
	#define YepARMIsaFeatureThumb                 0x0000000000000080ull
	/** @ingroup yepLibrary */
	/** @brief Thumb 2 mode. */
	#define YepARMIsaFeatureThumb2                0x0000000000000100ull
	/** @ingroup yepLibrary */
	/** @brief Thumb EE mode. */
	#define YepARMIsaFeatureThumbEE               0x0000000000000200ull
	/** @ingroup yepLibrary */
	/** @brief Jazelle extensions. */
	#define YepARMIsaFeatureJazelle               0x0000000000000400ull
	/** @ingroup yepLibrary */
	/** @brief FPA instructions. */
	#define YepARMIsaFeatureFPA                   0x0000000000000800ull
	/** @ingroup yepLibrary */
	/** @brief VFP instruction set. */
	#define YepARMIsaFeatureVFP                   0x0000000000001000ull
	/** @ingroup yepLibrary */
	/** @brief VFPv2 instruction set. */
	#define YepARMIsaFeatureVFP2                  0x0000000000002000ull
	/** @ingroup yepLibrary */
	/** @brief VFPv3 instruction set. */
	#define YepARMIsaFeatureVFP3                  0x0000000000004000ull
	/** @ingroup yepLibrary */
	/** @brief VFP implementation with 32 double-precision registers. */
	#define YepARMIsaFeatureVFPd32                0x0000000000008000ull
	/** @ingroup yepLibrary */
	/** @brief VFPv3 half precision extension. */
	#define YepARMIsaFeatureVFP3HP                0x0000000000010000ull
	/** @ingroup yepLibrary */
	/** @brief VFPv4 instruction set. */
	#define YepARMIsaFeatureVFP4                  0x0000000000020000ull
	/** @ingroup yepLibrary */
	/** @brief SDIV and UDIV instructions. */
	#define YepARMIsaFeatureDiv                   0x0000000000040000ull
	/** @ingroup yepLibrary */
	/** @brief Marvell Armada instruction extensions. */
	#define YepARMIsaFeatureArmada                0x0000000000080000ull
	/**@}*/

	/** @name	ARM SIMD Extensions
	 *  @see	yepLibrary_GetCpuSimdFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief XScale instructions. */
	#define YepARMSimdFeatureXScale               0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief Wireless MMX instruction set. */
	#define YepARMSimdFeatureWMMX                 0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief Wireless MMX 2 instruction set. */
	#define YepARMSimdFeatureWMMX2                0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief NEON (Advanced SIMD) instruction set. */
	#define YepARMSimdFeatureNEON                 0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief NEON (Advanced SIMD) half-precision extension. */
	#define YepARMSimdFeatureNEONHP               0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief NEON (Advanced SIMD) v2 instruction set. */
	#define YepARMSimdFeatureNEON2                0x0000000000000020ull
	/**@}*/


	/** @name	ARM CPU and System Features
	 *  @see	yepLibrary_GetCpuSystemFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief VFP vector mode is supported in hardware. */
	#define YepARMSystemFeatureVFPVectorMode      0x0000000100000000ull
	/**@}*/



	/** @name	MIPS ISA Extensions
	 *  @see	yepLibrary_GetCpuIsaFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief MIPS32/MIPS64 Release 2 architecture. */
	#define YepMIPSIsaFeatureR2                   0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief MicroMIPS extension. */
	/** @bug Not detected in this @Yeppp release. */
	#define YepMIPSIsaFeatureMicroMIPS            0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief FPU with S, D, and W formats and instructions. */
	#define YepMIPSIsaFeatureFPU                  0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief Multi-threading extension. */
	#define YepMIPSIsaFeatureMT                   0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief MIPS16 extension. */
	#define YepMIPSIsaFeatureMIPS16               0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief SmartMIPS extension. */
	#define YepMIPSIsaFeatureSmartMIPS            0x0000000000000020ull
	/**@}*/

	/** @name	MIPS SIMD Extensions
	 *  @see	yepLibrary_GetCpuSimdFeatures */
	/**@{*/
	/** @ingroup yepLibrary */
	/** @brief MDMX instruction set. */
	#define YepMIPSSimdFeatureMDMX                0x0000000000000001ull
	/** @ingroup yepLibrary */
	/** @brief MIPS3D instruction set. */
	#define YepMIPSSimdFeatureMIPS3D              0x0000000000000002ull
	/** @ingroup yepLibrary */
	/** @brief Paired-single instructions. */
	#define YepMIPSSimdFeaturePairedSingle        0x0000000000000004ull
	/** @ingroup yepLibrary */
	/** @brief MIPS DSP extension. */
	#define YepMIPSSimdFeatureDSP                 0x0000000000000008ull
	/** @ingroup yepLibrary */
	/** @brief MIPS DSP Release 2 extension. */
	#define YepMIPSSimdFeatureDSP2                0x0000000000000010ull
	/** @ingroup yepLibrary */
	/** @brief Loongson (Godson) MMX instruction set. */
	/** @bug Not detected in this @Yeppp release. */
	#define YepMIPSSimdFeatureGodsonMMX           0x0000000000000020ull
	/** @ingroup yepLibrary */
	/** @brief Ingenic Media Extension. */
	#define YepMIPSSimdFeatureIMX                 0x0000000000000040ull
	/**@}*/

#endif

#define YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(architecture) (256 + (architecture))
#define YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(architecture) (512 + (architecture))
#define YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(architecture) (768 + (architecture))

/** @ingroup	yepLibrary */
/** @brief	Indicates how to interpret integer value from one of @Yeppp enumerations. */
/** @see	yepLibrary_GetString */
enum YepEnumeration {
	/** @brief	The enumeration type is #YepStatus */
	YepEnumerationStatus = 0,
	/** @brief The enumeration type is #YepCpuArchitecture */
	YepEnumerationCpuArchitecture = 1,
	/** @brief The enumeration type is #YepCpuVendor */
	YepEnumerationCpuVendor = 2,
	/** @brief The enumeration type is #YepCpuMicroarchitecture */
	YepEnumerationCpuMicroarchitecture = 3,
	/** @brief The enumeration type is one of the processor packages for which a brief name (without vendor name) will be requested */
	YepEnumerationCpuBriefName = 4,
	/** @brief The enumeration type is one of the processor packages for which a full name (including vendor name) will be requested */
	YepEnumerationCpuFullName = 5,
	/** @brief The enumeration type is one of the common ISA features constants */
	YepEnumerationGenericIsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureUnknown),
	/** @brief The enumeration type is one of the common SIMD features constants */
	YepEnumerationGenericSimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureUnknown),
	/** @brief The enumeration type is one of the common non-ISA or system features constants */
	YepEnumerationGenericSystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureUnknown),
	/** @brief The enumeration type is one of the x86 ISA features constants */
	YepEnumerationX86IsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureX86),
	/** @brief The enumeration type is one of the x86 SIMD features constants */
	YepEnumerationX86SimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureX86),
	/** @brief The enumeration type is one of the x86 non-ISA or system features constants */
	YepEnumerationX86SystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureX86),
	/** @brief The enumeration type is one of the ARM ISA features constants */
	YepEnumerationARMIsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureARM),
	/** @brief The enumeration type is one of the ARM SIMD features constants */
	YepEnumerationARMSimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureARM),
	/** @brief The enumeration type is one of the ARM non-ISA or system features constants */
	YepEnumerationARMSystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureARM),
	/** @brief The enumeration type is one of the MIPS ISA features constants */
	YepEnumerationMIPSIsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureMIPS),
	/** @brief The enumeration type is one of the MIPS SIMD features constants */
	YepEnumerationMIPSSimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureMIPS),
	/** @brief The enumeration type is one of the MIPS non-ISA or system features constants */
	YepEnumerationMIPSSystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureMIPS),
	/** @brief The enumeration type is one of the PowerPC ISA features constants */
	YepEnumerationPowerPCIsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitecturePowerPC),
	/** @brief The enumeration type is one of the PowerPC SIMD features constants */
	YepEnumerationPowerPCSimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitecturePowerPC),
	/** @brief The enumeration type is one of the PowerPC non-ISA or system features constants */
	YepEnumerationPowerPCSystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitecturePowerPC),
	/** @brief The enumeration type is one of the IA64 ISA features constants */
	YepEnumerationIA64IsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureIA64),
	/** @brief The enumeration type is one of the IA64 SIMD features constants */
	YepEnumerationIA64SimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureIA64),
	/** @brief The enumeration type is one of the IA64 non-ISA or system features constants */
	YepEnumerationIA64SystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureIA64),
	/** @brief The enumeration type is one of the SPARC ISA features constants */
	YepEnumerationSPARCIsaFeature = YEP_ENUMERATION_ISA_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureSPARC),
	/** @brief The enumeration type is one of the SPARC SIMD features constants */
	YepEnumerationSPARCSimdFeature = YEP_ENUMERATION_SIMD_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureSPARC),
	/** @brief The enumeration type is one of the SPARC non-ISA or system features constants */
	YepEnumerationSPARCSystemFeature = YEP_ENUMERATION_SYSTEM_FEATURE_FOR_ARCHITECTURE(YepCpuArchitectureSPARC)
};

/**
 * @ingroup	yepLibrary
 * @brief	Energy counter state.
 * @see	yepLibrary_GetEnergyCounterAcquire, yepLibrary_GetEnergyCounterRelease
 */
struct YepEnergyCounter {
	Yep64u state[6];
};

/**
 * @ingroup	yepLibrary
 * @brief	Energy counter type.
 * @see	yepLibrary_GetEnergyCounterAcquire
 */
enum YepEnergyCounterType {
	/** @brief	Intel RAPL per-package energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the energy (in Joules) consumed by all chips in the CPU package. */
	YepEnergyCounterTypeRaplPackageEnergy = 1,
	/** @brief	Intel RAPL power plane 0 energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the energy (in Joules) consumed by power plane 0 (includes CPU cores and caches). */
	YepEnergyCounterTypeRaplPowerPlane0Energy = 2,
	/** @brief	Intel RAPL power plane 1 energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the energy (in Joules) consumed by power plane 1 (includes GPU cores). */
	YepEnergyCounterTypeRaplPowerPlane1Energy = 3,
	/** @brief	Intel RAPL DRAM energy counter.
	 *  @details	This counter is supported on Intel Sandy Bridge E processors, and estimates the energy (in Joules) consumed by DRAM modules.
	 *          	Motherboard support is required to use this counter. */
	YepEnergyCounterTypeRaplDRAMEnergy = 4,
	/** @brief	Intel RAPL per-package power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the average power (in Watts) consumed by all chips in the CPU package.
	 *          	This counter is implemented as a combination of RAPL per-package energy counter and system timer. */
	YepEnergyCounterTypeRaplPackagePower = 5,
	/** @brief	Intel RAPL power plane 0 power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the average power (in Watts) consumed by power plane 0 (includes CPU cores and caches).
	 *          	This counter is implemented as a combination of RAPL power plane 0 energy counter and system timer. */
	YepEnergyCounterTypeRaplPowerPlane0Power = 6,
	/** @brief	Intel RAPL power plane 1 power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge and Ivy Bridge processors, and estimates the average power (in Watts) consumed by power plane 1 (includes GPU cores).
	 *          	This counter is implemented as a combination of RAPL power plane 1 energy counter and system timer. */
	YepEnergyCounterTypeRaplPowerPlane1Power = 7,
	/** @brief	Intel RAPL DRAM power counter.
	 *  @details	This counter is supported on Intel Sandy Bridge E processors, and estimates the average power (in Watts) consumed by DRAM modules.
	 *          	This counter is implemented as a combination of RAPL DRAM energy counter and system timer.
	 *          	Motherboard support is required to use this counter. */
	YepEnergyCounterTypeRaplDRAMPower = 8
};
