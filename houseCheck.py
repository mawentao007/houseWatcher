#coding=utf-8
__author__ = 'marvin'

import re
import urllib
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime
import sys


def getHtml(url):
    retries = 0
    while retries < 5:
        try:
            page = urllib.urlopen(url)
            break
        except OSError:
            time.sleep(2)
            retries += 1

    try:
        page
    except NameError:
        return None
    else:
        return page


def getTop(page):
    html = page.read()
    soup = BeautifulSoup(html,"lxml")
    table = soup.find("ul",opentype="page")
    li = table.findAll('li')
    for one in li:
        a = one.find('a')
        title =  a.attrs['title'].encode('gb18030')
        url =  "http://www.bjjs.gov.cn/" + a.attrs['href'].encode('gb18030')
        date =  one.find('span').text.encode('gb18030')
        print '\t'.join([date, title, url])
    
     

url = "http://www.bjjs.gov.cn/bjjs/xxgk/ztzl/gycqzf/tzgg80/index.shtml"
page = getHtml(url)
getTop(page)


