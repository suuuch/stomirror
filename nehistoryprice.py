
# coding: utf-8

# In[ ]:

import requests
import re
import datetime
import urllib
import pandas as pd
import numpy as np
import io
from sqlalchemy import create_engine
Engine=create_engine("postgresql://grey:123456@localhost:5432/capital")
from multiprocessing import Pool


# In[ ]:

stocklist163=[]
def get163stocklist():
    url='http://quotes.money.163.com/hs/service/marketradar_ajax.php?page=0&query=STYPE%3AEQA&types=&count=3000&type=query&order=desc'
    r=requests.get(url)
    data=re.findall(r'"SYMBOL":"[0-9]{6}"',r.text)
    data=re.findall("[603][0-9]{5}",str(data))


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


# In[ ]:

errorlist=[]
exceptlist=[]

def get163history(code):
    
    try:
        
        downloadurl='http://quotes.money.163.com/service/chddata.html?code='+code+'&start=19900101&end='+datetime.datetime.today().strftime("%Y%m%d")+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        s=requests.get(downloadurl).content
        xl=pd.read_csv(io.StringIO(s.decode('gb2312')))
        #xl = pd.read_csv(downloadurl, sep=",", encoding='utf-8')
        xlx=xl.replace('None',np.nan)
        xlx.columns=['date','code','name','close','high','low','open','preclose','change','pctchange','turnover','volume',
                    'amount','cap','floatcap']
        
    except Exception as e:
        
        exceptlist.append(code[1:])
        print('exception',code[1:])
        print(e.message, e.args)
        pass
    
    else:
        
        if xlx is not None:
            
            xlx.code=code[1:]
            for i in xlx.columns[3:]:
                xlx[i]=xlx[i].astype(float)
            xlx["downloaddate"]=datetime.datetime.today().strftime('%Y-%m-%d')
            xlx['downloadtime']=datetime.datetime.today().strftime('%H:%M:%S')
            xlx.to_sql('nehistoryprice',Engine,if_exists='append')
            
        if xlx is None:
            print(code[1:] 'is None')
            


# In[ ]:

print(datetime.datetime.today())
pool=Pool(4)
pool.map(get163history,stocklist163)
print(datetime.datetime.today())

