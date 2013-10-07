/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

#if defined(_FORTIFY_SOURCE)
	#undef _FORTIFY_SOURCE
#endif

#include <yepPredefines.h>
#include <yepTypes.h>
#include <yepPrivate.h>
#include <yepLibrary.h>
#include <library/functions.h>
#include <yepBuiltin.h>
#include <string.h>

#if defined(YEP_LINUX_OS)
	#define AT_HWCAP  16
	#define AT_HWCAP2 26

	#define PPC_FEATURE_32             0x80000000
	#define PPC_FEATURE_64             0x40000000
	#define PPC_FEATURE_HAS_ALTIVEC    0x10000000
	#define PPC_FEATURE_HAS_FPU        0x08000000
	#define PPC_FEATURE_HAS_4xxMAC     0x02000000
	#define PPC_FEATURE_HAS_SPE        0x00800000
	#define PPC_FEATURE_HAS_EFP_SINGLE 0x00400000
	#define PPC_FEATURE_HAS_EFP_DOUBLE 0x00200000
	#define PPC_FEATURE_POWER4         0x00080000
	#define PPC_FEATURE_POWER5         0x00040000
	#define PPC_FEATURE_POWER5_PLUS    0x00020000
	#define PPC_FEATURE_BOOKE          0x00008000
	#define PPC_FEATURE_ARCH_2_05      0x00001000
	#define PPC_FEATURE_HAS_DFP        0x00000400
	#define PPC_FEATURE_POWER6_EXT     0x00000200
	#define PPC_FEATURE_ARCH_2_06      0x00000100
	#define PPC_FEATURE_HAS_VSX        0x00000080

	#define PPC_FEATURE2_ARCH_2_07     0x80000000
	#define PPC_FEATURE2_HTM           0x40000000
	#define PPC_FEATURE2_ISEL          0x08000000
	#define PPC_FEATURE2_TAR           0x04000000
#else
	#error "This OS is not supported yet"
#endif

