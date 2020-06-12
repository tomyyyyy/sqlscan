from lib.request.injection_point import injection_point
from lib.output.output import Output
import sys


class Controller(object):
    def __init__(self, script_path, arguments, output):
        self.script_path = script_path
        self.exit = False
        self.arguments = arguments
        self.output = output

        if self.arguments.options.url != None:
            injection_point(self.arguments).judge_inject()
        else:
            self.output.warining("must support url parameters")
            sys.exit(0)

        

