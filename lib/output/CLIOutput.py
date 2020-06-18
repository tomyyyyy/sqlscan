
from colorama import *
from lib.output.output import Colored, Output

import pyfiglet
import os,sys

Version = "1.1.0"

class Clioutput():
    def __init__(self,arguments):
        self.arguments = arguments
        self.output = Output()
        self.script_path = arguments.script_path
        self.banner()
        

    def banner(self):
        ascii_banner = pyfiglet.figlet_format("SQLscan")
        color = Colored()
        print(color.green(ascii_banner))
        if self.arguments.options.url == None:
            self.output.warning("must support url parameters")
            sys.exit(0)

        self.output.start(Version,self.arguments.options.url,"*")
        print()
        if not os.path.join(self.script_path,'lib','database','data'):
            os.makedirs(os.path.join(self.script_path,'lib','database','data'))
        
        


