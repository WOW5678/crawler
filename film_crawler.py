#-*- coding:utf-8  -*-
#功能：把豆瓣分类电影排行趴下来并写入数据库

from urllib.request import Request,urlopen
from urllib.error import  URLError, HTTPError
import re
import sys
import pymysql
import time
import json

#链接数据库，查看有没有douban这个表 如果有则删掉重建一个
conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='douban')
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS douban') #如果douban这个数据表存在 则删除，可确保每次执行数据都是最新的而不是插入的
sql="""create table douban(id int PRIMARY key not null auto_increment,title text,actor text,rating char(20))"""
cur.execute(sql)

url='https://movie.douban.com/j/chart/top_list?type=10&interval_id=100:90&action=&start=20&limit=100'
req=Request(url)
user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
req.add_header('User-Agent',user_agent)
try:
    response=urlopen(req)
except HTTPError as e:
    print('The server could not fuifill the request.')
    print('Error code:',e.code)
except URLError as e:
    print('We failed to reach a server.')
    print('Reason:',e.reason)

#对返回的文本内容进行utf-8 编码
html=response.read().decode('utf-8')
#print('html:',html)
#找出分类页面中所有电影的超链接地址
lp=re.compile(r'movie.douban.com.*?subject.*?\\d+')
link=lp.findall('https:\/\/movie.douban.com\/subject\/1763939\/')
print(link)





