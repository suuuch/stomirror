# encoding: utf-8
from database_conn import Engine
import pandas as pd
import math

sql = " select t.*, EXTRACT(year FROM date::date) as yr ,EXTRACT(quarter FROM date::date) as qr from investment.t_stock_front t where symbol = 'sh600779' "

df = pd.read_sql(sql, Engine)

def get_sr(df, column_name = 'close'):
    df['dailyret'] = ( df[column_name].shift(-1) - df[column_name] ) / df[column_name]
    df['excessRet'] = df['dailyret'] - 0.04/252
    return math.sqrt(252) * df['excessRet'].mean() / df['excessRet'].std()
    

grouped_count = df.groupby(['yr','qr']).apply(get_sr)