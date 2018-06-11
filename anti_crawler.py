# -*- coding:utf-8 -*-
#功能：实现简单的爬虫模块  考虑进去了网站的反爬虫策略 
#要解决的策略是（1）网站限制IP访问频率
# （2）网站对访问进行统计，单个UA的访问不能超过阈值
#该模块可以直接被其他爬虫程序使用

import requests
import re
import random
import time

class Download():
    def __init__(self):
        #获取IP代理的列表
        self.ip_list=[]
        html=requests.get('http://haoip.cc/tiqu.htm')
        #表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配换行符，findall返回的是个列表
        ipListn=re.findall(r'r/>(.*?)<b', html.text, re.S)
        for ip in ipListn:
            #re.sub是re 模块替换的方法，这里表示将\n替换成空
            i=re.sub('\n','',ip)
            self.ip_list.append(i.strip())

        #UA列表
        self.user_agent_list=[
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get(self,url,timeout,proxy=None,num_retries=6): #给函数一个默认参数proxy为None
        #从self.user_agent_list中随机选择一个ua
        UA=random.choice(self.user_agent_list)
        headers={'User-Agent':UA} #构建符合格式的User-Agent

        if proxy==None:
            try:
                #当代理为空时，不使用代理获取response
                response=requests.get(url,headers=headers)
                return response
            except:
                if(num_retries>0):
                    time.sleep(10)#延迟10秒钟
                    print(u'获取页面出错，10s后将获取倒数第:',num_retries,u'次')
                    return self.get(url,timeout,num_retries-1) #调用自身 并将可重用的次数减一
                else:
                    #当重用的次数小于0即重试了6次都失败了 则应使用代理
                    print(u'开始使用代理')
                    time.sleep(10)
                    ip=''.join(str(random.choice(self.ip_list)).strip())
                    proxy={'http':ip}
                    return self.get(url,timeout,proxy)
        else: #当代理不为空时
           try:
                #将从self.ipList中获取的字符串处理成需要的格式
                ip=''.join(str(random.choice(self.ip_list)).strip())
                proxy={'http':ip}#构造成一个代理
                response=requests.get(url,headers=headers,proxies=proxy)
                return response
           except:
               if num_retries>0:
                   time.sleep(10)
                   IP=''.join(str(random.choice(self.ip_list)).strip())
                   proxy={'http':IP}
                   print(u'正在使用代理，10s后将重新获取倒数第',num_retries,u'次')
                   print(u'当前代理是：',proxy)
                   return self.get(url,timeout,proxy,num_retries-1)
               else:
                   #代理尝试了6次都失败，该代理不能使用了
                   print(u'该代理已经不能使用，取消代理')
                   return self.get(url,3)


