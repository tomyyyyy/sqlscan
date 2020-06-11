


class Controller(object):
    def __init__(self, script_path, arguments, output):
        self.script_path = script_path
        self.exit = False
        self.arguments = arguments
        self.output = output

