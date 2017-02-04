# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 16:26:39 2016

@author: suuuc
"""

import tushare as ts

basic_data = ts.get_stock_basics()
# 行业总股本排名
df = basic_data.groupby('industry')['outstanding'].agg(['sum']) 