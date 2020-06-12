import requests
import urllib.parse
import sys
from lxml import etree
from lib.output.output import Output

class Page():
    def __init__(self,url):
        self.url = url
        self.output = Output()
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        self.cookie = ""
        self.headers = {
            'content-type': 'application/json',
            'User-Agent': self.user_agent,
            'cookie': self.cookie
           }
        self.output = Output()
        

    def parseurl(self):
        try:
            urlpath = self.url.split("?")[0]
            parameters = self.url.split("?")[1].split("&")
        except Exception as e:
            self.output.warning("url输入不符合要求!",e)
            sys.exit(0)
        try:
            if requests.get(self.url).status_code == 404:
                self.output.warning("url不可访问!")
                sys.exit(0)
        except Exception as e:
            print(e)
             
        parameter = {}
        for i in parameters:
            key, value = i.split("=")[0],i.split("=")[1]
            parameter[key] = value
        return self.url,urlpath, parameter


    def get_content(self):
        try:
            response = requests.get(self.url, headers = self.headers)
            body = response.text    #获取网页内容
        except Exception as e:
            self.output.warning('request is error!',e)
            sys.exit(0)
        # html=etree.HTML(body, etree.HTMLParser())  #解析HTML文本内容
        return body


if __name__ == "__main__":
    url = "https://www.duitang.com/napi/blog/list/by_search/?kw=dddd&start=1"
    page = Page(url)
    print(page.parseurl())
