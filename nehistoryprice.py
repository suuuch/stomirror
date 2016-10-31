# coding: utf-8
"""
reference url:
http://quotes.money.163.com/hs/service/marketradar_ajax.php?page=0&query=STYPE%3AEQA&types=&count=28&type=query&order=desc
query string:
page:0
query:STYPE:EQA
types:
count:28
type:query
order:desc
沪深A股:EQA
沪市A股:EQA_EXCHANGE_CNSESH -> EQA;EXCHANGE;CNSESH
深市A股:EQA_EXCHANGE_CNSESZ -> EQA;EXCHANGE;CNSESZ
fiddle: %2C is ,
http://quotes.money.163.com/hs/service/diyrank.php?page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query HTTP/1.1
simple:
http://quotes.money.163.com/hs/service/diyrank.php?page=0&query=STYPE%3AEQA%3BEXCHANGE%3ACNSESH&fields=NO,SYMBOL,NAME,PRICE,YESTCLOSE,OPEN,FIVE_MINUTE&sort=NO&order=desc&count=24&type=query
http://quotes.money.163.com/hs/service/diyrank.php?page=0&query=STYPE:EQA;EXCHANGE;CNSESH&fields=NO,SYMBOL,NAME,PRICE,YESTCLOSE,OPEN,FIVE_MINUTE&sort=SYMBOL&order=asc&count=24&type=query
sort=SYMBOL
163
日内实时盘口（JSON）：
http://api.money.126.net/data/feed/1000002,1000001,1000881,0601398,money.api
历史成交数据（CSV）：
http://quotes.money.163.com/service/chddata.html?code=0601398&start=20000720&end=20150508
财务指标（CSV）：
http://quotes.money.163.com/service/zycwzb_601398.html?type=report
资产负债表（CSV）：
http://quotes.money.163.com/service/zcfzb_601398.html
利润表（CSV）：
http://quotes.money.163.com/service/lrb_601398.html
现金流表（CSV）：
http://quotes.money.163.com/service/xjllb_601398.html
杜邦分析（HTML）：
http://quotes.money.163.com/f10/dbfx_601398.html
"""

import requests
import re
import datetime
import urllib
import pandas as pd
import numpy as np
import io, sys, functools
from multiprocessing import Pool
from database_conn import Engine

def get163stocklist():
    stocklist163 = []
    url='http://quote.eastmoney.com/stocklist.html#sh'
    r=requests.get(url)
    data=re.findall(r'\([036][0-9]{5}\)',r.text)
    data=[i[1:-1] for i in data]
    print('data length is',len(data))
    print('unique data length is',len(set(data)))
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
    return stocklist163

exceptlist=[]

def get163history(startdate, code):
    try:
        print(code)
        downloadurl='http://quotes.money.163.com/service/chddata.html?code='+code+'&start='+ startdate +'&end='+datetime.datetime.today().strftime("%Y%m%d")+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        s=requests.get(downloadurl).content
        xl=pd.read_csv(io.StringIO(s.decode('gb18030')))
        #xl = pd.read_csv(downloadurl, sep=",", encoding='utf-8')
        xlx=xl.replace('None',np.nan)
        xlx.columns=['date','code','name','close','high','low','open','preclose','change','pctchange','turnover','volume',
                    'amount','cap','floatcap']

    except Exception as e:
        exceptlist.append(code[1:])
        print('exception',code[1:])
        pass
    else:
        if xlx is not None:
            xlx.code=code[1:]
            for i in xlx.columns[3:]:
                xlx[i]=xlx[i].astype(float)
            xlx["downloaddate"]=datetime.datetime.today().strftime('%Y-%m-%d')
            xlx['downloadtime']=datetime.datetime.today().strftime('%H:%M:%S')
            xlx.to_sql('nehistoryprice',Engine,if_exists='append')
            #print(xlx)

        if xlx is None:
            print(code[1:], 'is None')


if __name__ == '__main__':
    try:
        startdate = sys.argv[1]
    except IndexError as e:
        startdate = '19900101'

    history_data_func = functools.partial(get163history, startdate)
    stocklist163 = get163stocklist()

    print(datetime.datetime.today())
    pool=Pool(2)
    pool.map(history_data_func,stocklist163)
    print(datetime.datetime.today())

