
# coding: utf-8

# In[1]:

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import numpy as np
import pandas as pd


# In[2]:

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}
url = "http://bj.58.com/job/?key=%252525E6%2525259C%252525BA%252525E5%25252599%252525A8%252525E5%252525AD%252525A6%252525E4%252525B9%252525A0&sourcetype=4"


# In[3]:

html = requests.get(url, headers=head)
selector = etree.HTML(html.text)
content = selector.xpath("//html")


# In[4]:

##find out the header of the website
title = content[0].xpath('//head//title/text()') 
description = content[0].xpath('//head//meta[@name="description"]/@content') 
header = [title[0],description[0]]


# In[5]:

ljob = content[0].xpath('//div[@id = "infolist"]')
##find out job details 
posnum = ljob[0].xpath('//dl/@_pos')
addition = ljob[0].xpath('//dl/@__addition')
sortid= ljob[0].xpath("//dl/@sortid")
expandurl = ljob[0].xpath('//dl/dt/span/@url')
titles = ljob[0].xpath('//dl/dd[@class = "w271"]/a/text()')
location = ljob[0].xpath('//dl/dd[@class = "w96"]/text()')
date = ljob[0].xpath('//dl/dd[@class = "w68"]/text()')


# In[6]:

#transfer String type into numeric value 
posnum = np.array(posnum).astype("int32")
addition = np.array(addition).astype("int32")
sortid = np.array(sortid).astype("int32")
#combine all of the data in dataframe
data = {'titles':titles,'location':location,'date':date,'posnum':posnum,'addition':addition,'jobid':sortid,"website":expandurl}
dataset = pd.DataFrame(data)
dataset = dataset[['titles','location','date','jobid','addition','posnum','website']]


# In[28]:

#relevant infomation
length = len(expandurl)
JdesC = []
CintroC = []
titleC = []
desC = []
for ele in expandurl:
    html = requests.get(ele, headers=head)
    selector = etree.HTML(html.text)
    content = selector.xpath("//html")
    ##find out the header of the website
    title = content[0].xpath('//head//title/text()') 
    description = content[0].xpath('//head//meta[@name="description"]/@content')
    titleC.append(title[0])
    desC.append(description[0])
    Jdes = content[0].xpath('//div[@class = "des"]/text()')
    Jdes = [x.strip(' ') for x in Jdes]
    Jdes = "".join("".join(Jdes).split("\t"))
    JdesC.append(Jdes)
    Cintro = content[0].xpath('//div[@class = "shiji"]/p/text()')
    Cintro = [x.strip(' ') for x in Cintro]
    Cintro = "".join("".join(Cintro).split("\t"))
    Cintro = "".join(Cintro.split('\r'))
    CintroC.append(Cintro)


# In[29]:

datanew = {"company title":titleC,"Introduction of the company":desC,"Corporate Culture" :CintroC,"job details":JdesC}
datasetnew = pd.DataFrame(datanew)
datasetnew = datasetnew[["company title","Introduction of the company","Corporate Culture","job details"]]
datasetnew


# In[30]:

#combine all result together
data = {'titles':titles,'location':location,'date':date,'posnum':posnum,'addition':addition,'jobid':sortid,"website":expandurl
       ,"company title":titleC,"Introduction of the company":desC,"Corporate Culture" :CintroC,"job details":JdesC}
dataset = pd.DataFrame(data)
dataset = dataset[['titles','location','date','jobid','addition','posnum','website',"company title","Introduction of the company",
                   "Corporate Culture","job details"]]
dataset


# In[31]:

#output result to excel file
writer = pd.ExcelWriter(r'C:\Users\Administrator\Desktop\output.xlsx')
dataset.to_excel(writer,'Sheet1')
writer.save()

