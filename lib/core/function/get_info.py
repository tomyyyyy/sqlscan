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
            malinformation = self._refine_str(self.info_normal[0], orig_malinformation[0])
            return malinformation

    def _refine_str(self, str1, str2):
        if len(str1) < len(str2):
            count = len(str1)
        else:
            count = len(str2)
        for i in range(count):
            if str1[i] != str2[i]:
                break
        return str2[i:]

    def init_malinfo_location(self, url_malformation, special_num_list):
        '''
        进行页面信息位置探测,初始化self.malinfo_location，返回页面信息暴露位置最后一次被探测到的特定字符序号
        special_num_list: 特定字符串列表. ['dsa', 'special']
        '''
        req = requests.get(url=url_malformation)
        page_malformation = req.text
        page_parse = Page_parse(page_malformation)
        i = -1
        for special_num in special_num_list:
            location= page_parse.str2location(str(special_num))
            if len(location) != 0:
                i = 1 + i
                self.malinfo_location.append(location)
        # 进行正常页面信息提取
        page_parse = Page_parse(self.page_normal)
        for location_list in self.malinfo_location:
            self.info_normal.append(page_parse.loction2str(location_list))

        return i

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

    def __init__(self, page_str):
        self.page_text = page_str

    def set_page_text(self, page_str):
        # 重新设置目标文本
        self.page_text = page_str

    def str2location(self, special_str):
        # 将第一个特定字符串的所有前标签位置以列表形式返回
        self.adjust_location_list = [] # 将判断列表置空
        self.special_str = special_str
        self.feed(self.page_text)
        return self.location_list

    def loction2str(self, loaction_list):
        # 取出给定的标签位置的内容
        self.special_str = '' # 将特定字符串置空
        self.adjust_location_list = loaction_list
        self.feed(self.page_text)
        return self.data

    def handle_starttag(self, tag, attrs):
        self.location_list.append(tag)

#    def handle_endtag(self, tag):
#        self.location_list.pop()

    def handle_data(self, data):
        # 得到ajust_location_list路径中的数据,当判断列表不为空时，表示被location2str调用
        if len(self.adjust_location_list) != 0 and operator.eq(self.adjust_location_list, self.location_list):
            self.data = data
            return
        # 获得特定字符串所在标签路径，当特殊字符不为空时，表示被location2str调用
        if self.special_str != '' and self.special_str in data:
            return

