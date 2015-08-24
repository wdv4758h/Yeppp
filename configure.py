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
        self.platform = Platform(options.platform)

        root_dir = os.path.dirname(os.path.abspath(__file__))
        library_source_root = os.path.join(root_dir, "library", "sources")
        library_header_root = os.path.join(root_dir, "library", "headers")
        jni_source_root = os.path.join(root_dir, "bindings", "java", "sources-jni")

        self.include_dirs = [library_header_root, library_source_root, jni_source_root]

        if self.platform.os == "osx":
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
        self.writer.variable("cc", cc)
        self.writer.variable("cxx", cxx)
        self.writer.variable("cflags", " ".join(cflags))
        self.writer.variable("cxxflags", " ".join(cxxflags))
        self.writer.variable("ldflags", " ".join(ldflags))
        self.writer.variable("libs", " ".join(libs))
        self.writer.variable("ar", "ar")
        self.writer.variable("nasm", "nasm")
        if self.platform.os == "osx":
            self.writer.variable("dsymutil", "dsymutil")
        self.writer.variable("strip", "strip")

        # Rules
        self.writer.rule("cc", "$cc $cflags -MMD -MT $out -MF $out.d -o $out -c $in",
            description="CC $descpath",
            depfile="$out.d")
        self.writer.rule("cxx", "$cxx $cxxflags -MMD -MT $out -MF $out.d -o $out -c $in",
            description="CXX $descpath",
            depfile="$out.d")
        self.writer.rule("cxxld", "$cxx -o $out $in $ldflags $libs",
            description="CXXLD $descpath")
        self.writer.rule("ar", "$ar $arflags rcs $out $in",
            description="AR $descpath")
        self.writer.rule("nasm", "$nasm -o $out $nasmflags $in",
            description="NASM $descpath")
        self.writer.rule("peachpy-obj", "$python -m peachpy.$arch -mabi=$abi -mimage-format=$image_format -o $out $in")
        if self.platform.os == "osx":
            self.writer.rule("dbgextract", "$dsymutil --flat --out=$dbgfile $in && $strip -o $objfile -x $in",
                description="DBGEXTRACT $descpath")

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
        variables = {
            "arch": arch,
            "abi": abi,
            "image_format": image_format
        }
        self.writer.build(object_file, "peachpy-obj", source_file, variables=variables)
        return source_file


    def compile_nasm(self, source_file, object_file=None):
        if object_file is None:
            object_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + self.platform.obj_ext
        nasm_format_map = {
            "x86_64-windows": "win64",
            "x86_64-linux": "elf64",
            "x86_64-android": "elf64",
            "x86_64-osx": "macho64",
            "x86-windows": "win32",
            "x86-linux": "elf32",
            "x86-android": "elf32",
            "x86-osx": "macho32"
        }
        if self.platform.name not in nasm_format_map:
            raise ValueError("nasm is not supported on %s platform" % self.platform.name)
        variables={
            "nasmflags": "-f " + nasm_format_map[self.platform.name],
            "descpath": os.path.relpath(source_file, self.source_dir)
        }
        self.writer.build(object_file, "nasm", source_file, variables=variables)
        return object_file

    def compile_c(self, source_file, object_file=None):
        if object_file is None:
            object_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + self.platform.obj_ext
        variables = {
            "descpath": os.path.relpath(source_file, self.source_dir)
        }
        if self.include_dirs:
            variables["cflags"] = "$cflags " + " ".join("-I" + include_dir for include_dir in self.include_dirs)
        self.writer.build(object_file, "cc", source_file, variables=variables)
        return object_file

    def compile_cxx(self, source_file, object_file=None):
        if object_file is None:
            object_file = os.path.join(self.build_dir, os.path.relpath(source_file, self.source_dir)) + self.platform.obj_ext
        variables = {
            "descpath": os.path.relpath(source_file, self.source_dir)
        }
        if self.include_dirs:
            variables["cxxflags"] = "$cxxflags " + " ".join("-I" + include_dir for include_dir in self.include_dirs)
        self.writer.build(object_file, "cxx", source_file, variables=variables)
        return object_file

    def link_cxx_library(self, object_files, library_file):
        self.writer.build(library_file, "cxxld", object_files,
            variables={"descpath": os.path.relpath(library_file, self.build_dir)})
        return library_file

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
parser.add_argument("--with-nasm", dest="nasm", default="nasm")


def main():
    options = parser.parse_args()

    config = Configuration(options)

    root_dir = os.path.dirname(os.path.abspath(__file__))
    library_source_root = os.path.join(root_dir, "library", "sources")
    library_header_root = os.path.join(root_dir, "library", "headers")
    jni_source_root = os.path.join(root_dir, "bindings", "java", "sources-jni")
    library_build_root = os.path.join(root_dir, "library", "build", config.platform.name)
    jni_build_root = os.path.join(root_dir, "bindings", "java", "build", config.platform.name)

    library_object_files = []
    config.source_dir = library_source_root
    config.build_dir = library_build_root
    source_extensions = ["*.c", "*.cpp"]
    if config.platform.arch == "x86-64" and config.platform.abi == "sysv":
        source_extensions += ["*.x64-sysv.asm"]
    if config.platform.arch == "x86-64" and config.platform.abi == "ms":
        source_extensions += ["*.x64-ms.asm"]
    for (source_dir, source_subdir, filenames) in os.walk(library_source_root):
        source_filenames = sum(map(lambda pattern: fnmatch.filter(filenames, pattern), source_extensions), [])
        source_filenames = map(lambda path: os.path.join(source_dir, path), source_filenames)
        for source_filename in source_filenames:
            relative_source_filename = os.path.relpath(source_filename, root_dir)
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

            if source_filename.endswith(".asm"):
                library_object_files.append(config.compile_nasm(source_filename))
            else:
                library_object_files.append(config.compile_cxx(source_filename))
    config.source_dir = jni_source_root
    config.build_dir = jni_build_root
    for (source_dir, source_subdir, filenames) in os.walk(os.path.join(root_dir, "bindings", "java", "sources-jni")):
        source_filenames = sum(map(lambda pattern: fnmatch.filter(filenames, pattern), ["*.c"]), [])
        source_filenames = map(lambda path: os.path.join(source_dir, path), source_filenames)
        for source_filename in source_filenames:
            library_object_files.append(config.compile_c(source_filename))

    config.source_dir = library_source_root
    config.build_dir = library_build_root
    libyeppp = config.link_cxx_library(library_object_files, os.path.join(library_build_root, "libyeppp.dylib"))
    binary_dir = os.path.join(root_dir, "binaries", config.platform.os, config.platform.arch)
    config.extract_debug_symbols(libyeppp, os.path.join(binary_dir, "libyeppp.dylib"), os.path.join(binary_dir, "libyeppp.dylib.dSYM"))

if __name__ == "__main__":
    sys.exit(main())
