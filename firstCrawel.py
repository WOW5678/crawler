# -*- coding:utf-8 -*-
#功能：实现一个小的爬虫程序完成抓取妹子图
#使用的工具是：beautifulsoup解析网页
#该站点目前已经被封掉，程序仅供学习

import requests
from bs4 import BeautifulSoup
import  os

#设置浏览器的请求头，大部分的网站没有这个会报错，请务必加上
headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 \
(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
#开始的Url地址
all_url='http://www.mzitu.com/all'
#使用request中的get方法来获取all-url这个地址的内容，
start_html=requests.get(all_url,headers=headers)
#打印出start_html,请注意，content是二进制的数据，一般用于下载图片，视频，音频等多媒体内容才使用content 对于打印网页内容还是使用text
#print start_html.text

#使用BeautifulSoup来解析我们获取到的内容，‘lxml’是指定的解析器
soup=BeautifulSoup(start_html.text,'lxml')
li_list=soup.find_all('li')
# for li in li_list:
#     print(li)
#先找到class为all的div标签，然后查找所有的a标签
all_a=soup.find('div',class_='all').find_all('a')
for a in all_a:
    #print a
    title=a.get_text()
    #print title
    #取出a标签的href属性
    href=soup.a['href']
    html=requests.get(href,headers=headers)
    html_soup=BeautifulSoup(html.text,'lxml')
    #查找所有的span标签 获取第十个span标签中的文本也就是最后一个页面了
    max_span=html_soup.find_all('span')[:5]
    #print max_span
    for page in range(1,len(max_span)+1):
        page_url=href+'/'+str(page)
        #print page_url
        image_html=requests.get(page_url,headers=headers)
        image_soup=BeautifulSoup(image_html.text,"lxml")
        div=image_soup.find('div',class_='main-image')
        if div!=None:
            print (div)
            #还需要嵌套一层
            image_url=div.find('img')['src']
            #在创建一层BeautifulSoup
            # soup2=BeautifulSoup()
            print (image_url)

            #开始保存图片了
            image_name=image_url.split(r'/')[-1]
            print (image_name)
            image=requests.get(image_url,headers=headers)
            f=open(image_name,"wb")
            f.write(image.content)
            f.close()
