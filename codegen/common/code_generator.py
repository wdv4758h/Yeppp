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

bounds =                        {'Yep8u' : ("0u", "255u"),
                                 'Yep16u': ("0u", "65535u"),
                                 'Yep32u': ("0u", "4294967295u"),
                                 'Yep64u': ("0ull", "18446744073709551615ull"),
                                 'Yep8s' : ("-128", "127"),
                                 'Yep16s': ("-32768", "32767"),
                                 'Yep32s': ("-2147483648", "2147483647"),
                                 'Yep64s': ("-92233720368547758ll", "9223372036854775807ll"),
                                 'Yep32f': ("-1.0f", "1.0f"),
                                 'Yep64f': ("-1.0", "1.0")}


class CodeGenerator(object):
    def __init__(self, use_tabs=False):
        self.indentationLevel = 0
        self.use_tabs = use_tabs
        self.code = []

    def indent(self):
        self.indentationLevel += 1
        return self

    def dedent(self):
        self.indentationLevel -= 1
        return self

    def add_line(self, string='', indent=None):
        if indent == None:
            indent = self.indentationLevel
        elif indent < 0:
            indent += self.indentationLevel
        if string == '':
            self.code.append(string)
        else:
            if self.use_tabs:
                self.code.append("\t" * indent + string)
            else:
                self.code.append("    " * indent + string)
        return self

    def add_lines(self, lines, indent=None):
        for line in lines:
            self.add_line(line, indent)

    def add_empty_lines(self, count):
        for i in range(count):
            self.add_line()
        return self

    def add_c_comment(self, lines, doxygen=False):
        if isinstance(lines, str) and lines.find("\n") != -1:
            lines = lines.split("\n")
        if isinstance(lines, list) and len(lines) > 1:
            if doxygen:
                self.add_line("/**")
            else:
                self.add_line("/*")
            for line in lines:
                self.add_line(" * " + line)
            self.add_line(" */")
        else:
            line = lines[0] if isinstance(lines, list) else str(lines)
            if doxygen:
                self.add_line("/** " + line + "*/")
            else:
                self.add_line("/* " + line + "*/")

    def add_assembly_comment(self, lines, indent=None):
        for line in lines:
            self.add_line("; " + line, indent)

    def add_fortran90_comment(self, lines, doxygen=False):
        if isinstance(lines, str) and lines.find("\n") != -1:
            lines = lines.split("\n")
        elif isinstance(lines, str):
            lines = [lines]
        for index, line in enumerate(lines):
            if doxygen:
                if index == 0:
                    self.add_line("!> " + line)
                else:
                    self.add_line("!! " + line)
            else:
                self.add_line("! " + line)

    def add_csharp_comment(self, lines, doxygen=False):
        if isinstance(lines, str) and lines.find("\n") != -1:
            lines = lines.split("\n")
        if isinstance(lines, list) and len(lines) > 1:
            if not doxygen:
                self.add_line("/*")
            for line in lines:
                if doxygen:
                    self.add_line("/// " + line)
                else:
                    self.add_line(" * " + line)
            if not doxygen:
                self.add_line(" */")
        else:
            line = lines[0] if isinstance(lines, list) else str(lines)
            if doxygen:
                self.add_line("/// " + line)
            else:
                self.add_line("// " + line)

    def get_code(self):
        return "\n".join(self.code)
