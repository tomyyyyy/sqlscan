from socket import gethostbyname
from urllib.parse import urljoin, urlparse
from helptxt import ArgumentParser

import pyfiglet
import os


def banner():
    ascii_banner = pyfiglet.figlet_format("SQLscan")
    print(ascii_banner)


class Sqlscan():
    def __init__(self):
        self.script_path = (os.path.dirname(os.path.realpath(__file__)))
        self.arguments = ArgumentParser(self.script_path)

if __name__ == "__main__":
    
    url = 'https://www.baidu.com'
    banner()
    main = Sqlscan()
