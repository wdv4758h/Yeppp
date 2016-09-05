from code_generator import *

class BenchmarkGenerator:
    """
    Class responsible for generating benchmarks of the different functions.
    """

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.input_arrs = [ arg for arg in self.arguments if arg.is_pointer and arg.is_const ]
        self.output = [ arg for arg in self.arguments if arg.is_pointer and not arg.is_const ][0]

    def generate_benchmark(self):
        benchgen = CodeGenerator()
        self._benchmark_signature(benchgen)
        self._init_rng(benchgen)
        benchgen.add_line()
        self._find_default_impl(benchgen)
        benchgen.add_line()
        self._init_arguments(benchgen)
        benchgen.add_line()
        self._bench_default_impl(benchgen)
        benchgen.add_line()
        self._begin_implementation_loop(benchgen)
        self._implementation_loop_body(benchgen)
        benchgen.dedent().add_line("}")
        return benchgen.get_code()

    def _benchmark_signature(self, benchgen):
        benchgen.add_line("static void Benchmark_{0}(Yep64u supportedIsaFeatures, Yep64u supportedSimdFeatures, Yep64u supportedSystemFeatures) {{".format(self._name_without_module())).indent()

    def _init_rng(self, benchgen):
        benchgen.add_line("YepRandom_WELL1024a rng;")
        benchgen.add_line("YepStatus status = yepRandom_WELL1024a_Init(&rng);")
        benchgen.add_line("assert(status == YepStatusOk);")

    def _find_default_impl(self, benchgen):
        benchgen.add_line("typedef YepStatus (YEPABI* FunctionPointer)({0});".format(
            ", ".join([arg.full_arg_type for arg in self.arguments])))
        benchgen.add_line("typedef const FunctionDescriptor<FunctionPointer>* DescriptorPointer;")
        benchgen.add_line("const DescriptorPointer defaultDescriptor = findDefaultDescriptor(_dispatchTable_{0});".format(self.name))
        benchgen.add_line("const FunctionPointer defaultImplementation = defaultDescriptor->function;")
        benchgen.add_line("Yep32s failedTests = 0;")

    def _init_arguments(self, benchgen):
        benchgen.add_line("YepSize length = 100000;")
        for arg in self.arguments:
            if arg.is_pointer:
                benchgen.add_line("YEP_ALIGN(64) {0} {1}[length];".format(
                    arg.arg_type, arg.name))
                if arg.name == self.output.name: continue
                benchgen.add_line("status = {0}(&rng, {1}, {2}, YEP_COUNT_OF({2}));".format(
                    random_generator_function_map[arg.arg_type], ", ".join(bounds[arg.arg_type]), arg.name))
            elif arg.arg_type != "YepSize":
                benchgen.add_line("{} {};".format(arg.arg_type, arg.name))
                benchgen.add_line("status = {0}(&rng, {1}, &{2}, 1);".format(
                    random_generator_function_map[arg.arg_type], ", ".join(bounds[arg.arg_type]), arg.name))
                benchgen.add_line("assert(status == YepStatusOk);")

    def _bench_default_impl(self, benchgen):
        benchgen.add_line("Yep64u startTicks, endTicks;")
        benchgen.add_line("yepLibrary_GetTimerTicks(&startTicks);")
        benchgen.add_line("defaultImplementation({});".format(", ".join(arg.name for arg in self.arguments)))
        benchgen.add_line("yepLibrary_GetTimerTicks(&endTicks);")
        benchgen.add_line("reportBenchmark(\"{}\", \"Default\", startTicks, endTicks);".format(self.name))
    
    def _begin_implementation_loop(self, benchgen):
        benchgen.add_line("for (DescriptorPointer descriptor = &_dispatchTable_{0}[0]; \
descriptor != defaultDescriptor; descriptor++) {{".format(self.name)).indent()
        benchgen.add_line("const Yep64u unsupportedRequiredFeatures = (descriptor->isaFeatures & ~supportedIsaFeatures) |")
        benchgen.add_line("\t(descriptor->simdFeatures & ~supportedSimdFeatures) |")
        benchgen.add_line("\t(descriptor->systemFeatures & ~supportedSystemFeatures);")
        benchgen.add_line("if (unsupportedRequiredFeatures == 0) {").indent()

    def _implementation_loop_body(self, benchgen):
        benchgen.add_line("yepLibrary_GetTimerTicks(&startTicks);")
        benchgen.add_line("status = descriptor->function({});".format(", ".join(arg.name for arg in self.arguments)))
        benchgen.add_line("yepLibrary_GetTimerTicks(&endTicks);")
        benchgen.add_line("reportBenchmark(\"{}\", getMicroarchitectureName(descriptor->microarchitecture), startTicks, endTicks);".format(self.name))
        benchgen.dedent().add_line("}").dedent().add_line("}")

    def _name_without_module(self):
        """
        Takes a name like yepCore_Add_V16sV16s_V16s and
        returns Add_V16sV16s_V16s
        """
        return "_".join(self.name.split("_")[1:])
