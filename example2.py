# coding: utf-8
from From_WY.datafetch_163 import WYData
import pandas as pd
import numpy as np
#pandas 入库参数
from sqlalchemy import create_engine
Engine=create_engine("postgresql://shaw:123456@127.0.0.1:5432/shawdb")

def insert_data_to_pg(code):
    wy = WYData()
    rst = delete_old_data_from_pg(code)
    print('Delete Code : %s ,Delete  Row Count is :%s' % (code, rst))
    report_type_list = {'lrb': '利润表',
                        'zycwzb': '主要财务指标',
                        'zcfzb': '资产负债表',
                        'cwbbzy': '财务报表摘要',
                        'ylnl': '盈利能力',
                        'chnl': '偿还能力',
                        'cznl': '成长能力',
                        'yynl': '营运能力',
                        'xjllb': '现金流量表'}
    for (report_type, report_name) in report_type_list.items():
        df  = wy.get_report_type(code, report_type)
        df.index = df.index.rename('report_date')
        df['code'] = code
        df['report_name'] = report_name
        df = df.set_index(['code','report_name'], append=True).stack()
        df = pd.DataFrame(df,columns=['values'])
        df.to_sql('report_data', Engine, if_exists='append', index =True )

def delete_old_data_from_pg(code):
    sql = "delete from public.report_data where code = '%s' " % code
    rst = Engine.connect().execute(sql).rowcount
    return rst

def get_already_in_code():
    already_in_code = """
            select code,max(report_date) as last_report_date
            from public.report_data
            where report_date > to_char(current_date::timestamp + '-3 month', 'YYYY-MM-DD')
            group by code
        """
    db_already_in_code = pd.read_sql(already_in_code, Engine)
    return list(db_already_in_code['code'])

def get_not_fetch_code():
    not_fetch_code_sql = """
            select distinct code as code
            from public.t_classified t
            where not exists(
            select 1 from public.report_data t1 where t.code = t1.code
            )
        """
    not_fet_code_list = pd.read_sql(not_fetch_code_sql, Engine)
    return list(not_fet_code_list['code'])


def get_all_code():
    db_code = pd.read_sql('SELECT distinct code FROM public.t_classified', Engine)
    return list(db_code['code'])



if __name__ == '__main__':
    from time import sleep
    not_fetch_code = get_not_fetch_code()

    if len(not_fetch_code) > 0:
        db_fetch_code_list = not_fetch_code
    else:
        db_already_in_code_lists = get_already_in_code()
        code_lists = get_all_code()
        db_fetch_code_list = set(code_lists) - set(db_already_in_code_lists)

    for code in db_fetch_code_list:
        insert_data_to_pg(code)
        sleep(3)
