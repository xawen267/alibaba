# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:30:59 2015

@author: BCI
"""
import requests
import bs4
import datetime,time

root_url = 'http://www.alibaba.com/products/F0/'


productlist = [];

def get_productname():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)
    templist = []
    for a in soup.select('div.lwrap a[title]'):
        templist.append(a.attrs.get('title'))
    return templist
#    return [a.attrs.get('title') for a in soup.select('div.lwrap a[title]')]

start = time.time()

for i in range(1,9):
    index_url = root_url + 'plush_toy/'+str(i)+'.html'
    productlist.extend(get_productname())

print productlist
print "Elapsed Time: %s" % (time.time() - start)

