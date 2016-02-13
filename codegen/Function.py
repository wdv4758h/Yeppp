from string_template import StringTemplate

class Function:

    def __init__(self, func, func_group):
        self.declaration = func["declaration"]
        self.java_documentation = func_group["java_documentation"]
        self.c_documentation = func_group["c_documentation"]
        self.default_impl_template = func_group["default_implementation_template"]
        self._parse_declaration()


    @property
    def c_declaration(self):
        # Write the function return type
        c_declaration += "YEP_PUBLIC_SYMBOL enum YepStatus YEPABI "

        # Parse the declaration passed in for its parameter names and types
        c_declaration += self.name + "("

        # Parse and write the declaration for the input args
        for i,arg in enumerate(self.arguments):
            c_declaration += arg.decl_str()
            if i != len(self.arguments) - 1:
                c_declaration += ", "
        c_declaration += ");"
        return c_declaration


    @property
    def default_implementation(self):
        # Write the declaration
        default_impl = "extern \"C\" YEP_LOCAL_SYMBOL YepStatus _{}_Default(".format(self.name)
        for i,arg in enumerate(self.arguments):
            default_impl += arg.declaration
            if i != len(self.arguments) - 1:
                default_impl += ", "
        default_impl += ") {\n"

        # Generate null pointer, alignment checks
        arg_checker = ArgumentCheckGenerator(self.arguments)
        checks = arg_checker.generate_arg_checks()
        for check in checks:
            default_impl += check
        default_impl += "\n"

        # Write the body of the implementation
        template = StringTemplate(self.default_impl_template)
        body = template.eval_template({ x.name: x for x in self.arguments })
        default_impl += "    "
        for i,c in enumerate(body):
            default_impl += c
            if c == "\n" and i != len(body) - 1:
                default_impl += "    "
        default_impl += "}\n"
        return default_impl


    @property
    def c_documentation(self):
        return self.c_documentation



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


    def _parse_declaration(self):
        self.name, _, args_str = self.declaration.partition(" ")
        name_parts = self.name.split("_") # Will be ['yepModule', 'Op', 'InputTypes', 'OutputType']
        input_types_encoded = self._separate_args_in_name(name_parts[2])
        output_type_encoded = name_parts[3]

        args_arr = args_str.split(",")
        args_arr = [ a.lstrip().rstrip() for a in args_arr ]

        self._parse_arg_types(args_arr, input_types_encoded, output_type_encoded)


    def _parse_arg_types(self, args_arr, inputs, output):
        self.arguments = []
        args_arr_ind = 0
        for i in inputs:
            is_const = "I" not in i
            is_pointer = "S" not in i
            arg_type = self._parse_arg_type(i)
            self.arguments.append(Argument(arg_type, args_arr[args_arr_ind], is_pointer, is_const))
            args_arr_ind += 1

        if "I" not in inputs[0]:
            arg_type = self._parse_arg_type(output)
            self.arguments.append(Argument(arg_type, args_arr[args_arr_ind], True, False))
            args_arr_ind += 1

        if args_arr_ind < len(args_arr):
            # There are more arguments after input / output, probably length
            for i in range(args_arr_ind,len(args_arr)):
                arg = args_arr[args_arr_ind].split(" ")
                self.arguments.append(Argument(arg[0], arg[1], False, False))


    def _parse_arg_type(self, arg_str):
        """
        This is a helper function which takes a Yeppp type found in the name
        (e.g V8s or IV16u) and returns the corresponding C type,
        ex. V8s -> const Yep8s *YEP_RESTRICT
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

    def __init__(self, arguments):
        self.arguments = arguments


    def generate_arg_checks(self):
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

    def __init__(self, arg_type, name, is_pointer, is_const):
        self.arg_type = arg_type
        self.name = name
        self.is_pointer = is_pointer
        self.is_const = is_const

    @property
    def arg_type(self):
        return self.arg_type

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
        ret = ""
        for c in self.arg_type:
            if c.isdigit():
                ret += c
        return ret




