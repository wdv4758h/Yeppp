class DispatchTableGenerator:
    """
    Class for generating the relevant parts of the dispatch table
    for a function, i.e the table itself, the declaration for headers,
    the function pointers filled in by the table, and the stub
    the user calls
    Used by Function class
    """

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def generate_dispatch_table(self):
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
        ret += "    YEP_DESCRIBE_FUNCTION_IMPLEMENTATION(_{}_Default,\
        YepIsaFeaturesDefault, YepSimdFeaturesDefault, YepSystemFeaturesDefault,\
        YepCpuMicroarchitectureUnknown, \"c++\", \"Naive\", \"None\")\n}};".format(self.name)
        return ret

    def generate_dispatch_table_declaration(self):
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

    def generate_function_pointer_definition(self):
        """
        Define the pointer to this function and set it to null
        """
        return "YEP_USE_DISPATCH_POINTER_SECTION YepStatus (YEPABI*_{})({}) = YEP_NULL_POINTER;".format(self.name, ", ".join([arg.full_arg_type for arg in self.arguments]))

    def generate_function_pointer_declaration(self):
        """
        Declare the function pointer to this function
        """
        return "extern \"C\" YEP_PRIVATE_SYMBOL YepStatus (YEPABI* _{})({});".format(self.name,
                ', '.join([arg.declaration for arg in self.arguments]))

    def generate_dispatch_stub(self):
        """
        Generate the stub which the user calls which just redirects
        to the function pointer set from the dispatch initialization
        """
        args_names = ", ".join([arg.name for arg in self.arguments])
        args_str = ", ".join([arg.declaration for arg in self.arguments])
        return "YEP_USE_DISPATCH_FUNCTION_SECTION YepStatus YEPABI {}({}) {{ return _{}({}); }}".format(self.name, args_str, self.name, args_names)

