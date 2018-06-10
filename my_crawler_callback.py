# -*- coding:utf-8 -*-
#功能：一个完整的爬虫实现例子 包含了爬虫的几乎所有知识点（代理，限时，防止陷阱、爬取回调，lxml解析内容等等）

import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue
import csv
import lxml.html

def link_crawler(seed_url,link_regex=None,delay=5,max_depth=-1,max_urls=-1,\
                 headers=None,user_agent='wswp',proxy=None,num_retries=1,ScrapeCallback=None):
    #待爬取的url列表
    crawl_quue=[seed_url]
    #seen中保存已经爬取的每个url的深度
    seen={seed_url:0}
    #记录已经下载的url个数
    num_urls=0
    rp=get_robots(seed_url)
    #创建一个限时的实例对象
    throttle=Throttle(delay)
    headers=headers or {}
    if user_agent:
        headers['User-agent']=user_agent

    while crawl_quue:
        #取出第一条Url
        url=crawl_quue.pop()
        #该url的深度
        depth=seen[url]
        #判断时候不被robots禁用
        if rp.can_fetch(user_agent,url):
            #休眠
            throttle.wait(url)
            html=download(url,headers,proxy=None,num_retires=num_retries)
            links=[]
            if ScrapeCallback:
                links.extend(ScrapeCallback.getContent(url,html) or [])
            if depth!=max_depth:
                if link_regex:
                    #print('get_links:',get_links(html))
                    links.extend(link for link in get_links(html) if re.match(link_regex,link))

                for link in links:
                    link=normalize(seed_url,link)

                    #检查这个url是否已经被爬取
                    if link not in seen:
                        seen[link]=depth+1
                        if same_domain(seed_url,link):
                            crawl_quue.append(link)

            num_urls+=1
            #判断是否达到了下载的最大量
            if num_urls==max_urls:
                break
        else:
            print('Blocked by the robots.txt:',url)

'''
获得robots解析对象
'''
def get_robots(url):
    rp=robotparser.RobotFileParser()
    #robots字符串拼接
    rp.set_url(urlparse.urljoin(url,'/robots.txt'))
    rp.read()
    return rp

'''
限时类
'''
class Throttle:
    def __init__(self,delay):
        self.delay=delay
        #上次访问域名的时间戳
        self.domains={}
    def wait(self,url):
        #分割url 获取服务器地址 即域名
        domain=urlparse.urlparse(url).netloc
        #获得上次访问该domain的时间 若不存在返回None
        last_accessed=self.domains.get(domain)
        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        #更新域名访问的时间戳
        self.domains[domain]=datetime.now()

'''
包含了用户代理 代理 重试次数的下载函数
'''
def download(url,headers,proxy=None,num_retires=1,data=None):
    print('Downloading:',url)
    #data为向服务器发送的是数据
    request=urllib2.Request(url,data,headers)
    opener=urllib2.build_opener()

    if proxy:
        proxy_params={urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response=opener.open(request)
        html=response.read()
        code=response.code
    except urllib2.URLError as e:
        print('Download error:',e.reason)
        html=''
        if hasattr(e,'code') and 500 <=e.code<600:
            html=download(url,headers,proxy,num_retires-1,data)
        else:
            code=None
    return html


'''
从HTML中解析出所有的url链接
'''
def get_links(html):
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)

'''
对url进行规则化处理 即移除url hash  并添加上域名
'''
def normalize(seed_url,link):
    #移除url的hash
    new_link,_ =urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url,new_link)

'''
判断两个url是否属于同一个域名
'''
def same_domain(url1, url2):
    return urlparse.urlparse(url1).netloc==urlparse.urlparse(url2).netloc

'''
回调类
'''
class ScrapeCallback:

    def __init__(self):
        self.writer=csv.writer(open('Counteries.csv','w'))
        self.fields=('area','population','iso','country','capital','continent','tld','currency_code',\
                     'currency_name','phone','postal_code_format','postal_code_regex','languages','neighbours')
        self.writer.writerow(self.fields)

    def getContent(self, url,html):
        if re.match('(.*?)/view',url):
            tree=lxml.html.fromstring(html)
            row=[]
            for filed in self.fields:
                print('field:',filed)
                row.append(tree.cssselect('tr#places_{0}__row > td.w2p_fw'.format(filed))[0].text_content())
            print('row:',row)
            self.writer.writerow(row)

if __name__ == '__main__':
    #link_crawler('http://example.webscraping.com/places/default', '(.*?)(view|index)', delay=0, num_retries=1, user_agent='BadCrawler')

    link_crawler('http://example.webscraping.com/places/default', '(.*?)(view|index)', delay=0, num_retries=1, max_depth=1,
                 user_agent='GoodCrawler',ScrapeCallback=ScrapeCallback())