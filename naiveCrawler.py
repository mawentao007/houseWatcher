#coding=utf-8
__author__ = 'marvin'

import re
import urllib
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import os
import time
from datetime import datetime





def getHtml(url):
    timeout = 100
    retries = 0
    while retries < 5:
        try:
            page = urllib.request.urlopen(url,timeout = timeout)
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

def getTop(html):
    soup = BeautifulSoup(html,"lxml")
    table = soup.find("table",id="ess_ctr9680_ListC_Info_LstC_Info").tr
    contents = []

    for index,x in enumerate(table.next_siblings):
        if index > 10:
            break
        contents.append(x.find("td",align="right").text)
    return contents


def checkDate(dates,siteUrl):

    today = datetime.today().day
    month = datetime.today().month

    root = tk.Tk()
    root.withdraw()

    for t in dates:
        pt = re.search(r"\d+\-(\d+)\-(\d+)",t)
        m = int(pt.group(1))
        d = int(pt.group(2))

        if month == m:
            if d == today:
                messagebox.showinfo("紧急","今天有新消息发布!")
                os.system("firefox %s"%siteUrl)
                return 0
            elif abs(today - d) < 3:
                messagebox.showinfo("查询结果","最近三天有新消息发布!")
                os.system("firefox %s"%siteUrl)
                return 0

    messagebox.showinfo("查询结果","最近三天没有新消息发布!")
    return 0




# def writeNewFile(contents):
#      with open("lastCraw.txt","w",encoding="utf-8") as f:
#         f.write(contents)
#
#
# def readOldFile():
#     with open("lastCraw.txt","r") as f:
#         contents = f.readline()
#         return contents


def main():
    root = tk.Tk()
    root.withdraw()

    siteUrl = "http://www.bjjs.gov.cn/tabid/1072/MoreModuleID/10041/MoreTabID/4021/Default.aspx"
    html = getHtml(siteUrl)
    if html == None:
        messagebox.showerror('错误','网络出现问题')
        return -1

    dates = getTop(html)
    checkDate(dates,siteUrl)

    return 0

if __name__ =="__main__":
    main()