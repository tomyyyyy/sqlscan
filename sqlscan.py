from lib.output.helptxt import ArgumentParser
from lib.output.output import Output
from lib.output.CLIOutput import Clioutput
from lib.core.controller import Controller

import os

class Sqlscan():
    def __init__(self):
        self.script_path = (os.path.dirname(os.path.realpath(__file__)))
        self.arguments = ArgumentParser(self.script_path)
        self.output = Clioutput()
        self.controller = Controller(self.script_path, self.arguments, self.output)

if __name__ == "__main__":
    main = Sqlscan()
