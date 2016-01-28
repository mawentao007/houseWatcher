#coding=utf-8
__author__ = 'marvin'

import re
import urllib
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import os
import time

import subprocess  #调用子进程执行




def getHtml(url):
    timeout = 100
    retries = 0
    while retries < 5:
        try:
            page = urllib.request.urlopen(url,timeout = timeout)
            break
        except OSError:
            time.sleep(1)
            retries += 1

    try:
        page
    except NameError:
        return None
    else:
        return page

def getTop10(html):
    soup = BeautifulSoup(html,"lxml")
    table = soup.find("table",id="ess_ctr9680_ListC_Info_LstC_Info").tr
    contents = []
    for index,x in enumerate(table.next_siblings):
        if index > 9:
            break
        contents.append(x.find("a").text)
    return str(contents)


def writeNewFile(contents):
     with open("lastCraw.txt","w",encoding="utf-8") as f:
        f.write(contents)


def readOldFile():
    with open("lastCraw.txt","r") as f:
        contents = f.readline()
        return contents


def main():
    root = tk.Tk()
    root.withdraw()

    siteUrl = "http://www.bjjs.gov.cn/tabid/1072/MoreModuleID/10041/MoreTabID/4021/Default.aspx"
    html = getHtml(siteUrl)
    if html == None:
        messagebox.showerror('错误','网络出现问题')
        return -1
    oldContents = readOldFile()
    newContents = getTop10(html)
    writeNewFile(newContents)





    if newContents != oldContents:
        messagebox.showwarning('查询结果', '有新的项目公告发布！')
        os.system("firefox %s"%siteUrl)
    else:
        messagebox.showwarning('查询结果', '暂时没有新项目发布！')
        #os.system("firefox  %s"%siteUrl)
    return 0

if __name__ =="__main__":
    main()