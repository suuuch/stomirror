
# coding: utf-8

# In[1]:

import pandas as pd
import requests
import time


# In[4]:

def get_marketview():
    url='http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=5000&type=query'
    r=requests.get(url)
    data1=r.text
    #print(data1)
    data2=eval(data1)
    df=pd.DataFrame([i for i in data2['list']])
    df["time"]=data2['time']
    df['total']=data2['total']
    df_x=pd.DataFrame.from_dict(i for i in df['MFRATIO'])
    df_x['CODE']=df.CODE
    df= df.drop(['ANNOUNMT','UVSNEWS','SNAME','MFRATIO',"NO",'YESTCLOSE','SYMBOL'],1)
    fin=pd.merge(df,df_x)
    fin=fin.set_index(['CODE','NAME'])
    fin=fin.fillna(True)
    fin[["MCAP","TCAP",'MFRATIO10','MFRATIO2','TURNOVER']]=fin[["MCAP","TCAP",'MFRATIO10','MFRATIO2','TURNOVER']]/100000000
    fin[["HS","PERCENT",'FIVE_MINUTE']]=fin[["HS","PERCENT",'FIVE_MINUTE']]*100
    fin.to_excel('/home/grey/qq.xlsx')
    selection1=fin[(fin.FIVE_MINUTE>0) & (fin.LB>5) & (fin.PERCENT>2)]
    print(selection1)
    


# In[8]:

def runfunc():
    
    while True:
        print(time.ctime())
        get_marketview()
        time.sleep(60)
        print(time.ctime())
    
runfunc()


# In[ ]:



