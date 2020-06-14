#!/bin/env python3
# nsfoxer

'''
页面加载，与暴露信息返回
'''
import requests
import sys
from html.parser import HTMLParser
import operator

class PageInfo():
    '''
    get，加载页面
    '''
    url = ''
    page_normal = '' # normal page
    malinfo_location = [] # 恶意信息位置, [ ['root', 'tree' ...],['root', 'tree' ... ], ...]
    info_normal = [] # 正常页面，信息

    def __init__(self, url):
        '''
        url :正常页面url访问
        '''
        self.url = url
        req = requests.get(url=url)

        if req.status_code == 200:
            # 将正常页面保存至页面已对payload进行比较
            self.page_normal = req.text
        else:
            # 如果url访问 ！= 200， 直接报错退出
            sys.stderr.write('website should response 200 status_code\n')
            raise SystemExit(1)

    def get_info(self, url_malformation):
        '''
         假设get方式请求，并且只有一个参数
         多参数，至暂未考虑
         应该先调用get_malinfo_location,进行恶意点初始化
         根据已知的信息位置，返回第一个内容 "dsada"
         返回-1表示找不到暴露信息路径
         返回-2，表示页面404
        '''
        if len(self.malinfo_location) == 0:
            return -1

        req = requests.get(url=url_malformation)
        if req.status_code == 404:
            # 404 页面，此次payload有误，重新加载
            return -2
        else:
            # 提取恶意信息
            orig_malinformation = [] # 原始信息
            page_malformation = req.text
            page_parse = Page_parse(page_malformation)
            for loaction_list in self.malinfo_location:
                orig_malinformation.append(page_parse.loction2str(loaction_list))
            # 进行页面比较
            malinformation = self._refine_str(self.info_normal[-1], orig_malinformation[-1])
            return malinformation

    def _refine_str(self, str1, str2):
        if isinstance(str2, str) == False:
            return ''
        if str1 == str2:
            return ''
        if len(str1) < len(str2):
            count = len(str1)
        else:
            count = len(str2)
        i = 0
        for i in range(count):
            if str1[i] != str2[i]:
                break
        # str2 字符过少，即未提取到有用信息；这里是边界处理
        if str1[i] == str2[i]:
            return ''
        return str2[i:]

    def init_malinfo_location(self, url_malformation, special_num_list):
        '''
        进行页面信息位置探测,初始化self.malinfo_location，返回页面信息暴露位置最后一次被探测到的特定字符序号
        special_num_list: 特定字符串列表. ['dsa', 'special']
        '''
        req = requests.get(url=url_malformation)
        page_malformation = req.text
        page_parse = Page_parse(page_malformation)
        # 包含special_num_list的字符串位置
        i = 0
        serial_num = -1 # 表示包含special_num_list字符第几个最后一次出现
        self.malinfo_location = []
        for special_num in special_num_list:
            location= page_parse.str2location(str(special_num))
            if len(location) != 0:
                serial_num = i
                self.malinfo_location.append(location)
            i += 1
        # 进行正常页面信息提取
        page_parse = Page_parse(self.page_normal)
        self.info_normal = []
        for location_list in self.malinfo_location:
            self.info_normal.append(page_parse.loction2str(location_list))

        return serial_num

    def get_malinfo_location(self):
        return self.malinfo_location


class Page_parse(HTMLParser):
    '''
    解析指定路径或根据数据形成路径(html)
    '''
    page_text = ''
    location_list = []
    special_str = ''
    adjust_location_list = []
    data = ''
    _str_is_success = False
    _location_is_success = False
    str_location_list = []

    def __init__(self, page_str):
        HTMLParser.__init__(self)
        self.page_text = page_str
        self._clean()

    def set_page_text(self, page_str):
        # 重新设置目标文本
        self._clean()
        self.page_text = page_str

    def _clean(self):
        self._str_is_success = False
        self._location_is_success = False
        self.location_list = []
        self.data = ''
        self.adjust_location_list = [] # 将判断列表置空
        self.special_str = '' # 将特定字符串置空
        self.str_location_list = []

    def str2location(self, special_str):
        self._clean()
        # 将第一个特定字符串的所有前标签位置以列表形式返回
        self.special_str = special_str
        self.feed(self.page_text)
        if self._str_is_success == True:
            return self.str_location_list
        else:
            return []

    def loction2str(self, loaction_list):
        self._clean()
        # 取出给定的标签位置的内容
        self.adjust_location_list = loaction_list
        self.feed(self.page_text)
        if self._location_is_success == True:
            return self.data
        else:
            return -1

    def handle_starttag(self, tag, attrs):
        self.location_list.append(tag)
        if self._str_is_success == False:
            self.str_location_list.append(tag)

#    def handle_endtag(self, tag):
#        self.location_list.append(tag)

    def handle_data(self, data):
        # 得到ajust_location_list路径中的数据,当判断列表不为空时，表示被location2str调用
        if len(self.adjust_location_list) != 0 and operator.eq(self.adjust_location_list, self.location_list) and self._location_is_success == False:
            self.data = data
            self._location_is_success = True
        # 获得特定字符串所在标签路径，当特殊字符不为空时，表示被str2location调用
        if self.special_str != '' and self.special_str in data and self._str_is_success == False:
            self._str_is_success = True
