#!/usr/bin/env python
# coding=utf-8

import urllib
import urllib2
import re
import json
from bs4 import BeautifulSoup

conf = dict(
    city = 101090107,
    city_name = u"高邑",
    url = u"http://www.weather.com.cn/weather1d/%d.shtml",
    header={
        u"host":u"tieba.baidu.com",
        u"Connection":u"keep-alive",
        u"Accept":u"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        u"User-Agent":u"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0",
        u"Accept-Language":u"zh-CN,zh;q=0.8"
    },
    h24content=u"observe24h_data"
)

class parase_h24():
    def __init__(self):

class Weather(): 
    def __init__(self, conf):
        self.conf = conf
        self.url = conf[u"url"]%conf[u"city"]
        self.header = conf[u"header"]

    def init(self):
        req = urllib2.Request(url=self.url)
        for k,v in self.conf[u'header'].iteritems():
            req.add_header(k,v)
        ret_handle = urllib2.urlopen(self.url)
        result  = ret_handle.read()
#        print result
        soup = BeautifulSoup(result, u'lxml')
        # content = soup.find(attrs={'class':'t'}).findAll("li")
        content = soup.find_all(u"script")
        for x in content:
#            print x.get_text().strip()
            if x.get_text().strip().startswith(u"var observe24h_d"):
                mm = x.get_text().strip()[22:-1]
                print mm 
                tokens = json.loads(mm)
                print tokens['od']



def test():
    w = Weather(conf)
    w.init()

if __name__ == "__main__":
    test()
