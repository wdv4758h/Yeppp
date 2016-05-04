#!/usr/bin/python

import os
import subprocess
import fnmatch
import sys
import argparse
import operator
import ninja_syntax


def get_program_info(program, arguments, use_stdout=True):
    from subprocess import PIPE, Popen

    if not isinstance(arguments, list):
        arguments = [str(arguments)]
    process = Popen([program] + arguments, stdout=PIPE, stderr=PIPE, bufsize=1)
    return process.communicate()


def detect_c_compiler(program):
    _, banner = get_program_info(program, "-v")
    if banner:
        banner = banner.splitlines()
        import re
        m = re.match("gcc version (\d+(:?\.\d+)+)\\b", banner[-1])
        if m:
            return "GCC", tuple(map(int, m.group(1).split(".")))
        m = re.match("\\bclang version (\d+(:?\.\d+)+)\\b", banner[0])
        if m:
            return "Clang", tuple(map(int, m.group(1).split(".")))
        m = re.match("icc version (\d+(:?\.\d+)+)", version)
        if m:
            return "ICC", tuple(map(int, m.group(1).split(".")))
    raise ValueError("Unknown compiler at %")


class Platform:
    _supported = {
        #                          arch      os            abi     fpabi
        "x86_64-windows":         ("x86-64", "windows",    "ms",   "hard"),
        "x86_64-cygwin":          ("x86-64", "windows",    "sysv", "hard"),
        "x86_64-linux":           ("x86-64", "linux",      "sysv", "hard"),
        "x86_64-linux-x32":       ("x86-64", "linux",      "x32",  "hard"),
        "x86_64-android":         ("x86-64", "android",    "sysv", "hard"),
        "x86_64-osx":             ("x86-64", "osx",        "sysv", "hard"),
        "x86_64-nacl":            ("x86-64", "chromium",   "nacl", "hard"),
        "x86-windows":            ("x86",    "windows",    "",     "hard"),
        "x86-cygwin":             ("x86",    "cygwin",     "",     "hard"),
        "x86-linux":              ("x86",    "linux",      "",     "hard"),
        "x86-android":            ("x86",    "android",    "",     "hard"),
        "x86-osx":                ("x86",    "osx",        "",     "hard"),
        "x86-nacl":               ("x86",    "chromium",   "nacl", "hard"),
        "k1om-linux":             ("k1om",   "linux",      "",     "hard"),
        "arm-linux-eabi":         ("arm",    "linux",      "eabi", "soft"),
        "arm-linux-eabihf":       ("arm",    "linux",      "eabi", "hard"),
        "arm-android-armeabi":    ("arm",    "android",    "eabi", "soft"),
        "arm-android-armeabiv7a": ("arm",    "android",    "eabi", "softfp"),
        "arm-nacl":               ("arm",    "chromium",   "nacl", "hard"),
        "mips-android":           ("mips",   "android",    "o32",  "hard"),
        "ppc-linux":              ("ppc",    "linux",      "",     "hard"),
        "ppc64-linux":            ("ppc64",  "linux",      "",     "hard"),
        "pnacl":                  ("pnacl",  "chromium",   "",     "hard")
    }

    def __init__(self, name):
        if name not in Platform._supported.iterkeys():
            raise ValueError("Unsupported platform: " + name)
        self.name = name
        (self.arch, self.os, self.abi, self.fpabi) = Platform._supported[name]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def kernel(self):
        return {
            "android": "linux",
            "osx": "mach",
            "windows": "nt",
            "cygwin": "nt",
            "chromium": "nacl"
        }.get(self.os, self.os)

    @property
    def obj_ext(self):
        if self.os == "windows":
            return ".obj"
        elif self.arch == "pnacl":
            return ".bc"
        else:
            return ".o"

    @property
    def exe_ext(self):
        if self.os == "windows":
            return ".exe"
        elif self.os == "chromium":
            return ".pexe" if self.arch == ".pnacl" else ".nexe"
        else:
            return ""

    @property
    def dylib_ext(self):
        if self.os == "windows":
            return ".dll"
        elif self.os == "osx":
            return ".dylib"
        else:
            return ".so"

    @property
    def lib_ext(self):
        if self.os == "windows":
            return ".lib"
        elif self.arch == "pnacl":
            return ".bc"
        else:
            return ".a"

    @property
    def lib_prefix(self):
        return "" if self.os == "windows" else "lib"


