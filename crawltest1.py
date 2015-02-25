# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 03:25:19 2015

@author: BCI
"""


import requests
import bs4
import datetime,time
from multiprocessing import Pool

root_url = 'http://www.alibaba.com/products/F0/'


#productlist = [];

def get_productname(index_url):
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    templist = []
    for a in soup.select('div.lwrap a[title]'):
        templist.append(a.attrs.get('title'))
    return templist

    
def get_list(root_url):
    urllist = []
    for i in range(1,9):
        urllist.append(root_url+'plush_toy/'+str(i)+'.html')
    return urllist
    
def get_data(root_url):
    pool = Pool(8)
    url_list = get_list(root_url)
    results = pool.map(get_productname,url_list)
    return results
    

if __name__ == '__main__':
    start = time.time()
    results = get_data(root_url)
    print results
    print "Elapsed Time: %s" % (time.time() - start)
