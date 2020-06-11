
from colorama import *
from lib.output.output import Colored, Output

import pyfiglet
import os


class Clioutput():
    def __init__(self):
        self.banner()

    def banner(self):
        ascii_banner = pyfiglet.figlet_format("SQLscan")
        color = Colored()
        print(color.green(ascii_banner))
        url="http://www.baidu.com"
        version = "1.0"
        Output().start(version,url,"*")
        print()
