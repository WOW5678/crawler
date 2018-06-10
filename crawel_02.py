# -*- coding:utf-8 -*-
#功能：第二个简单的爬虫程序 实现一个链接爬虫 根据正则表达式确定需要下载哪些页面

import re
from crawel_01 import download_03
def link_crawler(seed_url,link_regex):
    '''
    从种子Url中爬取 符合正则表达式的链接
    :param seed_url: 初始的Url
    :param link_regex: 匹配链接的正则表达式
    :return: 
    '''
    crawl_queue=[seed_url]
    seen=set(crawl_queue)
    while crawl_queue :
        #从连接栈中取出最上面的一条url
        url=crawl_queue.pop()
        html=download_03(url)
        for link in get_links(html):
            if re.match(link_regex,link):
                crawl_queue.append(link)

def get_links(html):
    '''
    :param html: url内容
    :return: 返回一个保存着Url的列表
    '''
    #从html中匹配出url链接
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #从html找出所有符合正则表达式的字符串 保存到一个列表中 并返回
    return webpage_regex.findall(html)

'''
解析robots.txt文件，以避免下载禁止爬取的Url
'''
import robotparser
rp=robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
print rp.read()
url='http://example.webscraping.com'
user_agent='BadCrawler'
#是不是可以使用这个代理获取网页
print rp.can_fetch(user_agent,url)
user_agent='GoodCrawler'
print(rp.can_fetch(user_agent,url))

'''
link_crawler函数的增强版本，加入了解析robots.txt的功能
'''
def link_crawler_02(seed_url,link_regex):
    crawl_queue = [seed_url]
    while crawl_queue:
        url=crawl_queue.pop()
        #检查这个url是否受robots.txt限制
        if rp.can_fetch(user_agent,url):
            html = download_03(url)
            for link in get_links(html):
                if re.match(link_regex, link):
                    crawl_queue.append(link)
        else:
            print('Blocked by the robots.txt:',url)
