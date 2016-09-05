#!/usr/bin/env python

import yaml
import argparse
import os
from common.Function import Function

def generate_benchmarks(path, function_list):
    with open(path, "w") as output:
        output.write(
"""
#include <yepPredefines.h>
#include <yepPrivate.h>
#include <yepLibrary.h>
#include <library/functions.h>
#include <yepRandom.h>
#include <core/yepCore.init.h>
#include <math/yepMath.init.h>
#include <yepBuiltin.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>

static const char* getMicroarchitectureName(YepCpuMicroarchitecture microarchitecture) {
	const YepSize bufferSize = 1024;
	static char buffer[bufferSize];
	YepSize bufferLength = bufferSize - 1;
	YepStatus status = yepLibrary_GetString(YepEnumerationCpuMicroarchitecture, microarchitecture, YepStringTypeDescription, buffer, &bufferLength);
	assert(status == YepStatusOk);
	buffer[bufferLength] = '\\0';
	return buffer;
}

static void reportBenchmark(const char * functionName, const char * arch, Yep64u startTicks, Yep64u endTicks) {
    static Yep64u frequency = 0;
    if (frequency == 0) {
        yepLibrary_GetTimerFrequency(&frequency);
    }
    Yep64f sec = (Yep64f)(endTicks - startTicks) / (Yep64f)frequency;
    printf("%s (%s): %f\\n", functionName, arch, sec);
}

""")

        for function in function_list:
            output.write(function.benchmark)
            output.write("\n\n")

        output.write("int main(int argc, char **argv) {\n")

        boolean_names = [ "bench" + "_".join(func.name.split("_")[1:]) for func in function_list ]
        for name in boolean_names:
            output.write("    YepBoolean {} = YepBooleanFalse;\n".format(name))
        output.write("    if (argc == 1) {\n")
        for name in boolean_names:
            output.write("        {} = YepBooleanTrue;\n".format(name))
        output.write(
"""     } else {
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

        output.write("        }\n")
        output.write("    }\n")
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
""")
        for name in boolean_names:
            output.write(
"""
        if YEP_LIKELY({})
            {}(supportedIsaFeatures, supportedSimdFeatures, supportedSystemFeatures);
""".format(name, "Benchmark_{}".format(name[5:])))

        output.write("    return 0;\n}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Generator")
    parser.add_argument("-o", dest="output", required=True, help="Output file name")
    parser.add_argument("input", nargs=1)
    parser.add_argument("-op", dest="op", required=True, help="Operation to generate benches for")
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

    generate_benchmarks(options.output, func_list)

