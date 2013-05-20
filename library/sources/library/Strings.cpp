/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See library/LICENSE.txt for the full text of the license.
 */

#include <yepPredefines.h>
#include <yepTypes.h>
#include <yepPrivate.hpp>
#include <yepLibrary.h>
#include <library/functions.h>
#include <string.h>

template <Yep64u n> struct CTZ {
	enum {
		result = CTZ<(n >> 1)>::result + 1
	};
};

template <> struct CTZ<1ull> {
	enum {
		result = 0
	};
};

#define YEP_RETURN_CONSTANT_STRING(text) \
	return ConstantString(text, YEP_COUNT_OF(text) - 1);

static ConstantString getStatusString(YepStatus status) {
	switch (status) {
		case YepStatusOk:
			YEP_RETURN_CONSTANT_STRING("Success");
		case YepStatusNullPointer:
			YEP_RETURN_CONSTANT_STRING("Null pointer");
		case YepStatusMisalignedPointer:
			YEP_RETURN_CONSTANT_STRING("Misaligned pointer");
		case YepStatusInvalidArgument:
			YEP_RETURN_CONSTANT_STRING("Invalid argument");
		case YepStatusInvalidData:
			YEP_RETURN_CONSTANT_STRING("Invalid data");
		case YepStatusInvalidState:
			YEP_RETURN_CONSTANT_STRING("Invalid state");
		case YepStatusUnsupportedHardware:
			YEP_RETURN_CONSTANT_STRING("Unsupported hardware");
		case YepStatusUnsupportedSoftware:
			YEP_RETURN_CONSTANT_STRING("Unsupported software");
		case YepStatusInsufficientBuffer:
			YEP_RETURN_CONSTANT_STRING("Insufficient buffer");
		case YepStatusOutOfMemory:
			YEP_RETURN_CONSTANT_STRING("Not enough memory");
		case YepStatusSystemError:
			YEP_RETURN_CONSTANT_STRING("System error");
		default:
			return ConstantString();
	}
}

static ConstantString getCpuArchitectureString(YepCpuArchitecture architecture) {
	switch (architecture) {
		case YepCpuArchitectureUnknown:
			YEP_RETURN_CONSTANT_STRING("Unknown");
		case YepCpuArchitectureX86:
			YEP_RETURN_CONSTANT_STRING("x86");
		case YepCpuArchitectureARM:
			YEP_RETURN_CONSTANT_STRING("ARM");
		case YepCpuArchitectureMIPS:
			YEP_RETURN_CONSTANT_STRING("MIPS");
		case YepCpuArchitecturePowerPC:
			YEP_RETURN_CONSTANT_STRING("PowerPC");
		case YepCpuArchitectureIA64:
			YEP_RETURN_CONSTANT_STRING("IA64");
		case YepCpuArchitectureSPARC:
			YEP_RETURN_CONSTANT_STRING("SPARC");
		default:
			return ConstantString();
	}
}

ConstantString _yepLibrary_GetCpuVendorString(YepCpuVendor vendor) {
	switch (vendor) {
		case YepCpuVendorUnknown:
			YEP_RETURN_CONSTANT_STRING("Unknown");
		case YepCpuVendorIntel:
			YEP_RETURN_CONSTANT_STRING("Intel");
		case YepCpuVendorAMD:
			YEP_RETURN_CONSTANT_STRING("AMD");
		case YepCpuVendorVIA:
			YEP_RETURN_CONSTANT_STRING("VIA");
		case YepCpuVendorTransmeta:
			YEP_RETURN_CONSTANT_STRING("Transmeta");
		case YepCpuVendorCyrix:
			YEP_RETURN_CONSTANT_STRING("Cyrix");
		case YepCpuVendorRise:
			YEP_RETURN_CONSTANT_STRING("Rise");
		case YepCpuVendorNSC:
			YEP_RETURN_CONSTANT_STRING("NSC");
		case YepCpuVendorSiS:
			YEP_RETURN_CONSTANT_STRING("SiS");
		case YepCpuVendorNexGen:
			YEP_RETURN_CONSTANT_STRING("NexGen");
		case YepCpuVendorUMC:
			YEP_RETURN_CONSTANT_STRING("UMC");
		case YepCpuVendorRDC:
			YEP_RETURN_CONSTANT_STRING("RDC");
		case YepCpuVendorDMP:
			YEP_RETURN_CONSTANT_STRING("DM&P");
		case YepCpuVendorARM:
			YEP_RETURN_CONSTANT_STRING("ARM");
		case YepCpuVendorMarvell:
			YEP_RETURN_CONSTANT_STRING("Marvell");
		case YepCpuVendorQualcomm:
			YEP_RETURN_CONSTANT_STRING("Qualcomm");
		case YepCpuVendorDEC:
			YEP_RETURN_CONSTANT_STRING("DEC");
		case YepCpuVendorTI:
			YEP_RETURN_CONSTANT_STRING("TI");
		case YepCpuVendorApple:
			YEP_RETURN_CONSTANT_STRING("Apple");
		case YepCpuVendorIngenic:
			YEP_RETURN_CONSTANT_STRING("Ingenic");
		case YepCpuVendorICT:
			YEP_RETURN_CONSTANT_STRING("ICT");
		case YepCpuVendorMIPS:
			YEP_RETURN_CONSTANT_STRING("MIPS");
		case YepCpuVendorIBM:
			YEP_RETURN_CONSTANT_STRING("IBM");
		case YepCpuVendorMotorola:
			YEP_RETURN_CONSTANT_STRING("Motorola");
		case YepCpuVendorPASemi:
			YEP_RETURN_CONSTANT_STRING("P.A.Semi");
		case YepCpuVendorSun:
			YEP_RETURN_CONSTANT_STRING("Sun");
		case YepCpuVendorOracle:
			YEP_RETURN_CONSTANT_STRING("Oracle");
		case YepCpuVendorFujitsu:
			YEP_RETURN_CONSTANT_STRING("Fujitsu");
		case YepCpuVendorMCST:
			YEP_RETURN_CONSTANT_STRING("MCST");
		default:
			return ConstantString();
	}
}

