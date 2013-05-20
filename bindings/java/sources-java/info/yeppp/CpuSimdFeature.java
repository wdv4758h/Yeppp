/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

package info.yeppp;

/**
 * @brief	SIMD extensions.
 * @see	CpuArchitecture#iterateSimdFeatures(), Library#isSupported(CpuSimdFeature), X86CpuSimdFeature, ArmCpuSimdFeature, MipsCpuSimdFeature
 */
public class CpuSimdFeature {
	static {
		/* Workaround for Android which ignores rpath */
		System.loadLibrary("yeppp");
		System.loadLibrary("yeppp-jni");
	}

	private final int architectureId;
	private final int id;

	protected CpuSimdFeature(int id, int architectureId) {
		this.id = id;
		this.architectureId = architectureId;
	}

	protected CpuSimdFeature(int id) {
		this.id = id;
		this.architectureId = CpuArchitecture.Unknown.getId();
	}

	protected final int getId() {
		return this.id;
	}

	protected final int getArchitectureId() {
		return this.architectureId;
	}

	protected static native boolean isDefined(int id, int architectureId);
	private static native String toString(int id, int architectureId);

	public final boolean equals(CpuSimdFeature other) {
		if (other == null) {
			return false;
		} else {
			return (this.id == other.id) && (this.architectureId == other.architectureId);
		}
	}

	@Override
	public final boolean equals(Object other) {
		if (other instanceof CpuSimdFeature) {
			return this.equals((CpuSimdFeature)other);
		} else {
			return false;
		}
	}

	@Override
	public final int hashCode() {
		return this.id ^ this.architectureId;
	}

	@Override
	public final String toString() {
		return CpuSimdFeature.toString(this.id, this.architectureId);
	}
};
