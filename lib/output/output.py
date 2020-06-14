from colorama import init, Fore, Back, Style
import datetime


class Output(object):
    def __init__(self):
        self.color = Colored()

    def warning(self, data):
        # 用蓝色显示当前时间
        time = str(datetime.datetime.now())[11:19]
        print(self.color.white("["), end="")
        print(self.color.blue(time), end="")
        print(self.color.white("]"), end=" ")
        # 用红色显示报告类型
        print(self.color.white("["), end="")
        print(self.color.red("warning"), end="")
        print(self.color.white("]"), end=" ")
        # 显示详细内容
        print(self.color.white(data))
    
    def error(self, data):
        # 用红色显示当前时间
        time = str(datetime.datetime.now())[11:19]
        print(self.color.white("["), end="")
        print(self.color.red(time), end="")
        print(self.color.white("]"), end=" ")
        # 用红色显示报告类型
        print(self.color.white("["), end="")
        print(self.color.red("error"), end="")
        print(self.color.white("]"), end=" ")
        # 显示详细内容
        print(self.color.red(data))

    def info(self, data):
        # 用蓝色显示当前时间
        time = str(datetime.datetime.now())[11:19]
        print(self.color.white("["), end="")
        print(self.color.blue(time), end="")
        print(self.color.white("]"), end=" ")
        # 用红色显示报告类型
        print(self.color.white("["), end="")
        print(self.color.yellow("info"), end="")
        print(self.color.white("]"), end=" ")
        # 显示详细内容
        print(self.color.white(data))

    def info_inject(self, data):
        # 用蓝色显示当前时间
        time = str(datetime.datetime.now())[11:19]
        print(self.color.white("["), end="")
        print(self.color.blue(time), end="")
        print(self.color.white("]"), end=" ")
        # 用红色显示报告类型
        print(self.color.white("["), end="")
        print(self.color.yellow("info"), end="")
        print(self.color.white("]"), end=" ")
        # 显示详细内容
        print(self.color.white("the parameter"), end=" ")
        print(self.color.yellow(data), end=" ")
        print(self.color.white("appears to be SQLi vulnerable"))
        

    def ending(self):
        # 用蓝色显示当前时间
        time=str(datetime.datetime.now())[:19]
        print("[*] ending @ ", end="")
        print(self.color.white(time))

    def start(self, version, url, threads):
        print(self.color.yellow("Version:"), end=" ")
        print(self.color.blue(version), end=" ")
        print(self.color.white("|"), end=" ")
        print(self.color.yellow("Target:"), end=" ")
        print(self.color.blue(url), end=" ")
        print(self.color.white("|"), end=" ")
        print(self.color.yellow("threads:"), end=" ")
        print(self.color.blue(threads), end=" ")
        print()


class Colored(object):
    def __init__(self):
        pass
    # 前景色:红色 背景色:默认
    def red(self, s):
        return Fore.RED + s + Fore.RESET

    # 前景色:绿色 背景色:默认
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    # 前景色:蓝色 背景色:默认
    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET

    # 前景色:黄色 背景色:默认
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    # 前景色:青色 背景色:默认
    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET

    # 前景色:白色 背景色:默认
    def white(self, s):
        return Fore.WHITE + s + Fore.RESET

    # 前景色:黑色 背景色:默认
    def black(self, s):
        return Fore.BLACK