ConstantString _yepLibrary_GetCpuMicroarchitectureString(YepCpuMicroarchitecture microarchitecture) {
	switch (microarchitecture) {
		case YepCpuMicroarchitectureUnknown:
			YEP_RETURN_CONSTANT_STRING("Unknown");
		case YepCpuMicroarchitectureP5:
			YEP_RETURN_CONSTANT_STRING("P5");
		case YepCpuMicroarchitectureP6:
			YEP_RETURN_CONSTANT_STRING("P6");
		case YepCpuMicroarchitectureWillamette:
			YEP_RETURN_CONSTANT_STRING("Willamette");
		case YepCpuMicroarchitecturePrescott:
			YEP_RETURN_CONSTANT_STRING("Prescott");
		case YepCpuMicroarchitectureDothan:
			YEP_RETURN_CONSTANT_STRING("Dothan");
		case YepCpuMicroarchitectureYonah:
			YEP_RETURN_CONSTANT_STRING("Yonah");
		case YepCpuMicroarchitectureConroe:
			YEP_RETURN_CONSTANT_STRING("Conroe");
		case YepCpuMicroarchitecturePenryn:
			YEP_RETURN_CONSTANT_STRING("Penryn");
		case YepCpuMicroarchitectureBonnell:
			YEP_RETURN_CONSTANT_STRING("Bonnell");
		case YepCpuMicroarchitectureNehalem:
			YEP_RETURN_CONSTANT_STRING("Nehalem");
		case YepCpuMicroarchitectureSandyBridge:
			YEP_RETURN_CONSTANT_STRING("Sandy Bridge");
		case YepCpuMicroarchitectureSaltwell:
			YEP_RETURN_CONSTANT_STRING("Saltwell");
		case YepCpuMicroarchitectureIvyBridge:
			YEP_RETURN_CONSTANT_STRING("Ivy Bridge");
		case YepCpuMicroarchitectureHaswell:
			YEP_RETURN_CONSTANT_STRING("Haswell");
		case YepCpuMicroarchitectureSilvermont:
			YEP_RETURN_CONSTANT_STRING("Silvermont");
		case YepCpuMicroarchitectureKnightsFerry:
			YEP_RETURN_CONSTANT_STRING("Knights Ferry");
		case YepCpuMicroarchitectureKnightsCorner:
			YEP_RETURN_CONSTANT_STRING("Knights Corner");
		case YepCpuMicroarchitectureK5:
			YEP_RETURN_CONSTANT_STRING("K5");
		case YepCpuMicroarchitectureK6:
			YEP_RETURN_CONSTANT_STRING("K6");
		case YepCpuMicroarchitectureK7:
			YEP_RETURN_CONSTANT_STRING("K7");
		case YepCpuMicroarchitectureGeode:
			YEP_RETURN_CONSTANT_STRING("Geode");
		case YepCpuMicroarchitectureK8:
			YEP_RETURN_CONSTANT_STRING("K8");
		case YepCpuMicroarchitectureK10:
			YEP_RETURN_CONSTANT_STRING("K10");
		case YepCpuMicroarchitectureBobcat:
			YEP_RETURN_CONSTANT_STRING("Bobcat");
		case YepCpuMicroarchitectureBulldozer:
			YEP_RETURN_CONSTANT_STRING("Bulldozer");
		case YepCpuMicroarchitecturePiledriver:
			YEP_RETURN_CONSTANT_STRING("Piledriver");
		case YepCpuMicroarchitectureJaguar:
			YEP_RETURN_CONSTANT_STRING("Jaguar");
		case YepCpuMicroarchitectureSteamroller:
			YEP_RETURN_CONSTANT_STRING("Steamroller");
		case YepCpuMicroarchitectureStrongARM:
			YEP_RETURN_CONSTANT_STRING("StrongARM");
		case YepCpuMicroarchitectureXScale:
			YEP_RETURN_CONSTANT_STRING("XScale");
		case YepCpuMicroarchitectureARM7:
			YEP_RETURN_CONSTANT_STRING("ARM7");
		case YepCpuMicroarchitectureARM9:
			YEP_RETURN_CONSTANT_STRING("ARM9");
		case YepCpuMicroarchitectureARM11:
			YEP_RETURN_CONSTANT_STRING("ARM11");
		case YepCpuMicroarchitectureCortexA5:
			YEP_RETURN_CONSTANT_STRING("Cortex-A5");
		case YepCpuMicroarchitectureCortexA7:
			YEP_RETURN_CONSTANT_STRING("Cortex-A7");
		case YepCpuMicroarchitectureCortexA8:
			YEP_RETURN_CONSTANT_STRING("Cortex-A8");
		case YepCpuMicroarchitectureCortexA9:
			YEP_RETURN_CONSTANT_STRING("Cortex-A9");
		case YepCpuMicroarchitectureCortexA15:
			YEP_RETURN_CONSTANT_STRING("Cortex-A15");
		case YepCpuMicroarchitectureScorpion:
			YEP_RETURN_CONSTANT_STRING("Scorpion");
		case YepCpuMicroarchitectureKrait:
			YEP_RETURN_CONSTANT_STRING("Krait");
		case YepCpuMicroarchitecturePJ1:
			YEP_RETURN_CONSTANT_STRING("PJ1");
		case YepCpuMicroarchitecturePJ4:
			YEP_RETURN_CONSTANT_STRING("PJ4");
		case YepCpuMicroarchitectureSwift:
			YEP_RETURN_CONSTANT_STRING("Swift");
		case YepCpuMicroarchitectureItanium:
			YEP_RETURN_CONSTANT_STRING("Itanium");
		case YepCpuMicroarchitectureItanium2:
			YEP_RETURN_CONSTANT_STRING("Itanium 2");
		case YepCpuMicroarchitectureMIPS24K:
			YEP_RETURN_CONSTANT_STRING("MIPS 24K");
		case YepCpuMicroarchitectureMIPS34K:
			YEP_RETURN_CONSTANT_STRING("MIPS 34K");
		case YepCpuMicroarchitectureMIPS74K:
			YEP_RETURN_CONSTANT_STRING("MIPS 74K");
		case YepCpuMicroarchitectureXBurst:
			YEP_RETURN_CONSTANT_STRING("XBurst");
		case YepCpuMicroarchitectureXBurst2:
			YEP_RETURN_CONSTANT_STRING("XBurst 2");
		default:
			return ConstantString();
	}
}

