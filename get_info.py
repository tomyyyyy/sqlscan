#!/bin/env python3
'''
页面加载，与信息返回
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
    req = '' # requests 请求
    malinfo_location = [] # 恶意信息位置

    def __init__(self, url):
        '''
        url :正常页面url访问
        '''
        self.url = url
        self.req = requests.get(url=url)

        if self.req.status_code == 200:
            # 将正常页面保存至页面已对payload进行比较
            self.page_normal = self.req.text
        else:
            # 如果url访问 ！= 200， 直接报错退出
            sys.stderr.write('website should response 200 status_code\n')
            raise SystemExit(1)

    def load_payload(self, url_malformation):
        '''
         假设get方式请求，并且只有一个参数
         多参数，至暂未考虑
         执行payload，返回页面信息点 ['', '', '']
         返回-1表示找不到暴露信息路径
         返回-2，表示页面404
        '''
        if len(self.malinfo_location) == 0:
            return -1

        self.req = requests.get(url=url_malformation)
        if self.req.status_code == 404:
            # 404 页面，此次payload有误，重新加载
            return -2
        else:
            # 进行页面比较
            malinformation = []
            page_malformation = self.req.text
            page_parse = Page_parse(page_malformation)
            for loaction_list in self.malinfo_location:
                malinformation.append(page_parse.loction2str(loaction_list))
            return malinformation

    def get_malinfo_location(self, page_malformation, special_num_list):
        '''
        进行页面信息位置探测，返回页面信息暴露位置次数
        '''
        page_parse = Page_parse(page_malformation)
        for special_num in special_num_list:
            location= page_parse.str2location(str(special_num))
            if len(location) != 0:
                self.malinfo_location.append(location)
        return len(self.malinfo_location)


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

