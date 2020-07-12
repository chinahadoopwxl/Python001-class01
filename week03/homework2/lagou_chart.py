from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lagou', charset="utf8")
sql_str = "select * from lagou_position"
df = pd.io.sql.read_sql_query(sql_str, conn)
d = dict(list(df.groupby('city_name')))

citys = []
salarys = []

for city_name in d:
    citys.append(city_name)
    salarys.append(d[city_name]['salary'])

salary_list = [pd.DataFrame(salary)['salary'].dropna() for salary in salarys]
salary_list2 = [salary[salary.str.contains('-')] for salary in salary_list]
salary_list3 = [salary.map(lambda x:x.lower().replace('k','000')) for salary in salary_list2]

# salaryLow_list = [salary.map(lambda x:int(x.split('-')[0])) for salary in salary_list3]
# salaryHigh_list = [salary.map(lambda x:int(x.split('-')[1])) for salary in salary_list3]
salaryAvg_list = [salary.map(lambda x:np.average([int(k) for k in x.split('-')])) for salary in salary_list3]

# 设置切分区域
listBins = [0, 10000, 20000, 30000, 40000, 50000]
# 设置切分后对应标签
listLabels = ['0k_10k','11k_20k','21k_30k','31k_40k','41k_50k']
# 地区标签
tick_labels = {'北京': 'beijing', '上海': 'shanghai', '深圳': 'shenzhen', '广州': 'guangzhou'}
colors = ['#008080', '#E9967A', '#1E90FF', '#FAA460']

l = len(listLabels)
x = [_ for _ in range(l)]

total_width, n = 4, 20
width = total_width / n

for i in range(len(salaryAvg_list)):
    sl = salaryAvg_list[i]
    datas = pd.cut(sl, bins=listBins, labels=listLabels, include_lowest=True)
    datas_df = pd.DataFrame(datas)
    gs = datas_df.groupby('salary').aggregate({'salary':'count'})

    y = [v[0] for v in gs.values]
    plt.bar(x, y, width=width, label= tick_labels[citys[i]], tick_label=listLabels, color=colors[i])
    x = [_ + width for _ in x ]
    
plt.title('Citys Salary Graph') 
plt.legend()
plt.show()