static ConstantString getGenericIsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		default:
			return ConstantString();
	}
};

static ConstantString getGenericSimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		default:
			return ConstantString();
	}
};

static ConstantString getGenericSystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		case CTZ<YepSystemFeatureCycleCounter>::result:
			YEP_RETURN_CONSTANT_STRING("CPU cycle counter");
		case CTZ<YepSystemFeatureCycleCounter64Bit>::result:
			YEP_RETURN_CONSTANT_STRING("64-bit CPU cycle counter");
		case CTZ<YepSystemFeatureAddressSpace64Bit>::result:
			YEP_RETURN_CONSTANT_STRING("64-bit address space");
		case CTZ<YepSystemFeatureGPRegisters64Bit>::result:
			YEP_RETURN_CONSTANT_STRING("64-bit general-purpose registers");
		case CTZ<YepSystemFeatureMisalignedAccess>::result:
			YEP_RETURN_CONSTANT_STRING("Misaligned memory access");
		case CTZ<YepSystemFeatureSingleThreaded>::result:
			YEP_RETURN_CONSTANT_STRING("Single hardware thread");
		default:
			return ConstantString();
	}
};

static ConstantString getX86IsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		case CTZ<YepX86IsaFeatureFPU>::result:
			YEP_RETURN_CONSTANT_STRING("x87 FPU");
		case CTZ<YepX86IsaFeatureCpuid>::result:
			YEP_RETURN_CONSTANT_STRING("CPUID instruction");
		case CTZ<YepX86IsaFeatureRdtsc>::result:
			YEP_RETURN_CONSTANT_STRING("RDTSC instruction");
		case CTZ<YepX86IsaFeatureCMOV>::result:
			YEP_RETURN_CONSTANT_STRING("CMOV instruction");
		case CTZ<YepX86IsaFeatureSYSENTER>::result:
			YEP_RETURN_CONSTANT_STRING("SYSENTER and SYSEXIT instructions");
		case CTZ<YepX86IsaFeatureSYSCALL>::result:
			YEP_RETURN_CONSTANT_STRING("SYSCALL and SYSRET instructions");
		case CTZ<YepX86IsaFeatureMSR>::result:
			YEP_RETURN_CONSTANT_STRING("RDMSR and WRMSR instructions");
		case CTZ<YepX86IsaFeatureClflush>::result:
			YEP_RETURN_CONSTANT_STRING("CLFLUSH instruction");
		case CTZ<YepX86IsaFeatureMONITOR>::result:
			YEP_RETURN_CONSTANT_STRING("MONITOR and MWAIT instructions");
		case CTZ<YepX86IsaFeatureFXSAVE>::result:
			YEP_RETURN_CONSTANT_STRING("FXSAVE and FXRSTOR instructions");
		case CTZ<YepX86IsaFeatureXSAVE>::result:
			YEP_RETURN_CONSTANT_STRING("XSAVE, XRSTOR, XGETBV, and XSETBV instructions");
		case CTZ<YepX86IsaFeatureCmpxchg8b>::result:
			YEP_RETURN_CONSTANT_STRING("CMPXCHG8B instruction");
		case CTZ<YepX86IsaFeatureCmpxchg16b>::result:
			YEP_RETURN_CONSTANT_STRING("CMPXCHG16B instruction");
		case CTZ<YepX86IsaFeatureX64>::result:
			YEP_RETURN_CONSTANT_STRING("x86-64 mode");
		case CTZ<YepX86IsaFeatureLahfSahf64>::result:
			YEP_RETURN_CONSTANT_STRING("LAHF and SAHF instructions in x86-64 mode");
		case CTZ<YepX86IsaFeatureFsGsBase>::result:
			YEP_RETURN_CONSTANT_STRING("RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions");
		case CTZ<YepX86IsaFeatureMovbe>::result:
			YEP_RETURN_CONSTANT_STRING("MOVBE instruction");
		case CTZ<YepX86IsaFeaturePopcnt>::result:
			YEP_RETURN_CONSTANT_STRING("POPCNT instruction");
		case CTZ<YepX86IsaFeatureLzcnt>::result:
			YEP_RETURN_CONSTANT_STRING("LZCNT instruction");
		case CTZ<YepX86IsaFeatureBMI>::result:
			YEP_RETURN_CONSTANT_STRING("BMI instruction set");
		case CTZ<YepX86IsaFeatureBMI2>::result:
			YEP_RETURN_CONSTANT_STRING("BMI 2 instruction set");
		case CTZ<YepX86IsaFeatureTBM>::result:
			YEP_RETURN_CONSTANT_STRING("TBM instruction set");
		case CTZ<YepX86IsaFeatureRdrand>::result:
			YEP_RETURN_CONSTANT_STRING("RDRAND instruction");
		case CTZ<YepX86IsaFeatureACE>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Advanced Cryptography Engine");
		case CTZ<YepX86IsaFeatureACE2>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Advanced Cryptography Engine 2");
		case CTZ<YepX86IsaFeatureRNG>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Random Number Generator");
		case CTZ<YepX86IsaFeaturePHE>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Hash Engine");
		case CTZ<YepX86IsaFeaturePMM>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Montgomery Multiplier");
		case CTZ<YepX86IsaFeatureAES>::result:
			YEP_RETURN_CONSTANT_STRING("AES instruction set");
		case CTZ<YepX86IsaFeaturePclmulqdq>::result:
			YEP_RETURN_CONSTANT_STRING("PCLMULQDQ instruction");
		case CTZ<YepX86IsaFeatureRdtscp>::result:
			YEP_RETURN_CONSTANT_STRING("RDTSCP instruction");
		case CTZ<YepX86IsaFeatureLWP>::result:
			YEP_RETURN_CONSTANT_STRING("Lightweight Profiling extension");
		case CTZ<YepX86IsaFeatureHLE>::result:
			YEP_RETURN_CONSTANT_STRING("Hardware Lock Elision extension");
		case CTZ<YepX86IsaFeatureRTM>::result:
			YEP_RETURN_CONSTANT_STRING("Restricted Transactional Memory extension");
		case CTZ<YepX86IsaFeatureXtest>::result:
			YEP_RETURN_CONSTANT_STRING("XTEST instruction");
		case CTZ<YepX86IsaFeatureRdseed>::result:
			YEP_RETURN_CONSTANT_STRING("RDSEED instruction");
		case CTZ<YepX86IsaFeatureADX>::result:
			YEP_RETURN_CONSTANT_STRING("ADCX and ADOX instructions");
		default:
			return getGenericIsaFeatureString(ctzIsaFeature);
	}
};

