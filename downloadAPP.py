# -*- coding:utf-8 -*-
import urllib2
import re
import json
import os
import hashlib

class AppSipder:
    def __init__(self):
        #URL模式：http://shouji.baidu.com/software/502/list_x.html,分成三个部分
        self.base_URL = 'http://shouji.baidu.com/software/'

        #类别数字
        self.category_num = [501, 502, 503, 504, 505, 506, 507, 508, 509, 510]
        #self.category_num = [501]
        #分页编号
        self.page_num = [1, 2, 3, 4, 5, 6, 7, 8]
        #self.page_num = [1]



    #获得所有应用 类别 页的url
    def getAppCategoryPageURL(self):
        #所有应用类别的URLlist
        categoryPageURL_list = []
        for x in self.category_num:
            for y in self.page_num:
                categoryPageURL_list.append(self.base_URL + str(x) + '/list_' + str(y) + '.html')
        print('categoryPageURL_list:',categoryPageURL_list)
        return categoryPageURL_list


    #爬取所有应用 详情 页的url
    def getAppDetailPageURL(self):
        categoryPageURL_list = self.getAppCategoryPageURL()
        appDetailPageURL_list = []
        for url in categoryPageURL_list:
            #构造request请求对象
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read().decode("unicode-escape")
            print('content:',content)
            #re模块用于对正则表达式的支持,pattern可以理解为一个匹配模式,re.S指"."可以匹配换行"\n"
            #pattern = re.compile('<div.*?app-box">.*?<a href="(.*?)".*?>', re.S)
            #
            pattern=re.compile('<a class="app-box" href="(.*?)".*?>',re.S)
            resultStr = re.findall(pattern, content)
            print('resultStr:',resultStr)
            for result in resultStr:
                #print 'crawling ' + result
                appDetailPageURL = 'http://shouji.baidu.com/' + result
                appDetailPageURL_list.append(appDetailPageURL)
        print('appDetailPageURL_list:',appDetailPageURL_list)
        return appDetailPageURL_list

    #爬取App详情页中的所需内容
    def getAppInfo(self, appURL):
        try:
            request = urllib2.Request(appURL)
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print "Get appInfo failed:", e.reason
            return None
        #content = response.read().decode("utf-8")
        content=response.read()
        # 创建保存结果的dict
        result = {}
        #得到app名字
        pattern = re.compile('<span>(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['Name'] = resultStr.group(1)

        # 得到app大小，需要对字符串处理
        pattern = re.compile('<span class="size">(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['Size'] = (((resultStr.group(1)).split(':'))[1]).strip()

        #版本
        pattern = re.compile('<span class="version">(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['Version'] = (((resultStr.group(1)).split(':'))[1]).strip()

        #下载量
        pattern = re.compile('<span class="download-num">(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['download-num'] = (((resultStr.group(1)).split(':'))[1]).strip()

        #LOGO URL
        pattern = re.compile('<img src="(.*?)".*?/>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['app-pic'] = resultStr.group(1)

        #下载地址
        pattern = re.compile('<div.*?area-download">.*?<a target="_blank.*?href="(.*?)".*?>', re.S)
        resultStr = re.search(pattern, content)
        if resultStr:
            result['app-href'] = resultStr.group(1)
            #这个就是app的下载地址
            self.download(result['app-href'])


        #详情页
        result['page-url'] = appURL

        #应用描述
        pattern = re.compile('<p.*?content content_hover">(.*?)<span.*?>.*?</span></p>', re.S)
        resultStr = re.search(pattern, content)
        if resultStr:
            result['description'] = resultStr.group(1)
        else:
            pattern = re.compile('<div class=.*?brief-long">.*?<p.*?content">(.*?)</p>.*?</div>', re.S)
            resultStr = re.search(pattern, content)
            if resultStr:
                result['description'] = resultStr.group(1)

        #应用截图
        pattern = re.compile('<li><img data-default=.*?src="(.*?)".*?>', re.S)
        resultStr = re.search(pattern, content)
        if resultStr:
            result['screen-shot'] = resultStr.group(1)
        #print result
        return result
    '''
    下载app到指定文件夹
    '''
    def download(self,app_href):
        #print('os.getcwd',os.getcwd())
        appDir=os.path.join(os.getcwd(),'apkFiles')
        if not os.path.exists(appDir):
            os.mkdir(appDir)
        try:
            request = urllib2.Request(app_href)
            response = urllib2.urlopen(request)
            data = response.read()
            m = hashlib.md5()
            m.update(data)
            appName=m.hexdigest()

            with open(os.path.join(appDir,appName+'.apk'), "wb") as code:
                code.write(data)
        except urllib2.URLError, e:
            print "Request download app failed:", e.reason


    #爬虫开始入口
    def startSpider(self):
        print 'Start crawling please wait...'
        appDetailPageURL_list = self.getAppDetailPageURL()
        resultInfo = []
        for url in appDetailPageURL_list:
            resultInfo.append(self.getAppInfo(url))
        print len(resultInfo), 'apps have been crawled.'
        #resultInfo转换为json数据格式进行保存
        encodedjson = json.dumps(resultInfo)
        with open('appData.json', 'w') as f:
            f.write(encodedjson)
        print 'Finished.'

Spider = AppSipder()
Spider.startSpider()