#!/usr/bin/env python

import yaml
import argparse
import os
from common.Function import Function

def generate_unit_tests(path, function_list):
    with open(path, "w") as output:
        output.write(
"""
#include <yepPredefines.h>
#include <yepPrivate.h>
#include <yepLibrary.h>
#include <library/functions.h>
#include <yepRandom.h>
#include <core/functions.h>
#include <yepBuiltin.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>


#ifdef YEP_WINDOWS_OS
	#include <windows.h>
	#define YEP_ESCAPE_NORMAL_COLOR ""
	#define YEP_ESCAPE_RED_COLOR ""
	#define YEP_ESCAPE_GREEN_COLOR ""
	#define YEP_ESCAPE_YELLOW_COLOR ""
#else
	#define YEP_ESCAPE_NORMAL_COLOR "\x1B[0m"
	#define YEP_ESCAPE_RED_COLOR "\x1B[31m"
	#define YEP_ESCAPE_GREEN_COLOR "\x1B[32m"
	#define YEP_ESCAPE_YELLOW_COLOR "\x1B[33m"
#endif


static const char* getMicroarchitectureName(YepCpuMicroarchitecture microarchitecture) {
	const YepSize bufferSize = 1024;
	static char buffer[bufferSize];
	YepSize bufferLength = bufferSize - 1;
	YepStatus status = yepLibrary_GetString(YepEnumerationCpuMicroarchitecture, microarchitecture, YepStringTypeDescription, buffer, &bufferLength);
	assert(status == YepStatusOk);
	buffer[bufferLength] = '\0';
	return buffer;
}

static void reportFailedTest(const char* functionName, YepCpuMicroarchitecture microarchitecture) {
	#ifdef YEP_WINDOWS_OS
		CONSOLE_SCREEN_BUFFER_INFO bufferInfo;
		::GetConsoleScreenBufferInfo(::GetStdHandle(STD_OUTPUT_HANDLE), &bufferInfo);
		printf("%s (%s): ", functionName, getMicroarchitectureName(microarchitecture));
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_RED | FOREGROUND_INTENSITY);
		printf("FAILED\n");
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), bufferInfo.wAttributes);
	#else
		printf("%s (%s): %sFAILED%s\n", functionName, getMicroarchitectureName(microarchitecture), YEP_ESCAPE_RED_COLOR, YEP_ESCAPE_NORMAL_COLOR);
	#endif
}

static void reportFailedTest(const char* functionName, YepCpuMicroarchitecture microarchitecture, float ulpError) {
	#ifdef YEP_WINDOWS_OS
		CONSOLE_SCREEN_BUFFER_INFO bufferInfo;
		::GetConsoleScreenBufferInfo(::GetStdHandle(STD_OUTPUT_HANDLE), &bufferInfo);
		printf("%s (%s): ", functionName, getMicroarchitectureName(microarchitecture));
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_RED | FOREGROUND_INTENSITY);
		printf("FAILED");
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), bufferInfo.wAttributes);
		printf(" (%f ULP)\n", ulpError);
	#else
		printf("%s (%s): %sFAILED%s (%f ULP)\n", functionName, getMicroarchitectureName(microarchitecture), YEP_ESCAPE_RED_COLOR, YEP_ESCAPE_NORMAL_COLOR, ulpError);
	#endif
}

static void reportPassedTest(const char* functionName, YepCpuMicroarchitecture microarchitecture) {
	#ifdef YEP_WINDOWS_OS
		CONSOLE_SCREEN_BUFFER_INFO bufferInfo;
		::GetConsoleScreenBufferInfo(::GetStdHandle(STD_OUTPUT_HANDLE), &bufferInfo);
		printf("%s (%s): ", functionName, getMicroarchitectureName(microarchitecture));
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_GREEN | FOREGROUND_INTENSITY);
		printf("PASSED\n");
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), bufferInfo.wAttributes);
	#else
		printf("%s (%s): %sPASSED%s\n", functionName, getMicroarchitectureName(microarchitecture), YEP_ESCAPE_GREEN_COLOR, YEP_ESCAPE_NORMAL_COLOR);
	#endif
}

static void reportSkippedTest(const char* functionName, YepCpuMicroarchitecture microarchitecture) {
	#ifdef YEP_WINDOWS_OS
		CONSOLE_SCREEN_BUFFER_INFO bufferInfo;
		::GetConsoleScreenBufferInfo(::GetStdHandle(STD_OUTPUT_HANDLE), &bufferInfo);
		printf("%s (%s): ", functionName, getMicroarchitectureName(microarchitecture));
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
		printf("SKIPPED\n");
		fflush(stdout);
		::SetConsoleTextAttribute(::GetStdHandle(STD_OUTPUT_HANDLE), bufferInfo.wAttributes);
	#else
		printf("%s (%s): %sSKIPPED%s\n", functionName, getMicroarchitectureName(microarchitecture), YEP_ESCAPE_YELLOW_COLOR, YEP_ESCAPE_NORMAL_COLOR);
	#endif
}


""")
        for function in function_list:
            output.write(function.unit_test)
            output.write("\n\n")

        output.write("int main (int argc, char **argv) {\n")
        boolean_names = [ "test" + "_".join(func.name.split("_")[1:]) for func in function_list ]
        for name in boolean_names:
            output.write("    YepBoolean {} = YepBooleanFalse;\n".format(name))
        output.write("    if (argc == 1) {\n")
        for name in boolean_names:
            output.write("        {} = YepBooleanTrue;\n".format(name))
        output.write(
"""     else {
        for (int i = 1; i < argc; i++) {
""")
        else_part = ""
        for name in boolean_names:
            output.write(
"""        {}if (strcmp(argv[i], \"{}\") == 0) {{
               {} = YepBooleanTrue;
           }}
""".format(else_part, "_".join(name.split("_")[1:]), name))
            else_part = "else "
        output.write(
"""

	YepStatus status = _yepLibrary_InitCpuInfo();
	assert(status == YepStatusOk);

	Yep64u supportedIsaFeatures, supportedSimdFeatures, supportedSystemFeatures;
	status = yepLibrary_GetCpuIsaFeatures(&supportedIsaFeatures);
	assert(status == YepStatusOk);
	status = yepLibrary_GetCpuSimdFeatures(&supportedSimdFeatures);
	assert(status == YepStatusOk);
	status = yepLibrary_GetCpuSystemFeatures(&supportedSystemFeatures);
	assert(status == YepStatusOk);

        Yep32s failedTests = 0;
""")
        for name in boolean_names:
            output.write(
"""
        if YEP_LIKELY({})
            failedTests += {}(supportedIsaFeatures, supportedSimdFeatures, supportedSystemFeatures);
""".format(name, "Test_{}".format(name[4:])))

        output.write("    return failedTests;\n}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unit Test Generator")
    parser.add_argument("-o", dest="output", required=True, help="Output file name")
    parser.add_argument("input", nargs=1)
    parser.add_argument("-op", dest="op", required=True, help="Operation to generate tests for")
    options = parser.parse_args()

    with open(options.input[0], "r") as specification_file:
        yaml_data = yaml.load(specification_file)
        module = yaml_data["module"]

        # Iterate through the operations of the module
        func_list = []
        for op_set in yaml_data["functions"]:
            op = op_set["operation"]
            if op != options.op: continue # Skip the operations that we don't care about

            for func_group in op_set["function_groups"]:
                for func in func_group["group"]:
                    func_list.append(Function(func, func_group))

    generate_unit_tests(options.output, func_list)

