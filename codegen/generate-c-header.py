#!/usr/bin/env python

import yaml
import argparse

class Function:

    def __init__(self, func, func_group):
        self.declaration = func["declaration"]
        self.java_documentation = func_group["java_documentation"]
        self.c_documentation = func_group["c_documentation"]

    @property
    def c_declaration(self):
        # Write the function documentation
        c_declaration = "/**\n"
        for doc_line in self.c_documentation.splitlines():
            c_declaration += " * " + doc_line + "\n"
        c_declaration += " */\n"

        # Write the function return type
        c_declaration += "YEP_PUBLIC_SYMBOL enum YepStatus YEPABI "

        # Parse the declaration passed in for its parameter names and types
        (name, _, args) = self.declaration.partition(" ")
        name_parts = name.split("_") # Will be ['yepModule', 'Op', 'InputTypes', 'OutputType']
        args_arr = args.split(",")
        input_types = name_parts[2]
        input_types = separate_args_in_name(input_types)
        output_type = name_parts[3]
        c_declaration += name + "("

        # Parse and write the declaration for the input args
        c_declaration += parse_arg_type(input_types[0], True) + " " + args_arr[0] + ", "
        c_declaration += parse_arg_type(input_types[1], True) + " " + args_arr[1] + ", "

        # Parse and write the output arg if it exists
        if len(args_arr) > 3:
            c_declaration += parse_arg_type(output_type, False) + " " + args_arr[2] + ", "

        # Write the length parameter
        c_declaration += "YepSize length);\n\n"

        return c_declaration


def parse_arg_type(arg_str, is_input):
    """
    This is a helper function which takes a Yeppp type found in the name
    (e.g V8s or IV16u) and returns the corresponding C type,
    ex. V8s -> const Yep8s *YEP_RESTRICT
    """
    ret = ""
    if arg_str[0] == "V":
        # This is a const vector type
        if is_input: # We don't want to make the outputs const
            ret += "const "
        ret += "Yep" + arg_str[1:] + " *YEP_RESTRICT"
        return ret
    elif arg_str[0] == "S":
        # This is a regular scalar passed by value
        return "Yep" + arg_str[1:]
    elif arg_str[0] == "I":
        # This points to both one input and where the output is stored
        return "Yep" + arg_str[2:] + " *YEP_RESTRICT"

def separate_args_in_name(arg_str):
    """
    Given a string such as IV64fV64f, it separates them into
    two and returns a list, e.g [IV64f, V64f] in this case
    """
    # Simply search for the first lowercase character and this is the split point.
    # This should maybe be replaced by something in the python standard library
    for (i,c) in enumerate(arg_str):
        if c.islower():
            split = i
            break
    return [arg_str[:split + 1], arg_str[split + 1:]]

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

        # Write the extern C decl
        for function in function_list:
            header_file.write(function.c_declaration)

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
