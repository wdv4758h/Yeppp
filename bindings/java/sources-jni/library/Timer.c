/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under 2-clause BSD license.
 * See library/LICENSE.txt for details.
 *
 */

#include <jni.h>
#include <yepPrivate.hpp>
#include <yepLibrary.h>
#include <yepJavaPrivate.h>

JNIEXPORT jlong JNICALL Java_info_yeppp_Library_getTimerTicks(JNIEnv *env, jclass class) {
	Yep64u ticks = 0ull;
	enum YepStatus status;
	status = yepLibrary_GetTimerTicks(&ticks);
	if (status != YepStatusOk) {
		yepJNI_ThrowSuitableException(env, status);
	}
	return ticks;
}

JNIEXPORT jlong JNICALL Java_info_yeppp_Library_getTimerFrequency(JNIEnv *env, jclass class) {
	Yep64u frequency = 0ull;
	enum YepStatus status;
	status = yepLibrary_GetTimerFrequency(&frequency);
	if (status != YepStatusOk) {
		yepJNI_ThrowSuitableException(env, status);
	}
	return frequency;
}

JNIEXPORT jlong JNICALL Java_info_yeppp_Library_getTimerAccuracy(JNIEnv *env, jclass class) {
	Yep64u accuracy = 0ull;
	enum YepStatus status;
	status = yepLibrary_GetTimerAccuracy(&accuracy);
	if (status != YepStatusOk) {
		yepJNI_ThrowSuitableException(env, status);
	}
	return accuracy;
}
