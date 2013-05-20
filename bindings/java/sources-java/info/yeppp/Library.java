/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	Non-computational functions for checking library version, quering information about processor, and benchmarking.
 */
public class Library {
	static {
		/* Workaround for Android which ignores rpath */
		System.loadLibrary("yeppp");
		System.loadLibrary("yeppp-jni");

		final int[] versionNumbers = new int[4];
		final String releaseName = Library.getVersionInfo(versionNumbers);
		Library.version = new Version(versionNumbers[0], versionNumbers[1], versionNumbers[2], versionNumbers[3], releaseName);
	}

	/**
	 * @brief	Queries the ticks count of the high-resolution system timer.
	 * @details	The difference in ticks between two time moments divided by timer frequency gives the number of seconds between two time moments.
	 * @return	The current ticks count of the high-resolution system timer.
	 *        	This value should be interpreted as unsigned 64-bit integer.
	 * @throws	SystemException	If the attempt to read the high-resolution timer failed inside the OS kernel.
	 */
	public static native long getTimerTicks();

	/**
	 * @brief	Queries the frequency (number of ticks per second) of the high-resolution system timer.
	 * @details	The difference in ticks between two time moments divided by timer frequency gives the number of seconds between two time moments.
	 * @return	The frequency of the high-resolution system timer.
	 *        	This value should be interpreted as unsigned 64-bit integer.
	 * @throws	SystemException	If the attempt to read the high-resolution timer frequency failed inside the OS kernel.
	 */
	public static native long getTimerFrequency();

	/**
	 * @brief	Detects the minimum time difference in nanoseconds which can be measured by the high-resolution system timer.
	 * @return	The accuracy (in nanoseconds) of the high-resolution system timer.
	 *        	This value should be interpreted as unsigned 64-bit integer.
	 * @throws	SystemException	If the attempt to measure the accuracy of high-resolution timer failed inside the OS kernel.
	 */
	public static native long getTimerAccuracy();

	/**
	 * @brief	Returns information about the vendor of the processor.
	 * @return	A CpuVendor object with information about the company which designed the CPU core.
	 * @see	CpuVendor
	 */
	public static CpuVendor getCpuVendor() {
		return Library.vendor;
	}

	/**
	 * @brief	Provides information about the architecture of the processor.
	 * @return	A CpuArchitecture instance with information about the architecture of the CPU.
	 * @see	CpuArchitecture
	 */
	public static CpuArchitecture getCpuArchitecture() {
		return Library.architecture;
	}

	/**
	 * @brief	Provides information about the microarchitecture of the processor.
	 * @return	A CpuMicroarchitecture instance with information about the microarchitecture of the CPU core.
	 * @see	CpuMicroarchitecture
	 */
	public static CpuMicroarchitecture getCpuMicroarchitecture() {
		return Library.microarchitecture;
	}

	/**
	 * @brief	Initializes the processor cycle counter and starts counting the processor cycles.
	 * @details	Call #releaseCycleCounter() to get the number of processor cycles passed.
	 * @warning	This function may allocate system resources.
	 *         	To avoid resource leak, always match a successfull call to #acquireCycleCounter() with a call to #releaseCycleCounter().
	 * @warning	The cycle counters are not guaranteed to be syncronized across different processors/cores in a multiprocessor/multicore system.
	 *         	It is recommended to bind the current thread to a particular logical processor before using this function.
	 * @return	An object representing the state of the processor cycle counter. Pass this object to #releaseCycleCounter() to get the number of cycles passed.
	 * @throws	UnsupportedHardwareException	If the processor does not have cycle counter.
	 * @throws	UnsupportedSoftwareException	If the operating system does not provide access to the CPU cycle counter.
	 * @throws	SystemException	If the attempt to initialize cycle counter failed inside the OS kernel.
	 * @see	#releaseCycleCounter()
	 */
	public static CpuCycleCounterState acquireCycleCounter() {
		final long state = Library.getCpuCyclesAcquire();
		return new CpuCycleCounterState(state);
	}

	/**
	 * @ingroup yepLibrary
	 * @brief	Stops counting the processor cycles, releases the system resources associated with the cycle counter, and returns the number of cycles elapsed.
	 * @param[in,out]	cycleCounter	An object representing the state of the cycle counter returned by #acquireCycleCounter().
	 *               	            	The cycle counter should be released only once, and this function invalidates the state object.
	 * @return	The number of cycles elapsed since the call to #acquireCycleCounter().
	 *        	This value should be interpreted as unsigned 64-bit integer.
	 * @throws	IllegalStateException	The cycleCounter object is not a valid state of the cycle counter.
	 *        	                               	This can happen if the cycleCounter object was released previously.
	 * @throws	UnsupportedHardwareException	If the processor does not have cycle counter.
	 * @throws	UnsupportedSoftwareException	If the operating system does not provide access to the CPU cycle counter.
	 * @throws	SystemException	If the attempt to read the cycle counter or release the OS resources failed inside the OS kernel.
	 * @see	#acquireCycleCounter()
	 */
	public static long releaseCycleCounter(CpuCycleCounterState cycleCounter) {
		try {
			final long cycles = Library.getCpuCyclesRelease(cycleCounter.state);
			cycleCounter.state = 0l;
			return cycles;
		} catch (IllegalStateException e) {
			cycleCounter.state = 0l;
			throw e;
		}
	}

