from string_template import StringTemplate

class DefaultImplementationGenerator:
    """
    Class responsible for generating default implementation
    function bodies and declarations.
    Used by Function class
    """

    def __init__(self, name, arguments, template):
        self.name = name
        self.arguments = arguments
        self.default_impl_template = template

    def generate_default_implementation(self):
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

    def generate_default_impl_declaration(self):
        """
        Get the C declaration for the default implementation of this function
        """
        return "extern \"C\" YEP_LOCAL_SYMBOL YepStatus YEPABI _{}_Default({});".format(
                self.name,
                ", ".join([arg.declaration for arg in self.arguments]))


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


