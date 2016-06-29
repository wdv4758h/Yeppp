#!/usr/bin/env python

import json
import argparse
import os
import yaml
from common.Function import Function


def generate_includes(src_dir, module):
    outfile.write("""
#include <yepPrivate.h>
#include <yep{}.h>
""".format(module.capitalize()))
    for dir_path,subdirs,build_files in os.walk(src_dir):
        for build_file in build_files:
            if build_file.endswith(".h"):
                outfile.write("#include <{}/{}>\n".format(module, build_file))


def generate_dispatch_table_header():
    pre, ext = os.path.splitext(options.output)
    header_out = pre + ".h"
    with open(header_out, "w") as header_outfile:
        header_outfile.write("""
#pragma once

#include <yepPredefines.h>
#include <yepTypes.h>
#include <yepPrivate.h>

""")
        for func in all_functions.values():
            header_outfile.write(func.default_impl_declaration)
            header_outfile.write("\n")


        for func in all_functions.values():
            header_outfile.write(func.dispatch_table_declaration)
            header_outfile.write("\n")

        header_outfile.write("\n\n")

        for func in all_functions.values():
            header_outfile.write(func.function_pointer_declaration)
            header_outfile.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates Dispatch tables for Yeppp")
    parser.add_argument("-o", dest="output", required=True, help="Output File name")
    parser.add_argument("input", nargs="*")
    parser.add_argument("--yaml", dest="specfile")
    options = parser.parse_args()

    outfile = open(options.output, "w")

    # Open the specfile and parse it with the YAML parser
    specfile = open(options.specfile, "r")
    yaml_data = yaml.load(specfile)
    module = yaml_data["module"]
    all_functions = {}
    for op_set in yaml_data["functions"]:
        for func_group in op_set["function_groups"]:
            for func in func_group["group"]:
                # Map function names -> Function objects
                all_functions[func["declaration"].split()[0]] = Function(func, func_group)


    # Put all implementations of a given function specialization in
    # a dictionary indexed by name.  E.g "yepCore_Add_V8sV8s_V8s" ->
    # a list of all implementations of that function's JSON data
    # Parse all JSON files and mark them as having assembly implementations
    json_files = options.input
    decoder = json.JSONDecoder()
    for json_file in json_files:
        with open(json_file) as json_f:
            metadata = decoder.decode(json_f.read())
            for func_data in metadata:
                func_name = func_data["name"]
                all_functions[func_name].asm_impl_metadata.append(func_data)

    generate_includes("library/sources/" + module, module) # Write the #include<> at head
    generate_dispatch_table_header()

    # Generate dispatch tables
    outfile.write("\n")
    for func in all_functions.values():
        outfile.write(func.dispatch_table)

    # Generate dispatch function pointers
    outfile.write("\n")
    for func in all_functions.values():
        outfile.write("\n")
        outfile.write(func.function_pointer_definition)

    # Write the functions which call the function pointers from dispatch table
    outfile.write("\n\n")
    for func in all_functions.values():
        outfile.write(func.dispatch_stub)
        outfile.write("\n\n")

