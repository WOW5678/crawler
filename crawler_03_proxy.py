# -*- coding:utf-8 -*-
#功能：使用代理访问某个网站，比如 Netflix屏蔽了美国以外的大多数国家 urlLib2支持代理有点复杂，可以使用更加
#友好的http 模块的requests来实现该功能
import urllib2
import urlparse
import  datetime
import time
'''
增加了代理功能的下载函数
'''
def download(url,user_agent='wswp',proxy=None,num_reties=2):
    '''
    :param url: 要下载的Url
    :param user_agent: 用户代理
    :param proxy: 代理
    :param num_reties:重试的次数 
    :return: 
    '''
    print('Downloading:',url)
    headers={'User-agent':user_agent}
    request=urllib2.Request(url,headers=headers)

    opener=urllib2.build_opener()
    if proxy:
        proxy_params={urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html=opener.open(request).read()
    except urllib2.URLError as e:
        print('Download error:',e.reason)
        html=None
        if num_reties>0:
            if hasattr(e,'code') and 500<=e.code<600:
                html=download(url,user_agent,proxy,num_reties-1)
    return html

'''
限制下载速度  如果我们爬取网站的速度过快，就会面临被封禁或者造成服务器过载，为了降低这个风险，我们可以在两次
下载之间添加延时，从而对爬虫限速
'''
class Throttle:
    def __init__(self,delay):
        self.delay=delay
        #保存着每个域名上次被获取的时间戳 即key为域名 value为时间戳
        self.domains={}

    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        #从self.domains中查找该域名 上次被访问的时间戳 若不存在 返回None
        last_accessed=self.domains.get(domain)

        if self.delay>0 and last_accessed is not None:
            #如果当前时间距离上次访问时间小于指定延时 则执行休眠
            seleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
            if seleep_secs>0:
                time.sleep(seleep_secs)

        #更新上次访问的时间为此时
        self.domains[domain]=datetime.datetime.now()

'''
避免爬虫陷阱 最简单的方法是记录到达当前网页经过了多少个链接 也就是深度，当达到最大深度时，就不再向队列
中添加网页的链接了
'''
from crawel_02 import get_links

#如果想要禁用该功能 只需max_depth为负值 此时当前深度用户不会与之相等
def link_crawler(seed_url,link_regex,max_depth=2):
    #该字典记录着获得每个链接，以及到达该页面经过的深度 key为url value为深度
    seen={}
    crawl_queue=[seed_url]

    while crawl_queue :
        #从连接栈中取出最上面的一条url
        url=crawl_queue.pop()
        depth = seen[url]
        if depth!=max_depth:
            for link in get_links(seed_url):
                if link not in seen:
                    seen[link]=depth+1
                    crawl_queue.append(link)

