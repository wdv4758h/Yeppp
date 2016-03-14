from string_template import StringTemplate

class Function:
    """
    Represents a particular specialization of a Yeppp function.
    Functions know how to generate their own declarations and
    default implementations
    """

    def __init__(self, func, func_group, has_asm_impl=False):
        self.yaml_declaration = func["declaration"] # This needs to be parsed to get function info
        self.java_documentation = func_group["java_documentation"]
        self.c_documentation = func_group["c_documentation"]
        self.default_impl_template = func_group["default_implementation_template"]

        # Parse the yaml declaration to gather info about the functions arguments and C decl
        self.name, _, args_str = self.yaml_declaration.partition(" ")
        name_parts = self.name.split("_") # Will be ['yepModule', 'Op', 'InputTypes', 'OutputType']
        input_types_encoded = self._separate_args_in_name(name_parts[2])
        output_type_encoded = name_parts[3]

        args_arr = args_str.split(",")
        args_arr = [ a.lstrip().rstrip() for a in args_arr ]

        # self.arguments will be an array of Argument objects we will use to generate everything
        self.arguments = []
        self._parse_arg_types(args_arr, input_types_encoded, output_type_encoded)

        self.has_asm_impl = has_asm_impl


    @property
    def dispatch_table(self):
        """
        Generate the dispatch table for this function,
        which does not have an asm implementation (since those
        dispatch tables are generated from .json files)
        """
        ret = "YEP_USE_DISPATCH_TABLE_SECTION const FunctionDescriptor<YepStatus (YEPABI*)("
        for i,arg in enumerate(self.arguments):
            ret += arg.full_arg_type
            if i != len(self.arguments) - 1:
                ret += ", "
        ret += ")> _dispatchTable_{}[] = {{\n".format(self.name)


        ret += "    YEP_DESCRIBE_FUNCTION_IMPLEMENTATION(_{},\
        YepIsaFeaturesDefault, YepSimdFeaturesDefault, YepSystemFeaturesDefault,\
        YepCpuMicroarchitectureUnknown, \"c++\", \"Naive\", \"None\")\n}};".format(self.name)
        return ret


    @property
    def dispatch_table_declaration(self):
        """
        Generate the declaration of the dispatch table for the header
        """
        ret = "extern \"C\" YEP_PRIVATE_SYMBOL const FunctionDescriptor<YepStatus (YEPABI*)("
        for i, arg in enumerate(self.arguments):
            ret += arg.full_arg_type
            if i != len(self.arguments) - 1:
                ret += ", "
        ret += ")> _dispatchTable_{}[];".format(self.name)
        return ret


    @property
    def c_declaration(self):
        """
        Generate the C declaration for this function, which will be used
        in the generated C headers
        """
        # Write the function return type
        c_declaration = "YEP_PUBLIC_SYMBOL enum YepStatus YEPABI "

        # Parse the declaration passed in for its parameter names and types
        c_declaration += self.name + "("

        # Parse and write the declaration for the input args
        for i,arg in enumerate(self.arguments):
            c_declaration += arg.declaration
            if i != len(self.arguments) - 1:
                c_declaration += ", "
        c_declaration += ");"
        return c_declaration


    @property
    def default_implementation(self):
        """
        Generate the default implementation for this function
        based on the template in the YAML file
        """
        # Write the declaration
        default_impl = "extern \"C\" YEP_LOCAL_SYMBOL YepStatus _{}_Default(".format(self.name)
        for i,arg in enumerate(self.arguments):
            default_impl += arg.declaration
            if i != len(self.arguments) - 1:
                default_impl += ", "
        default_impl += ") {"

        # Generate null pointer, alignment checks
        arg_checker = ArgumentCheckGenerator(self.arguments)
        checks = arg_checker.generate_arg_checks()
        for check in checks:
            default_impl += check
        default_impl += "\n"

        # Write the body of the implementation
        template = StringTemplate(self.default_impl_template)
        body = template.eval_template({ x.name: x for x in self.arguments })
        default_impl += "  " # We need to add indentation of the body here
        for i,c in enumerate(body):
            default_impl += c
            if c == "\n" and i != len(body) - 1:
                default_impl += "  "
        default_impl += "}\n"
        return default_impl


    @property
    def c_documentation(self):
        return self.c_documentation


    @property
    def function_pointer_definition(self):
        return "YEP_USE_DISPATCH_POINTER_SECTION YepStatus (YEPABI*_{})({}) = YEP_NULL_POINTER;".format(self.name, ", ".join([arg.full_arg_type for arg in self.arguments]))


    @property
    def function_pointer_declaration(self):
        return "extern \"C\" YEP_PRIVATE_SYMBOL YepStatus (YEPABI* _{})({});".format(self.name,
                ', '.join([arg.declaration for arg in self.arguments]))


    @property
    def dispatch_stub(self):
        args_names = ", ".join([arg.name for arg in self.arguments])
        args_str = ", ".join([arg.declaration for arg in self.arguments])
        return "YEP_USE_DISPATCH_FUNCTION_SECTION YepStatus YEPABI {}({}) {{ return _{}({}); }}".format(self.name, args_str, self.name, args_names)


    def _separate_args_in_name(self, arg_str):
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


    def _parse_arg_types(self, args_arr, inputs, output):
        """
        Takes an array such as [IV64f, V64f] of inputs,
        an output string (such as V64f), and the arguments
        from the YAML file and creates the Argument objects
        for each argument
        """
        args_arr_ind = 0
        for i in inputs:
            is_const = "I" not in i and "S" not in i
            is_pointer = "S" not in i
            arg_type = self._parse_arg_type(i)
            self.arguments.append(Argument(arg_type, args_arr[args_arr_ind], is_pointer, is_const))
            args_arr_ind += 1

        # Check if we even have an output (the operation doesn't write to one of the sources)
        if "I" not in inputs[0]:
            arg_type = self._parse_arg_type(output)
            self.arguments.append(Argument(arg_type, args_arr[args_arr_ind], True, False))
            args_arr_ind += 1

        if args_arr_ind < len(args_arr):
            # There are more arguments after input / output, namely length
            for i in range(args_arr_ind,len(args_arr)):
                # These arguments have their types specified in the declaration string
                arg = args_arr[args_arr_ind].split(" ")
                self.arguments.append(Argument(arg[0], arg[1], False, False))


    def _parse_arg_type(self, arg_str):
        """
        This is a helper function which takes a Yeppp type found in the name
        (e.g V8s or IV16u) and returns the corresponding C type,
        ex. V8s -> Yep8s
        """
        if arg_str[0] == "V":
            # This is a const vector type
            return "Yep" + arg_str[1:]
        elif arg_str[0] == "S":
            # This is a regular scalar passed by value
            return "Yep" + arg_str[1:]
        elif arg_str[0] == "I":
            # This points to both one input and where the output is stored
            return "Yep" + arg_str[2:]