class Configuration:
    def __init__(self, options, ninja_build_file="build.ninja"):
        self.output = open(ninja_build_file, "w")
        self.writer = ninja_syntax.Writer(self.output)
        self.source_dir = None
        self.build_dir = None
        self.header_dir = None
        self.unit_test_dir = None
        self.spec_dir = None
        self.platform = Platform(options.platform)

        root_dir = os.path.dirname(os.path.abspath(__file__))
        library_source_root = os.path.join(root_dir, "library", "sources")
        library_header_root = os.path.join(root_dir, "library", "headers")

        self.include_dirs = [library_header_root, library_source_root]

        if self.platform.os == "osx":
            python = "python"
            cc = options.cc if options.cc is not None else "clang"
            cxx = options.cxx if options.cxx is not None else "clang++"
            cflags = {
                "x86": ["-m32", "-march=core2", "-mno-ssse3", "-mtune=corei7-avx"],
                "x86-64": ["-m64", "-march=core2", "-mtune=corei7-avx"]
            }[self.platform.arch]
            ldflags = [cflags[0]]
            cflags += ["-O3", "-g", "-fPIC", "-Wa,--noexecstack", "-fomit-frame-pointer", "-fstrict-aliasing", "-DYEP_BUILD_LIBRARY"]
            self.include_dirs.append("/System/Library/Frameworks/JavaVM.framework/Headers/")
            cflags += ["-mmacosx-version-min=$osxmin"]
            cxxflags = list(cflags)
            cxxflags += ["-fno-rtti", "-fno-exceptions", "-fno-unwind-tables"]

            ldflags += ["-fPIC", "-dynamiclib", "-nostdlib"]
            ldflags += ["-mmacosx-version-min=$osxmin"]
            libs = ["-lc"]
        else:
            raise ValueError("Unsupported OS: " + str(self.platform.os))

        # Variables
        if self.platform.os == "osx":
            self.writer.variable("osxmin", "10.7")
        self.writer.variable("python", python)
        self.writer.variable("cc", cc)
        self.writer.variable("cxx", cxx)
        self.writer.variable("cflags", " ".join(cflags))
        self.writer.variable("cxxflags", " ".join(cxxflags))
        self.writer.variable("ldflags", " ".join(ldflags))
        self.writer.variable("libs", " ".join(libs))
        self.writer.variable("ar", "ar")
        if self.platform.os == "osx":
            self.writer.variable("dsymutil", "dsymutil")
        self.writer.variable("strip", "strip")

        # Rules
        self.writer.rule("cc", "$cc $cflags -MMD -MT $out -MF $out.d -o $out -c $src",
            description="CC $descpath",
            depfile="$out.d")
        self.writer.rule("cxx", "$cxx $cxxflags -MMD -MT $out -MF $out.d -o $out -c $src",
            description="CXX $descpath",
            depfile="$out.d")
        self.writer.rule("cxxld", "$cxx -o $out $in $ldflags $libs",
            description="CXXLD $descpath")
        self.writer.rule("cxxexec", "$cxx -o $out $in",
            description="Build CXX Binary $descpath")
        self.writer.rule("ar", "$ar $arflags rcs $out $in",
            description="AR $descpath")
        self.writer.rule("peachpy-obj",
            "$python -m peachpy.$arch -mabi=$abi -mimage-format=$image_format -fname-mangling=\"_\$${Name}_\$${uArch}_\$${ISA}\"" \
            " -emit-json-metadata $json_file -emit-c-header $header -o $object_file $in",
            description="PEACHPY $descpath")
        self.writer.rule("generate-dispatch-table",
            "$python codegen/generate-dispatch-table.py --yaml $yaml -o $srcout $json",
            description="GENERATE $descpath")
        self.writer.rule("generate-c-header",
            "$python codegen/generate-c-header.py $in -o $out",
            description="GENERATE $descpath")
        self.writer.rule("generate-default-impl",
            "$python codegen/generate-default-impl.py $in -o $out",
            description="GENERATE $descpath")
        self.writer.rule("generate-init-function",
            "$python codegen/generate-init-function.py $in -o $out",
            description="GENERATE $descpath")
        self.writer.rule("generate-unit-test",
            "$python codegen/generate-unit-test.py $yaml -o $out -op=$op",
            description="GENERATE $descpath")
        if self.platform.os == "osx":
            self.writer.rule("dbgextract", "$dsymutil --flat --out=$dbgfile $in && $strip -o $objfile -x $in",
                description="DBGEXTRACT $descpath")


    def generate_dispatch_table(self, yaml_file, json_files, source_files):
        self.writer.build(source_files, "generate-dispatch-table", [yaml_file] + json_files,
            variables={
                "yaml": yaml_file,
                "json": " ".join(json_files),
                "descpath": os.path.relpath(source_files[0], self.build_dir),
                "srcout": source_files[0]})
        return source_files

    def generate_c_header(self, yaml_file, source_file=None):
        if source_file is None:
            module_name = os.path.splitext(os.path.basename(os.path.relpath(yaml_file, self.spec_dir)))[0]
            source_file = os.path.join(self.header_dir, "yep{Module}.h".format(Module=module_name.capitalize()))
        self.writer.build(source_file, "generate-c-header", yaml_file,
            variables={
                "descpath": os.path.relpath(source_file, self.build_dir)})
        return source_file

    def generate_init_function(self, yaml_file, source_file=None):
        if source_file is None:
            module_name = os.path.splitext(os.path.basename(os.path.relpath(yaml_file, self.spec_dir)))[0]
            source_file = os.path.join(self.source_dir, module_name, "yep{Module}".format(Module=module_name.capitalize())) + ".init.h"
        self.writer.build(source_file, "generate-init-function", yaml_file,
            variables={
                "descpath": os.path.relpath(source_file, self.build_dir)})
        return source_file

    def generate_default_impl(self, yaml_file, source_file=None):
        if source_file is None:
            module_name = os.path.splitext(os.path.basename(os.path.relpath(yaml_file, self.spec_dir)))[0]
            source_file = os.path.join(self.source_dir, module_name, "yep{Module}".format(Module=module_name.capitalize())) + ".impl.cpp"
        self.writer.build(source_file, "generate-default-impl", yaml_file,
            variables={
                "descpath": os.path.relpath(source_file, self.build_dir)})
        return source_file

    def generate_unit_test(self, yaml_file, op, source_file=None, extra_deps=[]):
        if source_file is None:
            source_file = os.path.join(self.unit_test_dir, op + ".cpp")
        self.writer.build(source_file, "generate-unit-test", [yaml_file] + extra_deps,
            variables={
                "descpath": os.path.relpath(source_file, self.build_dir),
                "yaml": yaml_file,
                "op": op})
        return source_file

    def compile_peachpy(self, source_file, object_file=None):
        if object_file is None:
            object_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + self.platform.obj_ext
        platform_map = {
            #                          arch      abi      image_format
            "x86_64-windows":         ("x86_64", "ms",    "mscoff"),
            "x86_64-linux":           ("x86_64", "sysv",  "elf"),
            "x86_64-linux-x32":       ("x86_64", "x32",   "elf"),
            "x86_64-android":         ("x86_64", "sysv",  "mach-o"),
            "x86_64-osx":             ("x86_64", "sysv",  "mach-o"),
            "x86_64-nacl":            ("x86_64", "nacl",  "elf"),
        }
        if self.platform.name not in platform_map:
            raise ValueError("PeachPy is not supported on %s platform" % self.platform.name)
        (arch, abi, image_format) = platform_map[self.platform.name]
        json_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + ".json"
        variables = {
            "arch": arch,
            "abi": abi,
            "image_format": image_format,
            "header": source_file[:-3] + ".h",
            "json_file": json_file,
            "object_file": object_file
        }
        self.writer.build([object_file, json_file], "peachpy-obj", source_file, variables=variables)
        return object_file, json_file

    def compile_c(self, source_file, object_file=None, extra_deps=[]):
        if object_file is None:
            object_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + self.platform.obj_ext
        variables = {
            "src": source_file,
            "descpath": os.path.relpath(source_file, self.source_dir)
        }
        if self.include_dirs:
            variables["cflags"] = "$cflags " + " ".join("-I" + include_dir for include_dir in self.include_dirs)
        self.writer.build(object_file, "cc", [source_file] + extra_deps, variables=variables)
        return object_file

    def compile_cxx(self, source_file, object_file=None, extra_deps=[]):
        if object_file is None:
            object_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + self.platform.obj_ext
        variables = {
            "src": source_file,
            "descpath": os.path.relpath(source_file, self.source_dir)
        }
        if self.include_dirs:
            variables["cxxflags"] = "$cxxflags " + " ".join("-I" + include_dir for include_dir in self.include_dirs)
        self.writer.build(object_file, "cxx", [source_file] + extra_deps, variables=variables)
        return object_file

    def link_cxx_library(self, object_files, library_file):
        self.writer.build(library_file, "cxxld", object_files,
            variables={"descpath": os.path.relpath(library_file, self.build_dir)})
        return library_file

    def link_cxx_executable(self, object_files, executable_file):
        self.writer.build(executable_file, "cxxexec", object_files)
        return executable_file

    def link_c_executable(self, source_files, executable_file):
        self.writer.build(executable_file, "ccld", source_files,
            variables={"descpath": os.path.relpath(executable_file, self.build_dir)})
        return executable_file

    def extract_debug_symbols(self, unstripped_file, stripped_file, debug_file):
        variables = {
            "dbgfile": debug_file,
            "objfile": stripped_file,
            "descpath": os.path.relpath(unstripped_file, self.build_dir)
        }
        self.writer.build([stripped_file, debug_file], "dbgextract", unstripped_file, variables=variables)
        return stripped_file, debug_file

