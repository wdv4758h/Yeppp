from code_generator import CodeGenerator

random_generator_function_map = {'Yep8u' : 'yepRandom_WELL1024a_GenerateDiscreteUniform_S8uS8u_V8u',
                                 'Yep16u': 'yepRandom_WELL1024a_GenerateDiscreteUniform_S16uS16u_V16u',
                                 'Yep32u': 'yepRandom_WELL1024a_GenerateDiscreteUniform_S32uS32u_V32u',
                                 'Yep64u': 'yepRandom_WELL1024a_GenerateDiscreteUniform_S64uS64u_V64u',
                                 'Yep8s' : 'yepRandom_WELL1024a_GenerateDiscreteUniform_S8sS8s_V8s',
                                 'Yep16s': 'yepRandom_WELL1024a_GenerateDiscreteUniform_S16sS16s_V16s',
                                 'Yep32s': 'yepRandom_WELL1024a_GenerateDiscreteUniform_S32sS32s_V32s',
                                 'Yep64s': 'yepRandom_WELL1024a_GenerateDiscreteUniform_S64sS64s_V64s',
                                 'Yep32f': 'yepRandom_WELL1024a_GenerateUniform_S32fS32f_V32f_Acc32',
                                 'Yep64f': 'yepRandom_WELL1024a_GenerateUniform_S64fS64f_V64f_Acc64'}