class ArgumentCheckGenerator:
    """
    Class responsible for generating the argument checks on the default
    implementations of functions, e.g checking that pointers are non-null
    and aligned
    """

    def __init__(self, arguments):
        self.arguments = arguments


    def generate_arg_checks(self):
        """
        Generate all argument checks for the arguments
        passed in at construction and return them as
        an array of strings
        """
        checks = []
        for arg in self.arguments:
            if arg.is_pointer:
                checks.append(self.generate_null_check(arg))
                if arg.size != "8" and arg.size != "":
                    checks.append(self.generate_align_check(arg))
        return checks


    def generate_null_check(self, arg):
        return """
  if YEP_UNLIKELY({} == YEP_NULL_POINTER) {{
    return YepStatusNullPointer;
  }}""".format(arg.name)


    def generate_align_check(self, arg):
        return """
  if YEP_UNLIKELY(yepBuiltin_GetPointerMisalignment({}, sizeof({})) != 0) {{
    return YepStatusMisalignedPointer;
  }}""".format(arg.name, arg.arg_type)


class Argument:
    """
    Represents an argument to a function.
    Used to generate declarations and default implementations
    """

    def __init__(self, arg_type, name, is_pointer, is_const):
        self.arg_type = arg_type
        self.name = name
        self.is_pointer = is_pointer
        self.is_const = is_const

    @property
    def arg_type(self):
        """
        This is the type of the argument with no qualifiers,
        and if it is a pointer, it is the type pointed to
        e.g const Yep8s *x -> Yep8s
        """
        return self.arg_type

    @property
    def full_arg_type(self):
        """
        This is the type of the argument including qualifiers
        like const, pointers etc.
        """
        ret = ""
        if self.is_const:
            ret += "const "
        ret += self.arg_type + " "
        if self.is_pointer:
            ret += "*YEP_RESTRICT "
        return ret


    @property
    def name(self):
        return self.name

    @property
    def is_pointer(self):
        return self.is_pointer

    @property
    def is_const(self):
        return self.is_const

    @property
    def declaration(self):
        """
        Returns the declaration needed in a C function
        """
        ret = ""
        if self.is_const:
            ret += "const "
        ret += self.arg_type + " "
        if self.is_pointer:
            ret += "*YEP_RESTRICT "
        ret += self.name
        return ret

    @property
    def size(self):
        """
        Get the size of the argument, e.g Yep8s -> 8.
        This is needed to generate the right alignment checks
        """
        ret = ""
        for c in self.arg_type:
            if c.isdigit():
                ret += c
        return ret




