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
    retries = 0
    while retries < 5:
        try:
            page = urllib.request.urlopen(url)
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
    table = soup.find("table",id="ess_ctr9680_ListC_Info_LstC_Info")

    return table


#通过检查时间的方式来查看
def checkDate(table,siteUrl):

    today = datetime.today().day
    month = datetime.today().month

    tds = table.find_all("td",align="right")

    contents = []
    for x in tds:
        contents.append(x.text)


    for t in contents:
        pt = re.search(r"\d+\-(\d+)\-(\d+)",t)
        m = int(pt.group(1))
        d = int(pt.group(2))

        if month == m:
            if d == today:
                showMessage("紧急","今天有新消息发布!")
                os.system("firefox %s"%siteUrl)
                return 0
            elif abs(today - d) < 3:
                showMessage("查询结果","最近三天有新消息发布!")
                os.system("firefox %s"%siteUrl)
                return 0

    showMessage("查询结果","最近三天没有新消息发布!")
    return 0

def checkLocalFile(table,siteUrl,filePath):
    firstText = table.find("a").text
    oldTexts = readOldFile(filePath)
    writeNewFile(firstText,filePath)

    if firstText != oldTexts:
        showMessage("最新发布",firstText)
        os.system("firefox %s"%siteUrl)



    return 0


def writeNewFile(contents,filePath):

    with open(filePath,"w",encoding="utf-8") as f:
        f.write(contents)


def readOldFile(filePath):
    with open(filePath,"r") as f:
        contents = f.readline()
        return contents


def showMessage(title,content):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title,content)


def main():

    fileName = "lastCraw.txt"
    dir = os.path.dirname(__file__)
    filePath = os.path.join(dir,fileName)


    siteUrl = "http://www.bjjs.gov.cn/tabid/1072/MoreModuleID/10041/MoreTabID/4021/Default.aspx"
    html = getHtml(siteUrl)
    if html == None:
        showMessage('错误','网络出现问题')
        return -1

    table = getTop(html)
    #checkDate(table,siteUrl)
    checkLocalFile(table,siteUrl,filePath)

    return 0

if __name__ =="__main__":
    main()