static ConstantString getX86SimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		case CTZ<YepX86SimdFeatureMMX>::result:
			YEP_RETURN_CONSTANT_STRING("MMX instruction set");
		case CTZ<YepX86SimdFeatureMMXPlus>::result:
			YEP_RETURN_CONSTANT_STRING("MMX+ instruction set");
		case CTZ<YepX86SimdFeatureEMMX>::result:
			YEP_RETURN_CONSTANT_STRING("EMMX instruction set");
		case CTZ<YepX86SimdFeature3dnow>::result:
			YEP_RETURN_CONSTANT_STRING("3dnow! instruction set");
		case CTZ<YepX86SimdFeature3dnowPlus>::result:
			YEP_RETURN_CONSTANT_STRING("3dnow!+ instruction set");
		case CTZ<YepX86SimdFeature3dnowPrefetch>::result:
			YEP_RETURN_CONSTANT_STRING("3dnow! prefetch instructions");
		case CTZ<YepX86SimdFeature3dnowGeode>::result:
			YEP_RETURN_CONSTANT_STRING("Geode 3dnow! instructions");
		case CTZ<YepX86SimdFeatureSSE>::result:
			YEP_RETURN_CONSTANT_STRING("SSE instruction set");
		case CTZ<YepX86SimdFeatureSSE2>::result:
			YEP_RETURN_CONSTANT_STRING("SSE 2 instruction set");
		case CTZ<YepX86SimdFeatureSSE3>::result:
			YEP_RETURN_CONSTANT_STRING("SSE 3 instruction set");
		case CTZ<YepX86SimdFeatureSSSE3>::result:
			YEP_RETURN_CONSTANT_STRING("Supplemental SSE 3 instruction set");
		case CTZ<YepX86SimdFeatureSSE4_1>::result:
			YEP_RETURN_CONSTANT_STRING("SSE 4.1 instruction set");
		case CTZ<YepX86SimdFeatureSSE4_2>::result:
			YEP_RETURN_CONSTANT_STRING("SSE 4.2 instruction set");
		case CTZ<YepX86SimdFeatureSSE4A>::result:
			YEP_RETURN_CONSTANT_STRING("SSE 4A instruction set");
		case CTZ<YepX86SimdFeatureAVX>::result:
			YEP_RETURN_CONSTANT_STRING("AVX instruction set");
		case CTZ<YepX86SimdFeatureAVX2>::result:
			YEP_RETURN_CONSTANT_STRING("AVX 2 instruction set");
		case CTZ<YepX86SimdFeatureXOP>::result:
			YEP_RETURN_CONSTANT_STRING("XOP instruction set");
		case CTZ<YepX86SimdFeatureF16C>::result:
			YEP_RETURN_CONSTANT_STRING("F16C instruction set");
		case CTZ<YepX86SimdFeatureFMA3>::result:
			YEP_RETURN_CONSTANT_STRING("FMA3 instruction set");
		case CTZ<YepX86SimdFeatureFMA4>::result:
			YEP_RETURN_CONSTANT_STRING("FMA4 instruction set");
		case CTZ<YepX86SimdFeatureKNF>::result:
			YEP_RETURN_CONSTANT_STRING("KNF instruction set");
		case CTZ<YepX86SimdFeatureKNC>::result:
			YEP_RETURN_CONSTANT_STRING("KNC instruction set");
		default:
			return getGenericSimdFeatureString(ctzSimdFeature);
	}
};

