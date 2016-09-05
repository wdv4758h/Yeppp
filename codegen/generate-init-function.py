#!/usr/bin/env python

import yaml
import argparse


def generate_init_function(module, outfile, function_list):
    """
    module: the name of the module as a string (e.g "core")
    outfile: file to write the output to
    function_list: the functions to generate initializations for
    """
    with open(outfile, "w") as init_file:
        init_file.write("""
#pragma once

#include <yepPredefines.h>
#include <yepTypes.h>
#include <yepPrivate.h>
#include <yep{1}.h>
#include <library/functions.h>
#include <{0}/yep{1}.disp.h>

YEP_INLINE static YepStatus _yep{1}_Init() {{
""".format(module, module.capitalize()))

        for func in function_list:
            init_file.write("  *reinterpret_cast<FunctionPointer*>(&_{}) = _yepLibrary_InitFunction((const FunctionDescriptor<YepStatus (*)()>*)_dispatchTable_{});\n".format(func, func))

        init_file.write("  return YepStatusOk;\n}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Init Function Generator")
    parser.add_argument("-o", dest="output", required=True, help="Output file name")
    parser.add_argument("input", nargs=1)
    options = parser.parse_args()

    with open(options.input[0], "r") as specification_file:
        yaml_data = yaml.load(specification_file)
        module = yaml_data["module"]
        func_list = []

        for op_set in yaml_data["functions"]:
            for func_group in op_set["function_groups"]:
                for func in func_group["group"]:
                    func_list.append(func["declaration"].split()[0]) # Gets the name of the function only

        generate_init_function(module, options.output, func_list)
