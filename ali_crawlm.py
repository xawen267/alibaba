# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 06:13:45 2015

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
from multiprocessing import Pool




def get_list(root_url,productname):
    urllist = []
    for i in range(1,7):
        urllist.append(root_url+productname +'/'+str(i)+'.html')
    return urllist


    
def get_productname(index_url):
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    templist = []
    for a in soup.select('div.lwrap a[title]'):
        templist.append(a.attrs.get('title'))
    return templist

#def get_data(root_url,pname):
#    pool = Pool(1)
#    url_list = get_list(root_url,pname)
#    print url_list
#    results = pool.map(get_productname,url_list)
#    print results
#    return results
    
def get_data(root_url,pname):
    pool = Pool(6)
    url_list = get_list(root_url,pname)
    results = pool.map(get_productname,url_list)
    outresult = results[0] + results[1] +results[2] +results[3] + results[4] + results[5]
    return outresult
    
if __name__ == '__main__':
    start = time.time()
    current_path = os.path.dirname(os.path.abspath(__file__))
    c_path = current_path + "/showcase.txt"
    
    root_url = 'http://www.alibaba.com/products/F0/'
    
    source=open(c_path,"r")
    values=source.readlines()
    source.close()





#values.split('\n')
    lists=[]
    for i in values:
        i=i.strip("\n") 
        a=i.split(';')
        if len(a)>1:
           lists.append(a)
#        print lists
    r_list = []
    for lis in lists:
        for i in range(1,4):
           p_name = lis[i].strip("\r")
           p_name = re.sub(r' ','_',p_name)
           productlist = get_data(root_url,p_name)
           if lis[0] in productlist:
               r_list = r_list + [productlist.index(lis[0])]
           else:
               r_list = r_list + [0]
            
    print "Elapsed Time: %s" % (time.time() - start)