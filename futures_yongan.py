
# coding: utf-8

# In[1]:

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import datetime
import re
import requests
from bs4 import BeautifulSoup
Engine=create_engine('postgres://grey:123456@localhost:5432/capital')


# In[15]:

def yonganeastmoney(date,mkt):
    
    base_url_sh='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=QHCC&sty=QHSYCC&stat=4&mkt={1}&sc=&cmd=80102901&fd={0}&name=1&cb=callback&callback=callback&_=1478741745452'
    download_url_sh=base_url_sh.format(date,mkt)
    #print(download_url_sh)
    page_sh=requests.get(download_url_sh)
    page_sh.encoding='gb18030'
    sh0=page_sh.text
    sh1=sh0[9:-1]
    sh2=eval(sh1)
    sh3=[i.split(',') for i in sh2]
    df_sh=pd.DataFrame(sh3)
    data.append(df_sh)


# In[46]:

data=[]
date='2016-11-09'

for i in ['069001008','069001005','069001007']:
    yonganeastmoney(date,i)

    df=pd.concat(i for i in data)
df.columns=["合约","结算价（元）","成交量","增减","多单量","多单增减","空单量","空单增减","净多单","净空单"]
df['日期']=date
df=df.set_index('日期')
for i in df.columns[2:]:
    df[i]=df[i].astype(float)
df=df.sort_values('多单增减')
df.to_excel('/home/grey/yongan{0}.xlsx'.format(date))
df.to_sql('yongan',Engine,if_exists='append')

