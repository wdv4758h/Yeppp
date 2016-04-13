from Argument import Argument
from DispatchTableGenerator import DispatchTableGenerator
from DefaultImplementationGenerator import DefaultImplementationGenerator
from UnitTestGenerator import UnitTestGenerator
import re


class Function:
    """
    Represents a particular specialization of a Yeppp function.
    Functions know how to generate their own declarations and
    default implementations
    """

    def __init__(self, func, func_group, has_asm_impl=False):
        """
        Initialize the function, setting the function name,
        its documentation, template for default implementation,
        and creating an array of Argument objects for the functions
        arguments
        :param func A dictionary from the spec file containing the declaration
        :param func_group The group the function is in: groups subsets of specific operations,
            e.g all Add functions which take a vector and a scalar and output a vector
        :param has_asm_impl Whether or not this function has an assembly implementation
            (used in generating dispatch tables)
        """
        self.yaml_declaration = func["declaration"] # e.g yepCore_Add_V8sV8s_V8s xPointer, yPointer, sumPointer, YepSize length
        self.java_documentation = func_group["java_documentation"]
        self.c_documentation = func_group["c_documentation"]
        self.default_impl_template = func_group["default_implementation_template"]

        # Parse the yaml declaration to gather info about the functions arguments and C decl
        self.name, self.op, args_str = self.yaml_declaration.partition(" ")
        name_parts = self.name.split("_") # Will be ['yepModule', 'Op', 'InputTypes', 'OutputType']
        input_types_encoded = self._separate_args_in_name(name_parts[2])
        output_type_encoded = self._separate_args_in_name(name_parts[3])

        args_arr = args_str.split(",")
        args_arr = [ a.lstrip().rstrip() for a in args_arr ]

        # self.arguments will be an array of Argument objects we will use to generate everything
        self.arguments = []
        self._parse_arg_types(args_arr, input_types_encoded, output_type_encoded)

        self.has_asm_impl = has_asm_impl
        self.dispatch_table_generator = DispatchTableGenerator(self.name, self.arguments)
        self.default_impl_generator = DefaultImplementationGenerator(self.name, self.arguments, self.default_impl_template)
        self.unit_test_generator = UnitTestGenerator(self.name, self.arguments)

    @property
    def c_documentation(self):
        """
        Get the C documentation for this function
        that is parsed from the YAML file
        """
        return self.c_documentation

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
        return self.default_impl_generator.generate_default_implementation()

    @property
    def default_impl_declaration(self):
        return self.default_impl_generator.generate_default_impl_declaration()

    @property
    def dispatch_table(self):
        return self.dispatch_table_generator.generate_dispatch_table()

    @property
    def dispatch_table_declaration(self):
        return self.dispatch_table_generator.generate_dispatch_table_declaration()

    @property
    def dispatch_stub(self):
        return self.dispatch_table_generator.generate_dispatch_stub()

    @property
    def function_pointer_declaration(self):
        return self.dispatch_table_generator.generate_function_pointer_declaration()

    @property
    def function_pointer_definition(self):
        return self.dispatch_table_generator.generate_function_pointer_definition()

    @property
    def unit_test(self):
        return self.unit_test_generator.generate_unit_test()


    def _separate_args_in_name(self, arg_str):
        """
        Given a string such as IV64fV64f, it separates them into
        two and returns a list, e.g [IV64f, V64f] in this case
        """
        # Simply search for the first lowercase character and this is the split point.
        # This should maybe be replaced by something in the python standard library
        splits = []
        base = 0
        for (i,c) in enumerate(arg_str):
            if c.islower():
                splits.append(arg_str[base:i + 1])
                base = i + 1
        return splits

    def _parse_arg_types(self, args_arr, inputs, outputs):
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
        has_output = reduce(lambda x, y: x or not "I" in y, outputs, False)
        if has_output:
            for output in outputs:
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
