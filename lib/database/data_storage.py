# nsfoxer
# Time: 2020年 06月 11日 星期四 16:53:52 CST
# 数据库存储与处理
import sqlite3
import os
import sys
from lib.output.output import *

class Data():
    conn = None
    cursor = None

    def __init__(self, filename):
        f_l = F"./lib/database/data/{filename}"
        self.conn = sqlite3.connect(f_l)
        self.cursor = self.conn.cursor()
        self._create_databases(f_l)
        self.output = Output()

    def _create_databases(self, file_path):
        # 创建库表
        # 表示库名，表名
        sql = ';'
        if os.path.exists(file_path) == True:
            # 判断sqlscan表是否已经存在
            self.cursor.execute(" select name from sqlite_master where type='table' and name='sqlscan';")
            if len(self.cursor.fetchall()) == 0:
                sql = 'create table sqlscan  ( database char(50) not null, tables  char(50) not null);';
        else:
            sql = 'create table sqlscan  ( database char(50) not null, tables  char(50) not null);';
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def add_database(self, database):
        '''
        增加数据库名
        Args:
            database: 以列表方式增加若干个数据库
        Returns:
            -1, 错误
        '''
        if database[0] == '':
            self.output.error("数据无效")
            return -1
        for db in database:
            if db in self.get_databases():
                return -1
            sql = F"insert into sqlscan (database, tables) values('{db}', 'sqlscan');"
            self.cursor.execute(sql)
        self.conn.commit()

    def get_databases(self):
        '''
        返回所有数据库名['', '']
        '''
        sql = 'select database from sqlscan where tables="sqlscan" ;'
        self.cursor.execute(sql)
        return  [row[0] for row in self.cursor]

    def add_tables(self, database, table):
        '''
        增加若干表
        Args:
            database: str型的一个库名
            table: 若干个str(表名)的列表
        '''
        if database == '' or table[0] == '':
            self.output.error("数据无效")
            return -1
        # 判断库是否存在
        if database not in self.get_databases():
            return -1
        for tb in table:
            if tb in self.get_tables(database):
                # 表已经存在
                return -1
            # 向sqlscan表写入数据
            sql = F"insert into sqlscan (database, tables) values('{database}', '{tb}');"
            self.cursor.execute(sql)
            # 创建这个表
            table_name = F"{database}_{tb}"
            sql = F"create table {table_name} (sqlscan_id int);" # 无法创建空表，暂时就这么用吧
            self.cursor.execute(sql)
        self.conn.commit()

    def get_tables(self, database):
        '''
        得到database所有表名
        database: str
        Returns:
            字符串为单元的列表，每一项表示一个库名
        '''
        sql = F"select tables from sqlscan where database='{database}' and tables != 'sqlscan'; "
        result = self.cursor.execute(sql)
        return [row[0] for row in result]

    def add_column(self, database, table, column):
        '''
        表中增加一个键
        Args:
            database : str型的一个库名
            table : str型的一个表名
            column : str单元的列表名
        '''
        if database == '' or table == '' or column[0] == '':
            self.output.error("数据无效")
            return -1
        if database not in self.get_databases() or table not in self.get_tables(database):
            return -1
        know_column = self.get_columns(database, table)
        for cd in column:
            if cd == '' or cd == ':':
                return -1
            if cd in know_column:
                continue
            table_name = F"{database}_{table}"
            sql = F"alter table {table_name} add column {cd} vachar;"
            self.cursor.execute(sql)
        self.conn.commit()

    def get_columns(self, database, table):
        '''
        获得某个库的某个表的所有列
        Args:
            database: str型的一个库名
            table: str型的一个表名

        Returns:
            str单元的列表
        '''
        table_name = F"{database}_{table}"
        sql = F"pragma table_info({table_name});"
        result = self.cursor.execute(sql)
        sim_result = []
        for row in result:
            if row[1] != 'sqlscan_id':
                sim_result.append(row[1])
        return sim_result

    def add_data(self, database, table, column, data):
        '''
        向某表中添加数据
        Args:
            database: str型的一个库名
            table: str型的一个表名
            column: str单元列表,应当与data一一对应
            data: str单元列表，应当与column一一对应
        Returns:
            -1: 错误
            0: 成功
        '''
        if database == '' or table == '' or len(column)==0 or column[0] == '' or data [0]== '':
            self.output.error("数据无效")
            return -1
        # 数据有效性检测
        if len(column) != len(data):
            return -1
        # 库，表存在性检测
        if database not in self.get_databases() or table not in self.get_tables(database):
            return -1
        column_sql = ''
        data_sql = ''
        know_column = self.get_columns(database, table)
        for i in range(len(column)):
            if column[i] not in know_column:
                return -1
            column_sql += column[i]
            data_sql += F"'{data[i]}'"
            if i < len(column)-1:
                column_sql += ', '
                data_sql += ', '
        sql = F"insert into {database}_{table} ({column_sql}) values ({data_sql});"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except BaseException:
            sys.stderr.write("sql error: " + sql)
        return 0

    def get_data(self, database, table, column):
        '''
        返回所需要得数据
        Args:
            database: str型的一个库名
            table: str型的一个表名
            column: str单元列表
        Returns:
            返回[ (str, str, ...), (str, str, ...)...]
            -1: error
        '''
        # sql 列拼接
        sql_columns = ''
        for i in range(len(column)):
            sql_columns = sql_columns + column[i]
            if i < len(column)-1:
                sql_columns += ', '
        sql = F"select {sql_columns} from {database}_{table} ;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
