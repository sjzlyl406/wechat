#!/usr/bin/env python
# coding=utf-8

import re
import urllib
import urllib2
import time
import thread
from bs4 import BeautifulSoup

class BaiDuTieBa:
    header={
        u"host":u"tieba.baidu.com",
        u"Connection":u"keep-alive",
        u"Accept":u"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        u"User-Agent":u"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0",
        u"Accept-Language":u"zh-CN,zh;q=0.8"
    }

    def __init__(self):
        self.page = 1
        self.pages = list()
        self.enable = False
        self.url = u"http://tieba.baidu.com/p/3434860781?see_lz=1&pn="
        # self.url = u"http://tieba.baidu.com/p/4549000252"

    def get(self, page):
        self.url = self.url + page

        req = urllib2.Request(url=self.url, headers=self.header)
        result=urllib2.urlopen(req)
        result = result.read()
        
        soup=BeautifulSoup(result, u"lxml")
        content = soup.find('div', {u"id":u"j_p_postlist"}).findAll(u"cc")

        items = list()
        for item in content:
            print item.get_text()
            items.append(item.get_text())

        return items
    def load(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.get(str(self.page))
                    self.pages.append(myPage)
                    self.page += 1
                except Exception, e:
                    print u"can't connect to baidu.", e
            else:
                time.sleep(1)

    def show(self, currentPage, page):
        for items in currentPage:
            print u"第%d页" % page, items
            myInput = raw_input()
            if myInput == 'q':
                self.enable = False
                break
    def start(self):
        self.enable = True
        page = self.page
        print u"wait ..."

        thread.start_new_thread(self.load, ())

        while self.enable:
            if self.pages:
                currentPage = self.pages[0]
                del self.pages[0]
                self.show(currentPage, page)
                page += 1

def main():
    raw_input(' ')
    bd = BaiDuTieBa()
    bd.start()


if __name__=="__main__":
    main()