class UnitTestGenerator:
    """
    Class responsible for generating all unit tests for a function.
    Used by Function class
    """

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.inputs_arrs = [ arg for arg in self.arguments if arg.is_pointer and arg.is_const ]
        self.output = [ arg for arg in self.arguments if not arg.arg_type == "YepSize" and not arg.is_const ][0]

    def generate_unit_test(self):
        """
        Generate the CPP unit test for this function
        """
        utg = CodeGenerator()
        # Generate definition, rng setup, etc.
        self._unit_test_signature(utg)
        self._init_rng(utg)
        utg.add_line()
        self._find_default_impl(utg)
        utg.add_line()
        self._init_arguments(utg)
        utg.add_line()
        self._begin_implementation_loop(utg)
        self._begin_argument_loops(utg)
        self._argument_loop_body(utg)
        utg.add_line("for (YepSize length = 1024; length < 1088; length++) {").indent()
        self._argument_loop_body(utg)
        utg.dedent()

        indent_depth = len([ arg for arg in self.arguments if arg.is_pointer ])
        for i in range(indent_depth):
            utg.add_line("}").dedent()
        self._passed_or_skipped(utg)

        utg.add_line("next_descriptor:")
        utg.add_line("continue;")
        utg.dedent().add_line("}")
        utg.add_line("return -failedTests;")
        utg.dedent().add_line("}")
        return utg.get_code()

    def _unit_test_signature(self, utg):
        utg.add_line("static Yep32s Test_{0}(Yep64u supportedIsaFeatures, Yep64u supportedSimdFeatures, Yep64u supportedSystemFeatures) {{".format(self._name_without_module())).indent()

    def _init_rng(self, utg):
        utg.add_line("YepRandom_WELL1024a rng;")
        utg.add_line("YepStatus status = yepRandom_WELL1024a_Init(&rng);")
        utg.add_line("assert(status == YepStatusOk);")

    def _find_default_impl(self, utg):
        utg.add_line("typedef YepStatus (YEPABI* FunctionPointer)({0});".format(
            ", ".join([arg.full_arg_type for arg in self.arguments])))
        utg.add_line("typedef const FunctionDescriptor<FunctionPointer>* DescriptorPointer;")
        utg.add_line("const DescriptorPointer defaultDescriptor = findDefaultDescriptor(_dispatchTable_{0});".format(self.name))
        utg.add_line("const FunctionPointer defaultImplementation = defaultDescriptor->function;")
        utg.add_line("Yep32s failedTests = 0;")

    def _init_arguments(self, utg):
        for arg in self.arguments:
            if arg.is_pointer:
                utg.add_line("YEP_ALIGN(64) {0} {1}Array[1088 + (64 / sizeof({0}))];".format(
                    arg.arg_type, arg.name))
                if arg.name == self.output.name: continue # We don't want to initialize the output array here, only the init array below
                # TODO FIX THIS LINE!!!
                utg.add_line("status = {0}(&rng, {1}, {2}, YEP_COUNT_OF({2}));".format(
                    random_generator_function_map[arg.arg_type], ", ".join(["-128", "127"]), arg.name))
                utg.add_line("assert(status == YepStatusOk);")
            elif arg.arg_type != "YepSize":
                utg.add_line("{} {};".format(arg.arg_type, arg.name))
                # TODO FIX THIS LINE!!!
                utg.add_line("status = {0}(&rng, {1}, &{2}, 1);".format(
                    random_generator_function_map[arg.arg_type], ", ".join(["-128", "127"]), arg.name))
                utg.add_line("assert(status == YepStatusOk);")
        # Initial arrays and reference arrays:
        if self.output.is_pointer: # Output is an array (not max, min, etc.)
            utg.add_line("YEP_ALIGN(64) {0} {1}InitArray[1088 + (64 / sizeof({0}))];".format(self.output.arg_type, self.output.name))
            utg.add_line("YEP_ALIGN(64) {0} {1}RefArray[1088 + (64 / sizeof({0}))];".format(self.output.arg_type, self.output.name))
            utg.add_line("status = {0}(&rng, {1}, {2}InitArray, YEP_COUNT_OF({2}));".format(
                random_generator_function_map[self.output.arg_type], ", ".join(["-128", "127"]), self.output.name))

    def _begin_implementation_loop(self, utg):
        utg.add_line("for (DescriptorPointer descriptor = &_dispatchTable_{0}[0]; \
descriptor != defaultDescriptor; descriptor++) {{".format(self.name)).indent()
        utg.add_line("const Yep64u unsupportedRequiredFeatures = (descriptor->isaFeatures & ~supportedIsaFeatures) |")
        utg.add_line("\t(descriptor->simdFeatures & ~supportedSimdFeatures) |")
        utg.add_line("\t(descriptor->systemFeatures & ~supportedSystemFeatures);")
        utg.add_line("if (unsupportedRequiredFeatures == 0) {").indent()

    def _begin_argument_loops(self, utg):
        for arg in self.arguments:
            if arg.is_pointer:
                utg.add_line("for (YepSize {0}Offset = 0; {0}Offset < 64 / sizeof({1}); {0}Offset++) {{".format(
                    arg.name, arg.arg_type)).indent()
            elif arg.arg_type == "YepSize": # is the length argument
                utg.add_line("for (YepSize length = 0; length < 64; length++) {").indent()

    def _argument_loop_body(self, utg):
        inputs = [ arg for arg in self.arguments if arg.is_const ]
        output = [ arg for arg in self.arguments if not arg.is_const and not arg.arg_type == "YepSize" ][0]

        utg.add_line("memcpy({0}RefArray, {0}InitArray, sizeof({0}RefArray));".format(self.output.name))

        utg.add_line("status = defaultImplementation({});".format(", ".join(self._determine_func_call_args(True))))
        utg.add_line("assert(status == YepStatusOk);")
        utg.add_line()

        utg.add_line("memcpy({0}Array, {0}InitArray, sizeof({0}Array));".format(self.output.name))
        utg.add_line("status = descriptor->function({});".format(", ".join(self._determine_func_call_args(False))))
        utg.add_line("if (memcmp({0}Array, {0}RefArray, sizeof({0}Array)) != 0) {{".format(self.output.name)).indent()
        utg.add_line("failedTests++;")
        utg.add_line("reportFailedTest(\"{}\", descriptor->microarchitecture);".format(self.name))
        utg.add_line("goto next_descriptor;")
        utg.dedent().add_line("}").dedent().add_line("}")

    def _determine_func_call_args(self, is_default_impl_call):
        call_args = []
        for arg in self.arguments:
            if arg.is_pointer:
                if arg.is_const:
                    call_args.append("&{0}Array[{0}Offset]".format(arg.name))
                else:
                    extra_part = "Ref" if is_default_impl_call else ""
                    call_args.append("&{0}{1}Array[{0}Offset]".format(arg.name, extra_part))
            else:
                call_args.append(arg.name)
        return call_args

    def _passed_or_skipped(self, utg):
        utg.add_line("reportPassedTest(\"{}\", descriptor->microarchitecture);".format(self.name))
        utg.dedent().add_line("} else {").indent()
        utg.add_line("reportSkippedTest(\"{}\", descriptor->microarchitecture);".format(self.name))
        utg.dedent().add_line("}")

    def _name_without_module(self):
        """
        Takes a name like yepCore_Add_V16sV16s_V16s and
        returns Add_V16sV16s_V16s
        """
        return "_".join(self.name.split("_")[1:])
