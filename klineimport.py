# encoding: utf-8
import re

__author__ = 'airsen'

import json
import sys
import datetime

import httplib2
import pymysql

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

def main():
    symbol = input('下载K线数据，股票代码:')
    pattern = re.compile(r'\d{6}')
    match = pattern.search(symbol)
    simplesymbol = match.group()

    accesstoken = 'access_token=Pm0HVhQUxPHTd0osDjwJ4Y&_=1393950527823'
    h = httplib2.Http('.cache')
    resp, content = h.request(
        'http://xueqiu.com/stock/forchartk/stocklist.json?period=1day&type=before&' + accesstoken + '&symbol=' + symbol)

    klinejson = json.loads(str(content, 'utf-8'))

    chartlist = klinejson['chartlist']
    print('总长度为:' + str(len(chartlist)))

    conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='investment',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute('DELETE FROM T_K_LINE WHERE SYMBOL = \'' + simplesymbol + '\'')  # 删除

    insertsql = 'INSERT INTO T_K_LINE VALUES '
    insertvalues = ''

    for chart in chartlist:
        insertvalues += '(\'' + simplesymbol + '\',\'' + str(
            datetime.datetime.strptime(chart['time'], '%a %b %d %H:%M:%S +0800 %Y')) + '\',' + str(
            chart['open']) + ',' + str(
            chart['close']) + ',' + str(chart['high']) + ',' + str(chart['low']) + ',' + str(chart['chg']) + ',' + str(
            chart['percent']) + ',' + str(chart['turnrate']) + ',' + str(chart['ma5']) + ',' + str(
            chart['ma10']) + ',' + str(chart['ma20']) + ',' + str(chart['ma30']) + '),'
    cur.execute(insertsql + insertvalues[:-1])
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    sys.exit(main())