parser = argparse.ArgumentParser(
    description="Yeppp! configuration script")
parser.add_argument("-p", "--platform", dest="platform", required=True,
    choices=Platform._supported)
parser.add_argument("--with-cc", dest="cc")
parser.add_argument("--with-cxx", dest="cxx")


def main():
    options = parser.parse_args()

    config = Configuration(options)

    root_dir = os.path.dirname(os.path.abspath(__file__))
    library_source_root = os.path.join(root_dir, "library", "sources")
    library_header_root = os.path.join(root_dir, "library", "headers")
    library_build_root = os.path.join(root_dir, "build", config.platform.name)
    library_spec_root = os.path.join(root_dir, "specs")
    library_unit_test_root = os.path.join(root_dir, "unit-test")

    library_object_files = []
    config.source_dir = library_source_root
    config.build_dir = library_build_root
    config.header_dir = library_header_root
    config.spec_dir = library_spec_root
    config.unit_test_dir = library_unit_test_root
    source_extensions = ["*.c", "*.cpp", "*.py"]

    generated_public_headers = []
    generated_init_functions = []
    generated_implementations = []
    spec_files = [os.path.join(library_spec_root, yaml_file) for yaml_file in os.listdir(library_spec_root) if fnmatch.fnmatch(yaml_file, "*.yaml")]
    for yaml_file in spec_files:
        generated_public_headers.append(config.generate_c_header(yaml_file))
        generated_init_functions.append(config.generate_init_function(yaml_file))
        generated_implementations.append(config.generate_default_impl(yaml_file))

    for impl_src in generated_implementations:
        library_object_files.append(config.compile_cxx(impl_src, extra_deps=generated_public_headers))

    json_metadata_files = []
    for (source_dir, source_subdir, filenames) in os.walk(library_source_root):
        source_filenames = sum(map(lambda pattern: fnmatch.filter(filenames, pattern), source_extensions), [])
        source_filenames = map(lambda path: os.path.join(source_dir, path), source_filenames)
        for source_filename in source_filenames:
            relative_source_filename = os.path.relpath(source_filename, root_dir)
            if os.path.basename(source_filename) == "Init.cpp":
                continue # We need to generate yepModule.disp.h before Init.o, but this requires generating the JSON files first
            if relative_source_filename == "library/sources/library/CpuX86.cpp" and config.platform.arch not in {"x86", "x86-64"}:
                continue
            if relative_source_filename == "library/sources/library/CpuPPC.cpp" and config.platform.arch not in {"ppc", "ppc64"}:
                continue
            if relative_source_filename == "library/sources/library/CpuMips.cpp" and config.platform.arch not in {"mips"}:
                continue
            if relative_source_filename == "library/sources/library/CpuArm.cpp" and config.platform.arch != "arm":
                continue
            if relative_source_filename == "library/sources/library/CpuLinux.cpp" and config.platform.kernel != "linux":
                continue
            if relative_source_filename == "library/sources/library/Unsafe.cpp" and config.platform.kernel != "linux":
                continue
            if relative_source_filename == "library/sources/library/CpuWindows.cpp" and config.platform.kernel not in {"nt"}:
                continue
            if relative_source_filename == "library/sources/library/CpuMacOSX.cpp" and config.platform.kernel not in {"mach"}:
                continue

            if source_filename.endswith(".py") and os.path.basename(source_filename).startswith("yep"):
                object_file, json_file = config.compile_peachpy(source_filename)
                json_metadata_files.append(json_file)
                library_object_files.append(object_file)
            elif source_filename.endswith(".cpp"):
                library_object_files.append(config.compile_cxx(source_filename, extra_deps=generated_public_headers))

    # Generating Dispatch Tables
    dispatch_headers = []
    for yaml_file in spec_files:
        module_name = os.path.basename(os.path.splitext(yaml_file)[0])
        module_json_files = [ f for f in json_metadata_files if module_name.capitalize() in f ]
        src_and_hdr = ["yep{}.disp.cpp".format(module_name.capitalize()), "yep{}.disp.h".format(module_name.capitalize())]
        full_path_src_and_hdr = map(lambda x: os.path.join(library_source_root, module_name, x), src_and_hdr)
        dispatch_headers.append(full_path_src_and_hdr[1])
        dispatch_table_src, dispatch_table_header = config.generate_dispatch_table(yaml_file, module_json_files, full_path_src_and_hdr)
        library_object_files.append(config.compile_cxx(dispatch_table_src, extra_deps=generated_public_headers + [full_path_src_and_hdr[1]]))

    library_object_files.append(config.compile_cxx("library/sources/library/Init.cpp", extra_deps=generated_public_headers + dispatch_headers))

    # Generate unit tests
    ops = ["Add", "Multiply"]
    unit_test_source_files = {}
    for op in ops:
        source_file = config.generate_unit_test(os.path.join(library_spec_root, "core.yaml"), op, extra_deps=dispatch_headers)
        unit_test_source_files[op] = source_file
    unit_test_object_files = {}
    for op,src in unit_test_source_files.items():
        unit_test_object_files[op] = config.compile_cxx(src, extra_deps=generated_public_headers)

    config.source_dir = library_source_root
    config.build_dir = library_build_root
    libyeppp = config.link_cxx_library(library_object_files, os.path.join(library_build_root, "libyeppp.dylib"))
    binary_dir = os.path.join(root_dir, "binaries", config.platform.os, config.platform.arch.replace('-', '_'))
    config.extract_debug_symbols(libyeppp, os.path.join(binary_dir, "libyeppp.dylib"), os.path.join(binary_dir, "libyeppp.dylib.dSYM"))

    for op in ops:
        config.link_cxx_executable(library_object_files + [unit_test_object_files[op]], os.path.join(library_unit_test_root, op + "Test"))

if __name__ == "__main__":
    sys.exit(main())
