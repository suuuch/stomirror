
# coding: utf-8

# In[1]:

import pandas as pd
import requests
import time
from sqlalchemy import create_engine
Engine=create_engine('postgresql://grey:123456@localhost:5432/capital')


# In[4]:

def get_marketview():
    url='http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=5000&type=query'
    r=requests.get(url)
    data1=r.text
    #print(data1)
    data2=eval(data1)
    df=pd.DataFrame([i for i in data2['list']])
    df["TIME"]=data2['time']
    df['TOTAL']=data2['total']
    df_x=pd.DataFrame.from_dict(i for i in df['MFRATIO'])
    df_x['CODE']=df.CODE
    df= df.drop(['ANNOUNMT','UVSNEWS','SNAME','MFRATIO',"NO",'YESTCLOSE','SYMBOL','WB','UPDOWN','TOTAL'],1)
    fin=pd.merge(df,df_x)
    fin=fin.fillna(True)
    fin[["MCAP","TCAP",'MFRATIO10','MFRATIO2','TURNOVER']]=fin[["MCAP","TCAP",'MFRATIO10','MFRATIO2','TURNOVER']]/100000000
    fin[["HS","PERCENT",'FIVE_MINUTE']]=fin[["HS","PERCENT",'FIVE_MINUTE']]*100    
    fin.columns=['code','five_minute','high','hs','lb','low','floatcap','eps','name','open','pe','percent','price','marketcap','turnover','volume','zf','time','revenue','netprofit']
    fin.to_sql('nemarketview',Engine,if_exists='append')
    selectionone=fin[(fin.five_minute>0) & (fin.lb>4) & (fin.percent>2)]
    selectionone.to_sql('nemarketview_selectionone',Engine,if_exists='append')
    print(selectionone)
    


# In[8]:

def runfunc():
    
    while True:
        print(time.ctime())
        get_marketview()
        time.sleep(60)
        print(time.ctime())
    
runfunc()


# In[ ]:



