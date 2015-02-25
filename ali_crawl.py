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
import datetime,time


current_path = os.path.dirname(os.path.abspath(__file__))
c_path = current_path + "/showcase.txt"

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

p_index = [];

start = time.time()
linenum = 0;
for lis in lists:
    linenum = linenum + 1;
    for i in range(1,4):
        productlist = []
        p_name = lis[i].strip("\r")
        p_name = re.sub(r' ','_',p_name) 
        for j in range(1,7):
            index_url = root_url + p_name+'/' + str(j)+'.html' 
            productlist.extend(get_productname())
        if lis[0] in productlist:
            p_index.append(str(productlist.index(lis[0])))
        else:
            p_index.append(str(0))

down_path = current_path + "/" +time.strftime("%Y-%m-%d") +"keywordmonitor2.xls"


wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')
ws.write(0,0,u'序号')
ws.write(0,1,u'产品标题')
ws.write(0,2,'K1')
ws.write(0,3,'K2')
ws.write(0,4,'K3')

for i in range(len(lists)):
    ws.write(2*i+1,0,i+1)
    
    ws.write(2*i+1,1,lists[i][0])
    
    ws.write(2*i+1,2,lists[i][1])
    ws.write(2*i+2,2,p_index[i*3])
    
    ws.write(2*i+1,3,lists[i][2])
    ws.write(2*i+2,3,p_index[i*3+1])
    
    ws.write(2*i+1,4,lists[i][3])
    ws.write(2*i+2,4,p_index[i*3+2])
    
wb.save(down_path)
	    

print "Elapsed Time: %s" % (time.time() - start)    


   
