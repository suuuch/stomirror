# encoding: utf-8
import shutil

__author__ = 'airsen'
import os, requests, csv, re, sys, psycopg2
import httplib2
import pandas as pd
from database_conn import pg_conn

isremovecsv = False  # 是否删掉CSV文件
reporttype = {'利润表': {'url': 'http://quotes.money.163.com/service/lrb_%s.html'},
              '主要财务指标': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html'},
              '资产负债表': {'url': 'http://quotes.money.163.com/service/zcfzb_%s.html'},
              '财务报表摘要': {'url': 'http://quotes.money.163.com/service/cwbbzy_%s.html'},
              '盈利能力': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=ylnl'},
              '偿还能力': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=chnl'},
              '成长能力': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=cznl'},
              '营运能力': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=yynl'},
              '现金流量表': {'url': 'http://quotes.money.163.com/service/xjllb_%s.html'}}

itemtype = {}  # 类目
reportlist = []
h = httplib2.Http('.cache')

db = pg_conn()
cur = db.get_cur()


def download_files_again(function):
    RETRIES = 0
    #重试的次数
    count = {"num": RETRIES, 'symbol': ''}
    def wrapped(*args, **kwargs):
        try:
          return function(*args, **kwargs)
        except Exception as err:
            if count['symbol'] != args[0]:
                count['num'] = RETRIES
                count['symbol'] = args[0]
            print(count)
            if count['num'] > 9:
                raise Exception(err)
            else:
                count['num'] += 1
                download(args[0], args[1])
                return wrapped(*args, **kwargs)
    return wrapped

# @download_files_again
def insert_data_to_database(symbol, reportname, filename):
    executesql = 'INSERT INTO investment.t_163_data VALUES '

    # 读取 csv
    csvreader = csv.reader(open(filename, 'r', encoding='gb18030'))
    for row in csvreader:
        for index, value in enumerate(row):
            print(index)
            exit()
            if value.strip() == '':
                continue
            if row[0].strip() == '报告日期' or row[0].strip() == '报告期':
                if index != 0:
                    profit = {'date': value}  # 创建并加入到列表中
                    reportlist.append(profit)
            else:
                if index != 0 and index <= len(reportlist):
                    try:
                        value = float(value)
                    except ValueError:
                        value = 0
                    reportlist[index - 1][str(row[0].strip())] = str(value)

    # 存库
    values_list = []
    for report in reportlist:
        values = "('%s', '%s', '%%s' ,%%s)" % (symbol, report['date'])
        for key, item in report.items():
            if key != 'date':
                values_list.append(values % (key, item))

    print(symbol + '导入' + reportname + '数据:' + str(len(reportlist)))

    return  executesql + ','.join(values_list)


def download(symbol, reportname):
    if not os.path.exists('csv/' + symbol):
        os.makedirs('csv/' + symbol)
    # 下载文件
    resp, content = h.request(reporttype[reportname]['url'] % symbol)
    print(reporttype[reportname]['url'] % symbol)
    filename = 'csv/' + symbol + '/' + reportname + '.csv'
    profitfile = open(filename, 'wb+')
    profitfile.write(content)
    profitfile.close()


def main(joozy):

    # joozy = input('下载网易股票财报，股票代码:')
    # joozy = '600779'
    pattern = re.compile(r'(\d{6})')
    match = pattern.findall(joozy)
    print('下载网易股票财报，股票代码:' + joozy)
    if len(match) == 0:
        pass
    else:
        for symbol in match:
            print('# --------------------------------------------')
            cur.execute('DELETE FROM investment.t_163_data WHERE SYMBOL = \'' + symbol + '\'')
            for i in reporttype:
                # 下载财报
                # download(symbol, i)
                # 导入财报
                filename = 'csv/' + symbol + '/' + i + '.csv'
                print(filename)
                executesql = insert_data_to_database(symbol, i, filename)
            if isremovecsv:
                shutil.rmtree('csv/' + symbol)
            if len(executesql) > 41:
                cur.execute(executesql)
                print(cur.rowcount)



def get163stocklist():
    stocklist163 = []
    url='http://quote.eastmoney.com/stocklist.html#sh'
    r=requests.get(url)
    data=re.findall(r'\([036][0-9]{5}\)',r.text)
    data=[i[1:-1] for i in data]
    print('data length is',len(data))
    print('unique data length is',len(set(data)))
    for i in data:
        stocklist163.append(i)
    return stocklist163


if __name__ == '__main__':
    # for i in ['600764', '600765', '600766']:
    #     main(i)
    stock_list = get163stocklist()
    # print(list(map(main, stock_list)))
    main('000001')
    # values = insert_data_to_database('000001', '利润表', 'csv/000001/利润表.csv')
    sys.exit()
