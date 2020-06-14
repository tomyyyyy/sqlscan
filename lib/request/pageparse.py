import requests
import urllib.parse
import sys
from lxml import etree
from lib.output.output import Output
import requests

class Page():
    def __init__(self,arguments):
        self.options = arguments.options
        self.url = arguments.options.url
        self.headers = arguments.headers
        self.output = Output()

        
    def parseurl(self):
        if self.options.post_data == None:
            try:
                urlpath = self.url.split("?")[0]
                parameters = self.url.split("?")[1].split("&")
            except Exception as e:
                self.output.error("url输入不符合要求!",e)
                sys.exit(0)
            try:
                if requests.get(self.url).status_code == 404:
                    self.output.error("url不可访问!")
                    sys.exit(0)
            except Exception as e:
                print(e)
        else:
            parameters = self.options.post_data.split("&") 
            urlpath = self.url       
        parameter = {}
        for i in parameters:
            key, value = i.split("=")[0],i.split("=")[1]
            parameter[key] = value
        return self.url, urlpath, parameter

    def request(self,url,param,headers):
        if self.options.post_data == None:
            return requests.get(url,params=param,headers=headers)
        else:
            return requests.post(url,data=param,headers=headers)
        


            

