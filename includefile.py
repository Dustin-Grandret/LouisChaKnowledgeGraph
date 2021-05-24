PROJECTROOT=r'F:/课程资料/pythonProject//'
namelistroot=PROJECTROOT+'character.json'
root=PROJECTROOT+'rawdata\\'
saveroot=PROJECTROOT+'rawdata_tran\\'
testcsvroot=PROJECTROOT+'test.csv'
DATAFILE=PROJECTROOT+'triples\\'
PROFILE_ROOT=PROJECTROOT+'docs\test_2.csv'

import re
import json
#载入软件包=====================================
#数据结构
import pandas as pd
import os
import numpy
#爬虫操作
import urllib as url
import urllib.request as urlr
import urllib.error as urle
import urllib.parse as urlp

import urllib3#有些网站需要使用urllib3

#常用模组
import random as rand
import re
import time
import sys
import csv
#csv读写
import csv
from tqdm import tqdm
import codecs
#================================================
#载入资源文件uapools.py
from uapools import uapools
print("库载入成功")
def stop():
    input('asd')
def strongpat(string,patlist,*args):
    rst=[]
    if type(patlist)==dict:
        for elem in patlist.values():
            rst.append(re.compile(elem, *args).findall(string))
    elif type(patlist)==str:
        rst.append(re.compile(patlist,*args).findall(string))
    elif type(patlist)==list:
        for elem in patlist:
            rst.append(re.compile(elem, *args).findall(string))
    else:
        raise TypeError()
    return rst
def getrelation(rawdata):
    df=pd.read_html(rawdata)[0]
    return list(df['人名'])
def getc2i():
    return eval(open('charactername2int.txt','r',encoding='-utf-8').read())
def geti2c():
    return eval(open('../int2charactername.txt', 'r', encoding='-utf-8').read())
def tranchinise(word:str):
    return url.parse.quote(word)
def ua(muapools=uapools,method=0):#传入资源列表中的uapools，里面有1499个标签值可使用
    thisua=rand.choice(muapools)#从uapools中随机使用一个
    #print("当前使用的用户为："+thisua)
    headers=("User-Agent",thisua)#用元组的形式制作头信息，（标签，用户名）
    opener=urlr.build_opener()#使用urlr.build_opener()来获取总的内容
    opener.addheaders=[headers]#添加用户信息
    urlr.install_opener(opener)#安装为全局
def getpage(url,method=0):#ippoolsurl代表接口网址，url代表目标网址
    file=""
    if(method==0):#默认使用urllib方法
        for counts in range(0,9):
            try:
                ua()
                file=urlr.urlopen(url).read().decode('UTF-8',"ignore")
                break
            except urle.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
        #print("爬取成功")
    elif(method==1):#有的时候我们需要使用urllib3的方法
        for counts in range(0,9):
            try:
                http = urllib3.PoolManager()
                thisua=rand.choice(uapools)#从uapools中随机使用一个
                #print("当前使用的用户为："+thisua)
                headers={"User-Agent":thisua}#用字典的形式制作头信息，（标签，用户名）
                r=http.request('GET',url,headers=headers)
                file=(r.data).decode('UTF-8','ignore')
                break
            except urle.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
    return file
if __name__ == '__main__':
    getrelation(open('黄蓉.html','r',encoding='utf-8').read())
    '''with open(PROJECTROOT+'test.html','r',encoding='utf-8') as f:
        for elem in strongpat(f.read(),'<div class="para" label-module="para"><a(.*?)</a>[\s]*</div>',re.S):
            for elem2 in elem:
                print(elem2)'''