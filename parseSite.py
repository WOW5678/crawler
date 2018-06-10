# -*- coding:utf-8 -*-
#功能：解析网站的一些相关信息，比如网站构建的技术类型

import builtwith
#打印该网站使用到的技术
print builtwith.parse('http://example.webscraping.com')

import whois
print(whois.whois('appspot.com'))