#!/usr/bin/env python3
# coding=utf-8

'''打印页面中所有的链接'''

from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_alllinks_in_html(URL=u'http://en.wikipedia.org/wiki/Kevin_Bacon'):
    try:
        html = urlopen(URL)
    except HTTPError as e:
        print('not found {}'.format(URL))
    else:
        if html is None:
            print("html is None.")
    bsObj = BeautifulSoup(html, 'html.parser')
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            print(link.attrs['href'])

if __name__ == '__main__':
    get_alllinks_in_html(URL='http://www.chinacaipu.com/caipu/2595.html')
