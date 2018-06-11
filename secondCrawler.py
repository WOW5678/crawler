# -*- encoding=utf-8 -*-
#功能：将写的第一个爬虫程序进行简单的封装  使之更加整齐

import requests
from bs4 import BeautifulSoup
import os

class Meizi(object):
    #爬虫程序的入口函数
    def all_url(self,url):
        html=self.request(url)
        #对网页内容进行解析 查找class为‘all'的div 并找出所有的a标签
        all_a=BeautifulSoup(html.text,'lxml').find('div',class_='all').find_all('a')
        for a in all_a:
            #获取a标签中保存的文本信息-标题
            title=a.get_text()
            print ('benign saving:',title)
            #将路径中的？号替换成_
            path=title.replace("?","_")
            #创建保存图片内容的文件夹
            real_path=self.mkdir(path)

            #切换到相应的文件夹下
            os.chdir(real_path)
            href=a['href']
            self.html(href)
    #请求包含着图片地址的url
    def html(self,href):
        html=self.request(href)
        max_span=BeautifulSoup(html.text,'lxml').find_all('span')[10].get_text()
        for page in range(1,int(max_span)+1):
            page_url=href+'/'+str(page)
            self.img(page_url)
    #请求图片地址的url
    def img(self,page_url):
        img_html=self.request(page_url)
        img_url=BeautifulSoup(img_html.text,'lxml').find('div',class_='main-image').find('img')['src']
        self.save(img_url)
    #保存图片
    def save(self,img_url):
        name=img_url.split(r'/')[-1]
        img=self.request(img_url)
        f=open(name,'wb')
        f.write(img.content)
        f.close()
    #穿件图片保存的文件夹
    def mkdir(self,path):
        path=path.strip()
        isExists=os.path.exists(os.path.join("E:\meizi",path))
        if not isExists:
            print ('the dir'+path,'has been exisits')
            os.makedirs(os.path.join("E:\meizi",path))

        else:
            print ('the dir'+path,'has not been exisits')
        return os.path.join("E:\meizi",path)
    #请求一个网页，返回网页的内容
    def request(self,url):
        headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 \
        (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content=requests.get(url,headers=headers)
        return content
if __name__ == '__main__':
    meizi=Meizi()
    meizi.all_url("http://www.mzitu.com/all")

