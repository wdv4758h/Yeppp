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
