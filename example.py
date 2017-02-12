# encoding: utf-8

from From_WY.datafetch_163 import WYData


wy = WYData()
df  = wy.get_report_type('600779','ylnl')
print(df)