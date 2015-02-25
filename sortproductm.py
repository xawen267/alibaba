#-*- coding: utf-8 -*-
import Queue
import threading
import os
import string
import urllib2
import re
import datetime,time
import xlwt
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
        while j<=6:
            shuru=input.encode('gbk')
            shuru1= re.sub(r' ','_',shuru)
            self.wangzhi = "http://www.alibaba.com/products/F0/"+shuru1+'/'+str(j)+'.html'
            self.myPage=urllib2.urlopen(self.wangzhi).read()
            self.deal_name()
            j=j+1        
        return self.namelist

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
c_path = current_path + "/showcase.txt"

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
            if lis[0] in y1:
                z1 = y1.index(lis[0])
                if z1+1<=43:
                    keyword1= str(1)+"*38 + "+str(z1+1)
                else:
                    keyword1= str(1+((((z1+1)-43))/38)+1)+"*38 + "+str(((z1+1)-43)%38)
            else:
                keyword1= "0 page;"
            keywordlist1.append(keyword1)            
            
            mySpider = Baidu_Spider()
            y2=mySpider.output(lis[2])
            if lis[0] in y2:
                z2 = y2.index(lis[0])
                if z2+1<=43:
                    keyword2= str(1)+"*38 + "+str(z2+1)
                else:
                    keyword2= str(1+((((z2+1)-43))/38)+1)+"*38 + "+str(((z2+1)-43)%38)
            else:
                keyword2= "0 page;"
            keywordlist2.append(keyword2)             
            
            mySpider = Baidu_Spider()
            y3=mySpider.output(lis[3])
            if lis[0] in y3:
                z3 = y3.index(lis[0])
                if z3+1<=43:
                    keyword3= str(1)+"*38 + "+str(z3+1)
                else:
                    keyword3= str(1+((((z3+1)-43))/38)+1)+"*38 + "+str(((z3+1)-43)%38)
            else:
                keyword3= "0 page;"
            keywordlist3.append(keyword3)             
            threadLock.release()
            
            self.queue.task_done()    
            
            

start = time.time()
def main():

    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
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
down_path = current_path + "/" +now +"keywordmonitor.xls"

#f=open(down_path,'a')
#for i in range(len(lists)):
    #f.write(lists[i][0]+":"+keywordlist1[i]+keywordlist2[i]+keywordlist3[i]+"\n")
#f.close()
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
    ws.write(2*i+2,2,keywordlist1[i])
    
    ws.write(2*i+1,3,lists[i][2])
    ws.write(2*i+2,3,keywordlist2[i])
    
    ws.write(2*i+1,4,lists[i][3])
    ws.write(2*i+2,4,keywordlist3[i])
    
wb.save(down_path)