static ConstantString getX86SystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		case CTZ<YepX86SystemFeatureFPU>::result:
			YEP_RETURN_CONSTANT_STRING("x87 FPU registers");
		case CTZ<YepX86SystemFeatureSSE>::result:
			YEP_RETURN_CONSTANT_STRING("SSE registers");
		case CTZ<YepX86SystemFeatureAVX>::result:
			YEP_RETURN_CONSTANT_STRING("AVX registers");
		case CTZ<YepX86SystemFeatureMisalignedSSE>::result:
			YEP_RETURN_CONSTANT_STRING("Misaligned memory operands in SSE instructions");
		case CTZ<YepX86SystemFeatureACE>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Advanced Cryptography Engine");
		case CTZ<YepX86SystemFeatureACE2>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Advanced Cryptography Engine 2");
		case CTZ<YepX86SystemFeatureRNG>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Random Number Generator");
		case CTZ<YepX86SystemFeaturePHE>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Hash Engine");
		case CTZ<YepX86SystemFeaturePMM>::result:
			YEP_RETURN_CONSTANT_STRING("Padlock Montgomery Multiplier");
		case CTZ<YepX86SystemFeatureMIC>::result:
			YEP_RETURN_CONSTANT_STRING("MIC registers");
		default:
			return getGenericSystemFeatureString(ctzSystemFeature);
	}
};

