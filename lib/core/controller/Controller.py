from lib.request.injection_point import injection_point
from lib.output.output import Output
from lib.core.function.exec_payload import Injection
import sys


class Controller(object):
    def __init__(self, script_path, arguments, output):
        self.script_path = script_path
        self.exit = False
        self.arguments = arguments
        self.output = output

        if self.arguments.options.url != None:
            close_symbol = injection_point(self.arguments).judge_inject()
            inject = Injection(self.arguments.options.url,self.arguments, close_symbol)
            #对-l参数进行判断，判断注入等级
            if self.arguments.options.level == None:
                level = 2
            else:
                if self.arguments.options.level[0] == "=":
                    level = int(self.arguments.options.level[1:])
                else:
                    level = int(self.arguments.options.level)

            # inject.exec_payload(1,level)

            #对--dbs参数进行判断
            if self.arguments.options.show_dbs:
                inject.exec_payload(1,1)
            #对-D参数进行判断
            if self.arguments.options.database_name:
                database_name = self.arguments.options.database_name
            #对--tables参数进行判断
            if self.arguments.options.show_tables:
                inject.exec_payload(1,2,self.arguments.options.database_name)
            #对-T参数进行判断
            if self.arguments.options.table_name:
                table_name = self.arguments.options.table_name
            #对--columns参数进行判断
            if self.arguments.options.show_columns:
                inject.exec_payload(1,3,database_name,table_name)
            #对-C参数进行判断
            if self.arguments.options.column_name:
                columns_name = self.arguments.options.column_name
            #对--dump参数进行判断
            if self.arguments.options.show_dump:
                inject.exec_payload(1,4,database_name,table_name,columns_name.split(","))

            

        else:
            self.output.warining("must support url parameters")
            sys.exit(0)
        

        

