# -*- coding:utf-8 -*-
#演示 抓取网页数据的三种方法
import urllib2

def download(url):
    return urllib2.urlopen(url).read()
'''
方法1 正则表达式
'''
def method1(url):
    import re

    html=download(url)
    print re.findall('<td class="w2p_fw">(.*?)</td>',html)
    #仅获取面积这一行 可以把tr标签加进来 有个id 是唯一的
    print re.findall('tr id="places_area__row"><td class="w2p_fl"><label class="readonly" \
    for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>',html)

'''
Beautiful soup的补全功能
'''
def fix_html():
    from bs4 import BeautifulSoup

    broken_url='<ul class="country"><li>Area</li>Population</ul>'
    soup=BeautifulSoup(broken_url,'lxml')
    fix_html=soup.prettify()
    print fix_html

'''
方法2 使用Beautiful soup抽取实例国家的面积数据
'''
def method2(url):
    from bs4 import BeautifulSoup
    html=download(url)
    soup=BeautifulSoup(html)
    #定位面积 先定位到那行数据
    tr=soup.find('tr',attrs={'id':'places_area__row'})
    td=tr.find(attrs={'class':'w2p_fw'})
    area=td.text
    print area

'''
方法3 使用Lxml模块 获取面积数据 
'''
def method3(url):
    import lxml.html
    html=download(url)
    tree=lxml.html.fromstring(html)
    #使用css选择器抽取数据
    td=tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    area=td.text_content()
    print area

'''
lxml也可以实现修正错误的html的功能
'''
def fix_html_lxml():
    import lxml.html
    broken_url='<ul class="country"><li>Area<li>Population</ul>'
    tree=lxml.html.fromstring(broken_url)
    fixed_url=lxml.html.tostring(tree,pretty_print=True)
    print (fixed_url)

method1('http://example.webscraping.com/places/default/view/Aland-Islands-2')
fix_html()
print('====================================================================')
method2('http://example.webscraping.com/places/default/view/Aland-Islands-2')
print('================================================================')
method3('http://example.webscraping.com/places/default/view/Aland-Islands-2')
fix_html_lxml()