static ConstantString getARMIsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		case CTZ<YepARMIsaFeatureV4>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv4 instruction set");
		case CTZ<YepARMIsaFeatureV5>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv5 instruction set");
		case CTZ<YepARMIsaFeatureV5E>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv5 DSP instructions");
		case CTZ<YepARMIsaFeatureV6>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv6 instruction set");
		case CTZ<YepARMIsaFeatureV6K>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv6 Multiprocessing extensions");
		case CTZ<YepARMIsaFeatureV7>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv7 instruction set");
		case CTZ<YepARMIsaFeatureV7MP>::result:
			YEP_RETURN_CONSTANT_STRING("ARMv7 Multiprocessing extensions");
		case CTZ<YepARMIsaFeatureThumb>::result:
			YEP_RETURN_CONSTANT_STRING("Thumb mode");
		case CTZ<YepARMIsaFeatureThumb2>::result:
			YEP_RETURN_CONSTANT_STRING("Thumb-2 mode");
		case CTZ<YepARMIsaFeatureThumbEE>::result:
			YEP_RETURN_CONSTANT_STRING("Thumb EE mode");
		case CTZ<YepARMIsaFeatureJazelle>::result:
			YEP_RETURN_CONSTANT_STRING("Jazelle extension");
		case CTZ<YepARMIsaFeatureFPA>::result:
			YEP_RETURN_CONSTANT_STRING("FPA instruction set");
		case CTZ<YepARMIsaFeatureVFP>::result:
			YEP_RETURN_CONSTANT_STRING("VFP instruction set");
		case CTZ<YepARMIsaFeatureVFP2>::result:
			YEP_RETURN_CONSTANT_STRING("VFPv2 instruction set");
		case CTZ<YepARMIsaFeatureVFP3>::result:
			YEP_RETURN_CONSTANT_STRING("VFPv3 instruction set");
		case CTZ<YepARMIsaFeatureVFPd32>::result:
			YEP_RETURN_CONSTANT_STRING("VFP with 32 DP registers");
		case CTZ<YepARMIsaFeatureVFP3HP>::result:
			YEP_RETURN_CONSTANT_STRING("VFPv3 half-precision extension");
		case CTZ<YepARMIsaFeatureVFP4>::result:
			YEP_RETURN_CONSTANT_STRING("VFPv4 instruction set");
		case CTZ<YepARMIsaFeatureDiv>::result:
			YEP_RETURN_CONSTANT_STRING("SDIV and UDIV instructions");
		case CTZ<YepARMIsaFeatureArmada>::result:
			YEP_RETURN_CONSTANT_STRING("Marvell Armada instruction extensions");
		default:
			return getGenericIsaFeatureString(ctzIsaFeature);
	}
};

