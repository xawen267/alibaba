# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 04:19:27 2015

@author: BCI
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 21:43:36 2015

@author: summerxia
"""

import Queue
import threading
import os
import string
import urllib2
import re
import datetime,time
import xlwt
import requests
import bs4


current_path = os.path.dirname(os.path.abspath(__file__))
c_path = current_path + "/productlist.txt"

root_url = 'http://www.alibaba.com/products/F0/'

def get_productname():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    templist = []
    for a in soup.select('div.lwrap a[title]'):
        templist.append(a.attrs.get('title'))
    return templist

source=open(c_path,"r")
values=source.readlines() 
source.close()
productlist = [];
#values.split('\n')
lists=[]
for i in values:
    #i=i.replace("\n","")
    i=i.strip("\n") 
    a=i.split(';')
    #print len(a)
    if len(a)>1:
        lists.append(a)
print lists

for lis in lists:
    for i in range(1,4):
        p_name = lis[i].strip("\r")
        p_name = re.sub(r' ','_',p_name)
        for j in range(1,7):
            index_url = root_url + p_name+'/' + str(j)+'.html' 
            productlist.extend(get_productname())
        if lis[0] in productlist:
            print productlist.index(lis[0])