#if defined(YEP_POWERPC_CPU)
	#if defined(YEP_BLUEGENE_SYSTEM)
		static void initBlueGene(Yep32u& logicalCoresCount, YepCpuVendor& vendor, YepCpuMicroarchitecture& microarchitecture, Yep64u& isaFeatures, Yep64u& simdFeatures, Yep64u& systemFeatures) {
			#if defined(YEP_BLUEGENE_Q_SYSTEM)
				/* 16 cores, 4-way SMT */
				logicalCoresCount = 16 * 4;

				vendor = YepCpuVendorIBM;
				microarchitecture = YepCpuMicroarchitecturePowerPCA2;

				simdFeatures |= YepPowerPCSimdFeatureQPX;

				systemFeatures |= YepSystemFeatureCycleCounter;
				systemFeatures |= YepSystemFeatureCycleCounter64Bit;
				systemFeatures |= YepSystemFeatureAddressSpace64Bit;
				systemFeatures |= YepSystemFeatureGPRegisters64Bit;
			#elif defined(YEP_BLUEGENE_P_SYSTEM)
				/* 4 cores, no SMT */
				logicalCoresCount = 4;

				vendor = YepCpuVendorIBM;
				microarchitecture = YepCpuMicroarchitecturePowerPC450;

				simdFeatures |= YepPowerPCSimdFeatureDoubleHummer;

				systemFeatures |= YepSystemFeatureCycleCounter;
				systemFeatures |= YepSystemFeatureCycleCounter64Bit;
			#else
				#error "This BlueGene system is not supported yet"
			#endif
		}
	#else
		static void initProcessorVersion(Yep32u& _processorVersion) {
			_processorVersion = yepBuiltin_PPC_ReadProcessorVersionRegister_32u();
		}

		static void initProcessorMicroarchitecture(Yep32u processorVersion, YepCpuVendor& vendor, YepCpuMicroarchitecture& microarchitecture) {
			/* PVR values from:
			 * /arch/powerpc/kernel/cputable.c in Linux source tree
			 * /src/cpu/cpu_map.xml in libvirt source tree
			 * http://pearpc.sourceforge.net/pvr.html
			 * http://github.com/randombit/cpuinfo/tree/master/ppc
			 */
			switch (processorVersion & 0xFFFF0000) {
				case 0x00390000: /* PowerPC 970 */
				case 0x003C0000: /* PowerPC 970 FX */
				case 0x00440000: /* PowerPC 970 MP */
				case 0x00450000: /* PowerPC 970 GX */
					vendor = YepCpuVendorIBM;
					microarchitecture = YepCpuMicroarchitecturePowerPC970;
					return;
				case 0x003A0000: /* POWER 5 */
				case 0x003B0000: /* POWER 5+ */
					vendor = YepCpuVendorIBM;
					microarchitecture = YepCpuMicroarchitecturePOWER5;
					return;
				case 0x003E0000: /* POWER 6 */
					vendor = YepCpuVendorIBM;
					microarchitecture = YepCpuMicroarchitecturePOWER6;
					return;
				case 0x003F0000: /* POWER 7 */
				case 0x004A0000: /* POWER 7+ */
					vendor = YepCpuVendorIBM;
					microarchitecture = YepCpuMicroarchitecturePOWER7;
					return;
				case 0x004B0000: /* POWER 8 */
				case 0x004D0000: /* POWER 8 */
					vendor = YepCpuVendorIBM;
					microarchitecture = YepCpuMicroarchitecturePOWER8;
					return;
			}
			if YEP_UNLIKELY((processorVersion & 0x7FFF0000) == 0x00900000) {
				vendor = YepCpuVendorPASemi;
				microarchitecture = YepCpuMicroarchitecturePWRficient;
				return;
			}
		}

		Yep32u _processorVersion = 0x00000000u;

		Yep32u _auxHwcapVectors[2] = { 0x00000000u, 0x00000000u };

		static void parseAuxVector(YepSize type, YepSize value, void* state) {
			Yep32u* auxHwcapVectors = static_cast<Yep32u*>(state);
			switch (type) {
				case AT_HWCAP:
					auxHwcapVectors[0] = static_cast<Yep32u>(value);
					break;
				case AT_HWCAP2:
					auxHwcapVectors[1] = static_cast<Yep32u>(value);
					break;
			}
		}

		static void initProcessorIsaExtensions(Yep32u auxHwcapVectors[2], YepCpuMicroarchitecture microarchitecture, Yep64u& isaFeatures, Yep64u& simdFeatures, Yep64u& systemFeatures) {
			systemFeatures |= YepSystemFeatureCycleCounter;
			systemFeatures |= YepSystemFeatureCycleCounter64Bit;
			#if defined(YEP_POWERPC64_ABI)
				systemFeatures |= YepSystemFeatureAddressSpace64Bit;
				systemFeatures |= YepSystemFeatureGPRegisters64Bit;
			#endif

			if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_FPU) {
				isaFeatures |= YepPowerPCIsaFeatureFPU;
				if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_DFP) {
					isaFeatures |= YepPowerPCIsaFeatureDFP;
				}
			} else {
				if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_EFP_SINGLE) {
					isaFeatures |= YepPowerPCIsaFeatureEFPS;
				}
				if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_EFP_DOUBLE) {
					isaFeatures |= YepPowerPCIsaFeatureEFPD;
				}
			}

			if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_4xxMAC) {
				isaFeatures |= YepPowerPCIsaFeatureMAC;
			}

			if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE2_ISEL) {
				isaFeatures |= YepPowerPCIsaFeatureISEL;
			}

			if YEP_LIKELY(auxHwcapVectors[1] & PPC_FEATURE2_HTM) {
				isaFeatures |= YepPowerPCIsaFeatureTM;
			}

			if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_ALTIVEC) {
				simdFeatures |= YepPowerPCSimdFeatureVMX;
				if YEP_LIKELY(auxHwcapVectors[1] & PPC_FEATURE2_ARCH_2_07) {
					simdFeatures |= YepPowerPCSimdFeatureVMX207;
					if (microarchitecture == YepCpuMicroarchitecturePOWER8) {
						isaFeatures |= YepPowerPCIsaFeatureVMXCrypto;
						simdFeatures |= YepPowerPCSimdFeatureVMXRAID;
					}
				}
			}
			if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_VSX) {
				simdFeatures |= YepPowerPCSimdFeatureVSX;
				if YEP_LIKELY(auxHwcapVectors[1] & PPC_FEATURE2_ARCH_2_07) {
					simdFeatures |= YepPowerPCSimdFeatureVSX207;
				}
			}
			if YEP_LIKELY(auxHwcapVectors[0] & PPC_FEATURE_HAS_SPE) {
				simdFeatures |= YepPowerPCSimdFeatureSPE;
			}
			
			#if defined(YEP_BLUEGENE_Q_MACHINE)
				simdFeatures |= YepPowerPCSimdFeatureQPX;
			#elif defined(YEP_BLUEGENE_P_MACHINE)
				simdFeatures |= YepPowerPCSimdFeatureDoubleHummer;
			#endif
		}
	#endif

	YepStatus _yepLibrary_InitCpuInfo() {
		#if defined(YEP_BLUEGENE_SYSTEM)
			initBlueGene(_logicalCoresCount, _vendor, _microarchitecture, _isaFeatures, _simdFeatures, _systemFeatures);
		#else
			#if defined(YEP_LINUX_OS)
				_yepLibrary_InitLinuxLogicalCoresCount(_logicalCoresCount, _systemFeatures);
			#else
				#error "This OS is not supported yet"
			#endif

			initProcessorVersion(_processorVersion);
			_yepLibrary_ParseAuxVectors(parseAuxVector, static_cast<void*>(_auxHwcapVectors));

			initProcessorMicroarchitecture(_processorVersion, _vendor, _microarchitecture);

			initProcessorIsaExtensions(_auxHwcapVectors, _microarchitecture, _isaFeatures, _simdFeatures, _systemFeatures);
		#endif

		_dispatchList = _yepLibrary_GetMicroarchitectureDispatchList(_microarchitecture);
		return YepStatusOk;
	}
#else
	#error "The functions in this file should only be used in and compiled for x86/x86-64"
#endif