static ConstantString getARMSimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		case CTZ<YepARMSimdFeatureXScale>::result:
			YEP_RETURN_CONSTANT_STRING("XScale instructions");
		case CTZ<YepARMSimdFeatureWMMX>::result:
			YEP_RETURN_CONSTANT_STRING("Wireless MMX instruction set");
		case CTZ<YepARMSimdFeatureWMMX2>::result:
			YEP_RETURN_CONSTANT_STRING("Wireless MMX 2 instruction set");
		case CTZ<YepARMSimdFeatureNEON>::result:
			YEP_RETURN_CONSTANT_STRING("NEON (Advanced SIMD) instruction set");
		case CTZ<YepARMSimdFeatureNEONHP>::result:
			YEP_RETURN_CONSTANT_STRING("NEON (Advanced SIMD) half-precision extension");
		case CTZ<YepARMSimdFeatureNEON2>::result:
			YEP_RETURN_CONSTANT_STRING("NEON (Advanced SIMD) v2 instruction set");
		default:
			return getGenericSimdFeatureString(ctzSimdFeature);
	}
};

static ConstantString getARMSystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		case CTZ<YepARMSystemFeatureVFPVectorMode>::result:
			YEP_RETURN_CONSTANT_STRING("Hardware VFP vector mode");
		default:
			return getGenericSystemFeatureString(ctzSystemFeature);
	}
};

static ConstantString getMIPSIsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		case CTZ<YepMIPSIsaFeatureR2>::result:
			YEP_RETURN_CONSTANT_STRING("MIPS32/MIPS64 Release 2 architecture");
		case CTZ<YepMIPSIsaFeatureMicroMIPS>::result:
			YEP_RETURN_CONSTANT_STRING("MicroMIPS extension");
		case CTZ<YepMIPSIsaFeatureFPU>::result:
			YEP_RETURN_CONSTANT_STRING("FPU with S, D, and W formats");
		case CTZ<YepMIPSIsaFeatureMT>::result:
			YEP_RETURN_CONSTANT_STRING("Multi-threading extension");
		case CTZ<YepMIPSIsaFeatureMIPS16>::result:
			YEP_RETURN_CONSTANT_STRING("MIPS16 extension");
		case CTZ<YepMIPSIsaFeatureSmartMIPS>::result:
			YEP_RETURN_CONSTANT_STRING("SmartMIPS extension");
		default:
			return getGenericIsaFeatureString(ctzIsaFeature);
	}
};

static ConstantString getMIPSSimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		case CTZ<YepMIPSSimdFeatureMDMX>::result:
			YEP_RETURN_CONSTANT_STRING("MDMX instruction set");
		case CTZ<YepMIPSSimdFeatureMIPS3D>::result:
			YEP_RETURN_CONSTANT_STRING("MIPS3D instruction set");
		case CTZ<YepMIPSSimdFeaturePairedSingle>::result:
			YEP_RETURN_CONSTANT_STRING("Paired-single instructions");
		case CTZ<YepMIPSSimdFeatureDSP>::result:
			YEP_RETURN_CONSTANT_STRING("MIPS DSP extension");
		case CTZ<YepMIPSSimdFeatureDSP2>::result:
			YEP_RETURN_CONSTANT_STRING("MIPS DSP Release 2 extension");
		case CTZ<YepMIPSSimdFeatureGodsonMMX>::result:
			YEP_RETURN_CONSTANT_STRING("Loongson (Godson) MMX instruction set");
		case CTZ<YepMIPSSimdFeatureIMX>::result:
			YEP_RETURN_CONSTANT_STRING("Ingenic Media Extension");
		default:
			return getGenericSimdFeatureString(ctzSimdFeature);
	}
};

static ConstantString getMIPSSystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		default:
			return getGenericSystemFeatureString(ctzSystemFeature);
	}
};

static ConstantString getPowerPCIsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		default:
			return getGenericIsaFeatureString(ctzIsaFeature);
	}
};

static ConstantString getPowerPCSimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		default:
			return getGenericSimdFeatureString(ctzSimdFeature);
	}
};

static ConstantString getPowerPCSystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		default:
			return getGenericSystemFeatureString(ctzSystemFeature);
	}
};

static ConstantString getIA64IsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		default:
			return getGenericIsaFeatureString(ctzIsaFeature);
	}
};

static ConstantString getIA64SimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		default:
			return getGenericSimdFeatureString(ctzSimdFeature);
	}
};

static ConstantString getIA64SystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		default:
			return getGenericSystemFeatureString(ctzSystemFeature);
	}
};

static ConstantString getSPARCIsaFeatureString(Yep32u ctzIsaFeature) {
	switch (ctzIsaFeature) {
		default:
			return getGenericIsaFeatureString(ctzIsaFeature);
	}
};

static ConstantString getSPARCSimdFeatureString(Yep32u ctzSimdFeature) {
	switch (ctzSimdFeature) {
		default:
			return getGenericSimdFeatureString(ctzSimdFeature);
	}
};

