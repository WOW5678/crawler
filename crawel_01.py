# -*- coding:utf-8 -*-
# 功能：第一个简单的爬虫程序

import urllib2
'''
最简化的一个下载网页的函数
'''
def download_01(url):
    return urllib2.urlopen(url).read()
'''
加入了重试下载功能的下载网页函数
url:要爬虫的url
num_reties:最大的重传次数
'''
def download_02(url,num_retries=2):
    print('Downloading:',url)
    try:
        html=urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print('Download error:',e.reason)
        html=None
        if num_retries>0:
            #错误码在500-600之间的错误发生在服务器端 重新请求时 有可能服务器已经解决了这个问题
            if hasattr(e,'code') and 500<=e.code<600:
                return download_02(url,num_retries=num_retries-1)
    return html

'''
设置用户代理
'''
def download_03(url,user_agent='wswp',num_reties=2):
    print('downloading:',url)
    headers={'User-agent':user_agent}
    #在请求对象中加入用户代理信息
    request=urllib2.Request(url,headers=headers)
    try:
        html=urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print('Download error:',e.reason)
        html=None
        if num_reties>0:
            if hasattr(e,'code') and 500<= e.code<600:
                return download_03(url,user_agent,num_reties-1)
    return html

if __name__ == '__main__':

    '''
    使用Id下载所有国家的页面
    '''
    import itertools
    #itertools会创建一个可以无限循环的迭代对象
    for page in itertools.count(1):
        url='http://example.webscraping.com/view/-%d' %page
        html=download_03(url)
        #当返回的数据为空 说明Id不存在 已经遍历完了id  假设了Id之间是连续的
        if html is None:
            break
        else:
            pass

    #改进版本：
    #在连续发生多次下载错误以后才会退出程序
    max_error=5
    num_error=0 #用来计数 连续下载错误的次数
    for page in itertools.count(1):
        url='http://example.webscraping.com/view/-%d'%page
        html=download_03(url)
        if html is None:
            num_error+=1
            if num_error==max_error:
                break
        else:
            num_error=0




#测试函数是否正常运行
#print download_01(r'http://www.baidu.com')