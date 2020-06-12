# coding = utf-8

from optparse import OptionParser
from optparse import OptionGroup



class ArgumentParser(object):

    def __init__(self, script_path):
        self.script_path = script_path
        self.parseConfig()
        self.options = self.parseArguments()

    def parseConfig(self):
        pass

       
    def parseArguments(self):
        usage = 'Usage: %prog [options] arg1 arg2 ...'

        parser = OptionParser(usage,version='%prog 1.0')
        #通过OptionParser类创建parser实例,初始参数usage中的%prog等同于os.path.basename(sys.argv[0]),即
        #你当前所运行的脚本的名字，version参数用来显示当前脚本的版本。

        parser.add_option('-u','--url',
                        action='store',dest='url',
                        metavar='url',help='input url')

        parser.add_option('-l',
                        action='store',dest='level',
                        metavar='level',help='input level')

        parser.add_option('--thread',
                        action='store',dest='threads_Count',default=5,
                        help='input threadsCount')

        parser.add_option('--data',
                        action='store',dest='post_data',
                        help='input post data')
        parser.add_option('--cookie',
                        action='store_true',dest='cookie',
                        help='input cookie information')

        parser.add_option("--user-agent",
                        action='store_false',dest='user_agent',
                        help="use user-agent")

        group = OptionGroup(parser,'Scan Options')
        group.add_option('--dbs',action='store_true',
                        help='list databases')
        group.add_option('--tables',action='store_true',
                        help='list tables')
        group.add_option('--columns',action='store_true',
                        help='list columns')
        group.add_option('--dump',action='store_true',
                        help='list all information')
        parser.add_option_group(group)

        group = OptionGroup(parser,'set scan-Options')
        group.add_option('-D',action='store',dest='database_name',
                        help='Print debug information.')
        group.add_option('-T',action='store',dest='table_name',
                        help='Print all SQL statements executed')
        group.add_option('-C',action='store',dest='column_name',
                        help='Print every action done')
        parser.add_option_group(group)

        #解析脚本输入的参数值，options是一个包含了option值的对象
        #args是一个位置参数的列表
        options, arguments = parser.parse_args()
        return options