# coding: utf-8
import re

"""
drop table investment.t_stock_front;
create table investment.t_stock_front(
	date varchar(12),
	symbol	varchar(20),
	close double precision,
	percent varchar(20),
	open	double precision,
	high 	double precision,
	low	double precision,
	vol	varchar(46),
	amount varchar(46),
	CONSTRAINT t_stock_front_pkey PRIMARY KEY (symbol, date)
"""
__author__ = 'suuuch'

import requests
import re, functools
import datetime
from bs4 import BeautifulSoup
from database_conn import pg_conn


# http://app.finance.china.com.cn/stock/quote/history_factor.php?code=sz000001&begin_day=2016-01-01&end_day=20161031&direction=front
# http://app.finance.china.com.cn/stock/quote/history_factor.php?code=sz000001&begin_day=2012-01-01&end_day=2012-12-31&direction=front
def get163history(startdate, enddate, code):
    base_url = 'http://app.finance.china.com.cn/stock/quote/history_factor.php?code=%s&begin_day=%s&end_day=%s&direction=front'
    downloadurl = base_url % (code, startdate, enddate)
    page = requests.get(downloadurl)
    page.encoding = 'utf-8'
    content = BeautifulSoup(page.text, 'lxml')
    right_table = content.find('table')
    trs = right_table.find_all('tr')
    values = "(\'" + code + "\','%s', %s, '%s', %s, %s, %s ,'%s' ,'%s' )"
    data = []
    for k, tr in enumerate(trs):
        if k == 0:
            continue
        tds = tr.find_all('td')
        data.append(values % (tuple(map(lambda x:x.text , tds))))
    return data

def insert_data_to_database(startdate, enddate, code):
    db = pg_conn()
    cur = db.get_cur()
    data = get163history(startdate, enddate, code)
    sql = "insert into investment.t_stock_front(symbol, date, close, percent, open, high, low, vol, amount) values"
    final_sql = sql + ','.join(data)
    cur.execute(final_sql)
    return cur.rowcount

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
            i='sh'+i
            stocklist163.append(i)
        elif i[0] in ("3","0" ):
            i= 'sz'+i
            stocklist163.append(i)
    return stocklist163

if __name__ == '__main__':
    stocklist163 = get163stocklist()
    date_list = [('20160101','20161231'),
                 ('20150101','20151231'),
                 ('20140101','20141231'),
                 ('20130101','20131231'),
                 ('20120101','20121231')]

    for code in stocklist163:
        for dt in date_list:
            rowcount = insert_data_to_database(dt[0], dt[1], code)
            print("Code %s Insert Row %s " % (code, rowcount))