static ConstantString getSPARCSystemFeatureString(Yep32u ctzSystemFeature) {
	switch (ctzSystemFeature) {
		default:
			return getGenericSystemFeatureString(ctzSystemFeature);
	}
};

YepStatus yepLibrary_GetString(YepEnumeration enumerationType, Yep32u enumerationValue, void *buffer, YepSize *lengthPointer) {
	if YEP_UNLIKELY(buffer == YEP_NULL_POINTER) {
		return YepStatusNullPointer;
	}
	if YEP_UNLIKELY(lengthPointer == YEP_NULL_POINTER) {
		return YepStatusNullPointer;
	}
	const YepSize length = *lengthPointer;
	ConstantString constantString;
	switch (enumerationType) {
		case YepEnumerationStatus:
			constantString = getStatusString(static_cast<YepStatus>(enumerationValue)); break;
		case YepEnumerationCpuArchitecture:
			constantString = getCpuArchitectureString(static_cast<YepCpuArchitecture>(enumerationValue)); break;
		case YepEnumerationCpuVendor:
			constantString = _yepLibrary_GetCpuVendorString(static_cast<YepCpuVendor>(enumerationValue)); break;
		case YepEnumerationCpuMicroarchitecture:
			constantString = _yepLibrary_GetCpuMicroarchitectureString(static_cast<YepCpuMicroarchitecture>(enumerationValue)); break;
		case YepEnumerationCpuBriefName:
			constantString = _briefCpuName; break;
		case YepEnumerationCpuFullName:
			constantString = _fullCpuName; break;
		case YepEnumerationGenericIsaFeature:
			constantString = getGenericIsaFeatureString(enumerationValue); break;
		case YepEnumerationGenericSimdFeature:
			constantString = getGenericSimdFeatureString(enumerationValue); break;
		case YepEnumerationGenericSystemFeature:
			constantString = getGenericSystemFeatureString(enumerationValue); break;
		case YepEnumerationX86IsaFeature:
			constantString = getX86IsaFeatureString(enumerationValue); break;
		case YepEnumerationX86SimdFeature:
			constantString = getX86SimdFeatureString(enumerationValue); break;
		case YepEnumerationX86SystemFeature:
			constantString = getX86SystemFeatureString(enumerationValue); break;
		case YepEnumerationARMIsaFeature:
			constantString = getARMIsaFeatureString(enumerationValue); break;
		case YepEnumerationARMSimdFeature:
			constantString = getARMSimdFeatureString(enumerationValue); break;
		case YepEnumerationARMSystemFeature:
			constantString = getARMSystemFeatureString(enumerationValue); break;
		case YepEnumerationMIPSIsaFeature:
			constantString = getMIPSIsaFeatureString(enumerationValue); break;
		case YepEnumerationMIPSSimdFeature:
			constantString = getMIPSSimdFeatureString(enumerationValue); break;
		case YepEnumerationMIPSSystemFeature:
			constantString = getMIPSSystemFeatureString(enumerationValue); break;
		case YepEnumerationPowerPCIsaFeature:
			constantString = getPowerPCIsaFeatureString(enumerationValue); break;
		case YepEnumerationPowerPCSimdFeature:
			constantString = getPowerPCSimdFeatureString(enumerationValue); break;
		case YepEnumerationPowerPCSystemFeature:
			constantString = getPowerPCSystemFeatureString(enumerationValue); break;
		case YepEnumerationIA64IsaFeature:
			constantString = getIA64IsaFeatureString(enumerationValue); break;
		case YepEnumerationIA64SimdFeature:
			constantString = getIA64SimdFeatureString(enumerationValue); break;
		case YepEnumerationIA64SystemFeature:
			constantString = getIA64SystemFeatureString(enumerationValue); break;
		case YepEnumerationSPARCIsaFeature:
			constantString = getSPARCIsaFeatureString(enumerationValue); break;
		case YepEnumerationSPARCSimdFeature:
			constantString = getSPARCSimdFeatureString(enumerationValue); break;
		case YepEnumerationSPARCSystemFeature:
			constantString = getSPARCSystemFeatureString(enumerationValue); break;
	}
	if YEP_UNLIKELY(constantString.isEmpty()) {
		return YepStatusInvalidArgument;
	}
	if YEP_UNLIKELY(constantString.length > length) {
		*lengthPointer = constantString.length;
		return YepStatusInsufficientBuffer;
	} else {
		memcpy(buffer, static_cast<const void*>(constantString.pointer), constantString.length);
		*lengthPointer = constantString.length;
		return YepStatusOk;
	}
}
