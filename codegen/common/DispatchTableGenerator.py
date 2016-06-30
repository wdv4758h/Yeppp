class DispatchTableGenerator:
    """
    Class for generating the relevant parts of the dispatch table
    for a function, i.e the table itself, the declaration for headers,
    the function pointers filled in by the table, and the stub
    the user calls
    Used by Function class
    """

    x86_64_SIMD_EXTENSIONS = {
        "Nehalem"       : ["YepX86SimdFeatureSSE", "YepX86SimdFeatureSSE2"],
        "SandyBridge"   : ["YepX86SimdFeatureAVX"],
        "Haswell"       : ["YepX86SimdFeatureAVX2", "YepX86SimdFeatureAVX"]
    }

    x86_64_SYSTEM_FEATURES = {
        ("Nehalem", "Microsoft")                      : ["YepX86SystemFeatureXMM"],
        ("SandyBridge", "Microsoft")                  : ["YepX86SystemFeatureYMM"],
        ("Haswell", "Microsoft")                      : ["YepX86SystemFeatureYMM"],
        ("Nehalem", "SystemV x86-64 ABI")             : ["YepX86SystemFeatureXMM"],
        ("SandyBridge", "SystemV x86-64 ABI")         : ["YepX86SystemFeatureYMM"],
        ("Haswell", "SystemV x86-64 ABI")             : ["YepX86SystemFeatureYMM"]
    }

    DISPATCH_TABLE_TEMPLATE = \
    """
YEP_USE_DISPATCH_TABLE_SECTION
const FunctionDescriptor<YepStatus (YEPABI*)({args})> _dispatchTable_{name}[] = {{
    {table}
}};
    """

    DISPATCH_TABLE_ENTRY_TEMPLATE = \
    """
    YEP_DESCRIBE_FUNCTION_IMPLEMENTATION({symbol}, {isafeats}, {simdfeats}, {systemfeats}, YepCpuMicroarchitecture{microarch}, {lang}, {descriptor}, {final})
    """

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def generate_dispatch_table(self, asm_impl_metadata):
        descriptors = []
        for data in asm_impl_metadata:
            arch = data["uarch"]
            descriptors.append(
                    DispatchTableGenerator.DISPATCH_TABLE_ENTRY_TEMPLATE.format(
                        symbol=data["symbol"],
                        isafeats="YepIsaFeaturesDefault",
                        simdfeats=' | '.join(DispatchTableGenerator.x86_64_SIMD_EXTENSIONS[arch]),
                        systemfeats=' | '.join(DispatchTableGenerator.x86_64_SYSTEM_FEATURES[arch, data["abi"]]),
                        microarch=arch,
                        lang="\"asm\"",
                        descriptor="YEP_NULL_POINTER",
                        final="YEP_NULL_POINTER"
                    )
            )

        # Now add the default impl
        descriptors.append(
                    DispatchTableGenerator.DISPATCH_TABLE_ENTRY_TEMPLATE.format(
                        symbol="_{}_Default".format(self.name),
                        isafeats="YepIsaFeaturesDefault",
                        simdfeats="YepSimdFeaturesDefault",
                        systemfeats="YepSystemFeaturesDefault",
                        microarch="Unknown",
                        lang="\"c++\"",
                        descriptor="\"Naive\"",
                        final="\"None\""
                    )
        )

        table = DispatchTableGenerator.DISPATCH_TABLE_TEMPLATE.format(
                        args=', '.join([ arg.full_arg_type for arg in self.arguments ]),
                        name=self.name,
                        table=', '.join(descriptors)
                )

        return table

    def generate_dispatch_table_declaration(self):
        """
        Generate the declaration of the dispatch table for the header
        """
        return "extern \"C\" YEP_PRIVATE_SYMBOL const FunctionDescriptor<YepStatus (YEPABI*)({args})> _dispatchTable_{name}[];".format(
                args=', '.join([ arg.full_arg_type for arg in self.arguments ]),
                name=self.name
        )

    def generate_function_pointer_definition(self):
        """
        Define the pointer to this function and set it to null
        """
        return "YEP_USE_DISPATCH_POINTER_SECTION YepStatus (YEPABI*_{name})({args}) = YEP_NULL_POINTER;".format(
                name=self.name,
                args=', '.join([ arg.full_arg_type for arg in self.arguments ])
        )

    def generate_function_pointer_declaration(self):
        """
        Declare the function pointer to this function
        """
        return "extern \"C\" YEP_PRIVATE_SYMBOL YepStatus (YEPABI* _{name})({args});".format(
                name=self.name,
                args=', '.join([ arg.declaration for arg in self.arguments ])
        )

    def generate_dispatch_stub(self):
        """
        Generate the stub which the user calls which just redirects
        to the function pointer set from the dispatch initialization
        """
        return "YEP_USE_DISPATCH_FUNCTION_SECTION YepStatus YEPABI {name}({args}) {{ return _{name}({argnames}); }}".format(
                name=self.name,
                args=', '.join([ arg.declaration for arg in self.arguments ]),
                argnames=', '.join([ arg.name for arg in self.arguments ])
        )

