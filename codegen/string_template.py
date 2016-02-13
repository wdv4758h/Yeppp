class StringTemplate:
    """
    Input a string with python commands and text.
    The commands will be evaluated and substituted
    into the resulting text.
    Include ${expr} to have what is inside {} be evaluated.
    E.x: "Hello ${"world" if True else "WORLD"}" becomes "Hello world"
    Assumes that ${ always begins something that needs to be evaluated,
    closed off by the next } it sees.
    """

    def __init__(self, template):
        self.template = template

    def eval_template(self, args):
        """
        Evaluates the template and returns the appropriate string.
        If the string is ill-formed it returns the empty string.
        """
        ret = ""
        eval_str = ""
        in_template = False
        for i,c in enumerate(self.template):
            if c == "{": continue
            if c == "$" and not in_template:
                in_template = True
                if self.template[i+1] != "{":
                    return ""
            elif in_template and c == "}":
                in_template = False
                ret += str(eval(eval_str, args))
                eval_str = ""
            elif in_template:
                eval_str += c
            else:
                ret += c
        if in_template:
            # We shouldn't be parsing an expression after exiting the loop
            return ""
        return ret
