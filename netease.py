
# coding: utf-8

# In[1]:

import requests
import re
import datetime
import urllib
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
Engine=create_engine("postgresql://shaw:123456@127.0.0.1:5432/shawdb")
from multiprocessing import Pool



stocklist163=[]
def get163stocklist():
    url='http://quotes.money.163.com/hs/service/marketradar_ajax.php?page=0&query=STYPE%3AEQA&types=&count=3000&type=query&order=desc'
    r=requests.get(url)
    data=re.findall(r'"SYMBOL":"[0-9]{6}"',r.text)
    data=re.findall("[603][0][0-9]{4}",str(data))


    for i in data:
        if i[0]=="6":
            i='0'+i
            stocklist163.append(i)
        elif i[0]=="3":
            i= '1'+i
            stocklist163.append(i)
        elif i[0]=="0":
            i= '1'+i
            stocklist163.append(i)

get163stocklist()     


# In[5]:

def get163history(code):
    downloadurl='http://quotes.money.163.com/service/chddata.html?code='+code+'&start=19900101&end='+datetime.datetime.today().strftime("%Y%m%d")+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    urllib.urlretrieve(downloadurl,'trade_csv/'+code[1:]+'.xls')
    xl = pd.read_csv('trade_csv/'+code[1:]+'.xls', sep=",", encoding='gb2312')
    xlx=xl.replace('None',np.nan) 
    for i in xlx.columns[3:]:
        xlx[i]=xlx[i].astype(float)
    if xlx.values is None:
        print(code[1:],'is of NoneValue, passed')
        pass

    if xlx.values is not None:
        xlx.to_sql('nehistorypricetest',Engine,if_exists='append')
    



# print(datetime.datetime.today())
# pool=Pool(2)
# pool.map(get163history,stocklist163)
# print(datetime.datetime.today())

map(get163history, stocklist163)
# In[ ]:



