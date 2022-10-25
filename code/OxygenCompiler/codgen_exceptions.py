E_UNKNOWN_LABEL = " unknown label: "

class CodeGenError(Exception):
    def __init__(self, message, line=-1, extra=""):
        self.base = "Code generation error: "
        self.line = line
        self.extra = extra

        super().__init__(self.base + message + line.__repr__())

        if line != -1:
            self.message = self.base + message + line.__repr__() + self.extra
        else:
            self.message = self.base + message

    def __repr__(self):
        return self.message

    def get_err_repr(self):
        err = self.__repr__() + '\n'
        lin = str(self.line)

        return err + lin + "\nline"

    @staticmethod
    def form_errors_array(errors_array):

        ret = []
        l = len(errors_array)

        for err in errors_array:
            ret += [err.get_err_repr()]

        return ret, l