#!/usr/bin/env python

import yaml
import argparse
from common.Function import Function

def generate_c_header(header_path, function_list):
    with open(header_path, "w") as header_file:
        # Write the includes
        header_file.write("""
#pragma once

#include <yepPredefines.h>
#include <yepTypes.h>

#ifdef __cplusplus
    extern "C" {
#endif

""")

        for function in function_list:
            header_file.write(function.c_declaration)
            header_file.write("\n")

        # Close C decl
        header_file.write("""\
#ifdef __cplusplus
    } /* extern "C" */
#endif

""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="C header generator")
    parser.add_argument("-o", dest="output", required=True, help="Output file name")
    parser.add_argument("input", nargs=1)
    options = parser.parse_args()

    with open(options.input[0], "r") as specification_file:
        yaml_data = yaml.load(specification_file)
        module = yaml_data["module"]

        # A list of all of the function objects for this module.
        # Later it may be better to group these keyed by an operation or something
        func_list = []

        # Iterate through each operation the module supports (the functions
        # are grouped logically by their operation, e.g Add, Sub)
        for op_set in yaml_data["functions"]:
            op = op_set["operation"]

            # Iterate through each function group within an operation.
            # A group would be functions which operate on two vectors and output a third vector,
            # functions which operate on a vector and a scalar, etc.
            # These functions will share documentation among other things.
            for func_group in op_set["function_groups"]:

                # Now actually iterate through the individual functions in the group
                for func in func_group["group"]:
                    func_list.append(Function(func, func_group))

        generate_c_header(options.output, func_list)
