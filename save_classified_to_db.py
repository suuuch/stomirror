
# coding: utf-8

# In[ ]:

from sqlalchemy import create_engine
import pandas as pd
import tushare as ts
Engine=create_engine("postgresql://shaw:123456@127.0.0.1:5432/shawdb")


# In[ ]:

#行业分类
df_industry_classified = ts.get_industry_classified()
#概念分类
df_concept_classified = ts.get_concept_classified()
#地域分类
df_area = ts.get_area_classified()
# df_area['classified_type'] = '地域'
# df_area.rename(columns={'area': 'c_name'}, inplace=True)
result = pd.merge(df_industry_classified, df_concept_classified, how='left', on=['code','name'])
result = pd.merge(result, df_area, how='left', on=['code','name'])
result.to_sql('t_classified', Engine, if_exists='append', index =False )