	/**
	 * @brief	Checks if the specified ISA extension is supported by the processor.
	 * @param[in]	isaFeature	An object specifying the ISA extension of interest.
	 * @retval	true	If the processor supports the specified ISA extension.
	 * @retval	false	If the processor does not support the specificed ISA extension.
	 * @see	CpuIsaFeature, X86CpuIsaFeature, ArmCpuIsaFeature, MipsCpuIsaFeature, IA64CpuIsaFeature
	 */
	public static boolean isSupported(CpuIsaFeature isaFeature) {
		if ((isaFeature.getArchitectureId() == Library.architectureId) || (isaFeature.getArchitectureId() == CpuArchitecture.Unknown.getId())) {
			final long mask = 1l << isaFeature.getId();
			return (Library.isaFeatures & mask) != 0l;
		} else {
			return false;
		}
	}

	/**
	 * @brief	Checks if the specified SIMD extension is supported by the processor.
	 * @param[in]	simdFeature	An object specifying the SIMD extension of interest.
	 * @retval	true	If the processor supports the specified SIMD extension.
	 * @retval	false	If the processor does not support the specificed SIMD extension.
	 * @see	CpuSimdFeature, X86CpuSimdFeature, ArmCpuSimdFeature, MipsCpuSimdFeature
	 */
	public static boolean isSupported(CpuSimdFeature simdFeature) {
		if ((simdFeature.getArchitectureId() == Library.architectureId) || (simdFeature.getArchitectureId() == CpuArchitecture.Unknown.getId())) {
			final long mask = 1l << simdFeature.getId();
			return (Library.simdFeatures & mask) != 0l;
		} else {
			return false;
		}
	}

	/**
	 * @brief	Checks if processor or system support the specified non-ISA feature.
	 * @param[in]	systemFeature	An object specifying the non-ISA processor or system feature of interest.
	 * @retval	true	If the specified processor or system extension is supported on this machine.
	 * @retval	false	If the specified processor or system extension is not supported on this machine.
	 * @see	CpuSystemFeature, X86CpuSystemFeature, ArmCpuSystemFeature
	 */
	public static boolean isSupported(CpuSystemFeature systemFeature) {
		if ((systemFeature.getArchitectureId() == Library.architectureId) || (systemFeature.getArchitectureId() == CpuArchitecture.Unknown.getId())) {
			final long mask = 1l << systemFeature.getId();
			return (Library.systemFeatures & mask) != 0l;
		} else {
			return false;
		}
	}

	/**
	 * @brief	Provides information about @Yeppp library version.
	 * @return	An object describing @Yeppp library version.
	 * @see	Version
	 */
	public static Version getVersion() {
		return Library.version;
	}

	/* EXPERIMENTAL! Will be removed in future versions. */
	public static native String getCpuName();
	public static native int getCpuLogicalCoresCount();
	public static native int getCpuL0ICacheSize();
	public static native int getCpuL0DCacheSize();
	public static native int getCpuL1ICacheSize();
	public static native int getCpuL1DCacheSize();
	public static native int getCpuL2CacheSize();
	public static native int getCpuL3CacheSize();

	private static native long getCpuIsaFeatures();
	private static native long getCpuSimdFeatures();
	private static native long getCpuSystemFeatures();
	private static native int getCpuVendorId();
	private static native int getCpuArchitectureId();
	private static native int getCpuMicroarchitectureId();
	private static native long getCpuCyclesAcquire();
	private static native long getCpuCyclesRelease(long state);

	private static long isaFeatures = Library.getCpuIsaFeatures();
	private static long simdFeatures = Library.getCpuSimdFeatures();
	private static long systemFeatures = Library.getCpuSystemFeatures();
	private static CpuVendor vendor = new CpuVendor(Library.getCpuVendorId());
	private static int architectureId = Library.getCpuArchitectureId();
	private static CpuArchitecture architecture = new CpuArchitecture(architectureId);
	private static CpuMicroarchitecture microarchitecture = new CpuMicroarchitecture(Library.getCpuMicroarchitectureId());

	private static native String getVersionInfo(int[] versionNumbers);
	private static Version version;

}
