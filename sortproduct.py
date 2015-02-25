#-*- coding: utf-8 -*-
import Queue
import threading
import os
import string
import urllib2
import re
import datetime,time
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n|<a.*?>|<img.*?>)")
    
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&"),("&amp;","\""),("&nbsp;"," "),("&quot","")]
    
    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        #x = self.BgnPartRex.sub("\n    ",x)
        x = self.BgnPartRex.sub("\n    ",x)
        #x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:  
            x = x.replace(t[0],t[1])  
        return x
class Baidu_Spider:
    # 申明相关的属性
    def __init__(self):
        self.rmblist=[]
        self.namelist=[]
        self.myTool = HTML_Tool()
        #self.myPage=urllib2.urlopen(url).read()#.decode("gbk")
        
    def output(self,input):
        j=1
        while j<=20:
            shuru=input.encode('gbk')
            shuru1= re.sub(r' ','_',shuru)
            self.wangzhi = "http://www.alibaba.com/products/F0/"+shuru1+'/'+str(j)+'.html'
            self.myPage=urllib2.urlopen(self.wangzhi).read()
            self.deal_name()
            j=j+1        
        return self.namelist
    
    #def deal_url(self):
        #myItems3 = re.findall('<h2 class="title"><a href="(.*?)" title.*? target="_blank".*?>.*?</a>',self.myPage,re.S)
        #return myItems3
    #def deal_info(self):
        #urls=self.deal_url()
        #for url in urls:
            #myinfo = urllib2.urlopen(url).read()
            #mes = re.findall('>Place of Origin:</span>.*?<div class="ellipsis" title="(.*?)">',myinfo,re.S)
            #print mes
            #mes2 = re.findall('>Material:</span>.*?<div class="ellipsis" title="(.*?)">',myinfo,re.S)
            #if mes2 == []:
                #mes2="无此信息"
            #print mes2

    def deal_name(self):
        myItems1 = re.findall('<h2 class="title"><a href=".*?" title.*? target="_blank".*?>(.*?)</a>',self.myPage,re.S)
        for item1 in myItems1:
            item1 = item1.replace("\n","")
            data = self.myTool.Replace_Char(item1.replace("\n",""))#.encode('gbk'))
            #print data
            self.namelist.append(data)
        

#mySpider = Baidu_Spider()

#mySpider.output("baby toys")


current_path = os.path.dirname(os.path.abspath(__file__))
c_path = current_path + "\productlist.txt"

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


keywordlist1=[]
keywordlist2=[]
keywordlist3=[]
queue = Queue.Queue()
global threadLock
threadLock = threading.Lock()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            
            lis = self.queue.get()
            
            threadLock.acquire()
            mySpider = Baidu_Spider()
            y1=mySpider.output(lis[1])
            z1 = y1.index(lis[0])
            keyword1= lis[1]+","+str(z1/43+1)+"page and "+str(z1%43)+"lines;"
            keywordlist1.append(keyword1)            
            
            mySpider = Baidu_Spider()
            y2=mySpider.output(lis[2])
            z2 = y2.index(lis[0])
            keyword2= lis[2]+","+str(z2/43+1)+"page and "+str(z2%43)+"lines;"
            keywordlist2.append(keyword2)             
            
            mySpider = Baidu_Spider()
            y3=mySpider.output(lis[3])
            z3 = y3.index(lis[0])
            keyword3= lis[3]+","+str(z3/43+1)+"page and "+str(z3%43)+"lines;"
            keywordlist3.append(keyword3)             
            threadLock.release()
            
            self.queue.task_done()    
            
            

start = time.time()
def main():

    #spawn a pool of threads, and pass them queue instance
    for i in range(10):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for lis in lists:
        queue.put(lis)

    #wait on the queue until everything has been processed
    queue.join()
    
main()
print "Elapsed Time: %s" % (time.time() - start)

now = time.strftime("%Y-%m-%d")        
down_path = current_path + "/" +now +"keywordmonitor.txt"

f=open(down_path,'a')
for i in range(len(lists)):
    f.write(lists[i][0]+":"+keywordlist1[i]+keywordlist2[i]+keywordlist3[i]+"\n")
f.close()


