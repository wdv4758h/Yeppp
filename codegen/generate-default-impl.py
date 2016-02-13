#!/usr/bin/env python

import yaml
import argparse
import os
from Function import Function


def generate_default_implementations(path, function_list):
    with open(path, "w") as impl_file:
        impl_file.write("""
#include <yepBuiltin.h>
#include <yepCore.h>

""")
        for function in function_list:
            impl_file.write(function.default_implementation + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Default Implementation Generator")
    parser.add_argument("-o", dest="output", required=True, help="Output file name")
    parser.add_argument("input", nargs=1)
    parser.add_argument("--op-to-generate", required=True, dest="op_to_generate", help="The operation to generate default impls for")
    options = parser.parse_args()

    # The file name with no path, e.g Add.impl.cpp
    file_name = os.path.split(options.output)[1]

    # Determine which operation we are generating the default implementations for
    op_to_generate = options.op_to_generate

    with open(options.input[0], "r") as specification_file:
        yaml_data = yaml.load(specification_file)
        module = yaml_data["module"]

        func_list = []

        # Iterate through the operations of the module
        for op_set in yaml_data["functions"]:
            op = op_set["operation"]

            # Only want to generate for a specific operation
            if op.lower() != options.op_to_generate.lower(): continue

            # Iterates through each function group of the operation,
            # where a group consists of functions which add vectors to vectors,
            # functions which add scalars to vectors, etc.
            for func_group in op_set["function_groups"]:

                # Now actually iterate through individual functions
                for func in func_group["group"]:
                    func_list.append(Function(func, func_group))

        generate_default_implementations(options.output, func_list)
