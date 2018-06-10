# -*- coding:utf-8 -*-
#功能：为链接爬虫添加缓存支持目的是：
# 可以让每个网页只下载一次，再次下载时直接从缓存中加载 极大地提高了爬取速度
import urlparse
import urllib2
import random
import time
from datetime import datetime,timedelta
import socket

DEFAUL_AGENT='wswp'
DEFAUL_DELAY=5
DEFAUL_RETRIES=1
DEFAUL_TIMEOUT=60

class downloader:
    def __init__(self,delay=DEFAUL_DELAY,user_agent=DEFAUL_AGENT,proxies=None,num_retires=DEFAUL_RETRIES,timeout=DEFAUL_TIMEOUT,opener=None,cache=None):
        socket.setdefaulttimeout(timeout)
        #限速对象
        self.throttle=Throttle(delay)
        self.user_agent=user_agent
        self.proxies=proxies
        self.num_retires=num_retires
        self.opener=opener
        self.cache=cache

    def __call__(self, url):
        result=None

        #如何设置了缓存
        if self.cache:
            try:
                result=self.cache[url]
            except KeyError:
                pass
            #如果cache中存在该url的内容 但是服务器端没有报错 也将reuslt设为None
            else:
                if self.num_retires>0 and 500<=result['code']<600:
                    result=None
        if result==None:
            #缓存中不存在 则要重新下载 先进行限时
            self.throttle.wait(url)
            #从代理列表中随机选择一个代理 如果列表为空 则代理设为None
            proxy=random.choice([self.proxies]) if self.proxies else None
            headers={'user-agent':self.user_agent}
            result=self.download(url,headers,proxy=proxy,num_retires=self.num_retires)

            #将新下载的内容加入到缓存中
            if self.cache:
                self.cache[url]=result
        return result['html']

    '''
    从网上下载网页的函数
    '''
    def download(self,url,headers,proxy,num_retires,data=None):
        print('Downloading:',url)
        request=urllib2.Request(url,data,headers or {})
        opener=self.opener or urllib2.build_opener()
        if proxy:
            proxy_params={urlparse.urlparse(url).scheme:proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response=opener.open(request)
            html=response.read()
            code=response.code
        except Exception as e:
            print('Download error:',str(e))
            html=''
            if hasattr(e,'code') and 500<=e.code<600:
                return self._get(url,headers,proxy,num_retires-1,data)
            else:
                code=None
        #将下载的网页和错误码同时返回
        return {'html':html,'code':code}
'''
限时对象
'''
class Throttle:
    def  __init__(self,delay):
        self.delay=delay
        #保存着上次访问的网页以及访问的时间
        self.domains={}
    def wait(self,url):
        #分割url字符串 获得服务器
        domain=urlparse.urlsplit(url).netloc
        last_accessed=self.domains.get(domain)
        #如果加入了限时条件并且 最近刚访问了此域名
        if self.delay >0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                #进行休眠
                time.sleep(sleep_secs)
        #更新该域名被访问的时间
        self.domains[domain]=datetime.now()

d=downloader(DEFAUL_DELAY,DEFAUL_AGENT,DEFAUL_RETRIES,DEFAUL_TIMEOUT,cache=None)
d.__call__('http://example.webscraping.com/places/default/view/Aland-Islands-2')


