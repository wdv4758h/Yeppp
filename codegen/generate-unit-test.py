#!/usr/bin/env python

import yaml
import argparse
import os
from common.Function import Function

def generate_unit_tests(path, function_list):
    for function in function_list:
        print function.unit_test
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unit Test Generator")
    parser.add_argument("-o", dest="output", required=True, help="Output file name")
    parser.add_argument("input", nargs=1)
    options = parser.parse_args()

    with open(options.input[0], "r") as specification_file:
        yaml_data = yaml.load(specification_file)
        module = yaml_data["module"]

        # Iterate through the operations of the module
        func_list = []
        for op_set in yaml_data["functions"]:
            op = op_set["operation"]

            for func_group in op_set["function_groups"]:
                for func in func_group["group"]:
                    func_list.append(Function(func, func_group))
    
    generate_unit_tests(options.output, func_list)

