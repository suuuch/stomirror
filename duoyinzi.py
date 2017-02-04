# encoding: utf-8
from database_conn import Engine
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import math

sql = " select t.*, EXTRACT(year FROM date::date) as yr ,EXTRACT(quarter FROM date::date) as qr from investment.t_stock_front t where symbol = 'sh600779' "

trade_df = pd.read_sql(sql, Engine)

def get_sr(df, column_name = 'close'):
    df['dailyret'] = ( df[column_name].shift(-1) - df[column_name] ) / df[column_name]
    df['excessRet'] = df['dailyret'] - 0.04/252
    return math.sqrt(252) * df['excessRet'].mean() / df['excessRet'].std()
    


trade_series = trade_df.groupby(['yr','qr']).apply(get_sr)
trade_df = trade_series.to_frame()
trade_df.columns=['IR']

report_sql = '''
select t.item_key,t.item_value, EXTRACT(year FROM date::date) as yr ,EXTRACT(quarter FROM date::date) as qr  
from investment.t_163_data t where symbol = '600779' and date > '2011-12-31' order by date 
'''

report_df = pd.read_sql(report_sql, Engine)
report_df = report_df.pivot_table(index = ['yr','qr'] , columns = 'item_key', values= 'item_value')

df = trade_df.join(report_df)

df = df.fillna(0)

df['is_train'] = np.random.uniform(0, 1, len(df)) <= 1

#train, test = df[df['is_train']==True], df[df['is_train']==False]
train = df

features = df.columns[1:]
clf = RandomForestClassifier(n_jobs=2)
y, _ = pd.factorize(train['IR'])
clf.fit(train[features], y)

#preds = iris.target_names[clf.predict(test[features])]
#pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])

importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
item_name_sql= ' select id,group_id,group_name from investment.t_163_item '
item_df = pd.read_sql(item_name_sql, Engine)

print("Feature ranking:")

for f in range(train[features].shape[1]):
    item_df[item_df['id'] == indices[f]][['group_id','group_name']]
    print("%d. feature %d ,%s ,%s , (%f)" % 
          (f + 1, 
           indices[f], 
           item_df[item_df['id'] == indices[f]][['group_id']].values[0][0],
            item_df[item_df['id'] == indices[f]][['group_name']].values[0][0],
           importances[indices[f]]
          )
          )

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(train[features].shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(train[features].shape[1]), indices)
plt.xlim([-1, train[features].shape[1]])
plt.show()