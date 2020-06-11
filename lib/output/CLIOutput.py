
from colorama import *
from lib.output.output import Colored, Output

import pyfiglet
import os

Version = "1.0"

class Clioutput():
    def __init__(self,arguments):
        self.arguments = arguments
        self.banner()

    def banner(self):
        ascii_banner = pyfiglet.figlet_format("SQLscan")
        color = Colored()
        print(color.green(ascii_banner))
        Output().start(Version,self.arguments.options.url,"*")
        print()
