#!/bin/env python3
# nsfoxer
# time: 2020年 06月 10日 星期三 17:02:23 CST 

import get_info

class Injection():
    '''
    不进行注入检测，假设为带回显的注入
    '''
    database = Database()
    page_info = None
    url = ''
    payload = ''

    def __init__(self, url):
        self.database = Database()
        self.url = url
        self.page_info = get_info.PageInfo(url)
        self.payload = '' # .......................

    def __get_columns_num(self, url_ready, magic_str):
        '''
        得到当前列的所有列数
        '''
        low = 0
        high = 64
        probe_num = 0
        while low < high:
            probe_num = (low+high)/2
            payload = self.payload.get_order_by(probe_num)
            url_malformation = url_ready.replace(magic_str, payload)
            count = self.page_info.init_malinfo_location(url_malformation, ['You have an error in your SQL syntax;'])
            if count > 0:
                # 表示列存在
                low = probe_num+1
            else: # 表示测试列超出范围
                high = probe_num-1
        return probe_num


    def exec_payload(self, location, level):
        '''
        执行
        location == 注入点位置()
        level: 所需要得到的数据详细程度
                1. 库名
                2. 表名
                3. 列名
                4. 库内容
        '''
        # url 预处理
        magic_str = '$$$$$$$$$$$'
        url_ready = self.url.split('=')[:location] + magic_str + '&' + self.url.split('&')[1:]
        # 探测当前表名的列数
        probe_num = self.__get_columns_num(url_ready, magic_str)
        # 探测页面信息暴露点
        payload = self.__get_

        _level = 0
        while _level < level:

            # 
            payload = self.payload.get_payload(database='', table='', column = '')
            # 处理payload
            payload = ''
            # url 拼接
            url_malformation = url_ready.replace(magic_str, payload)
            #
            self.page_info.get_malinfo_location(url_malformation, special_num_list)



def Database():
    database = []
    table= {}

    def __init__(self):
        pass

    def set_database(self, database):
        self.database.append[database]
        self.table.append

    def set_table(self, database, table);
        pass
    def set_column(self, database, table, column):
        pass
    def set_data(self, database, table, column, data):
        pass
    def get_database(self):
        return self.database
    def get_table(self, Database):
        return k

