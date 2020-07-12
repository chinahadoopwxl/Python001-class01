from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lagou', charset="utf8")
sql_str = "select * from lagou_position"
df = pd.io.sql.read_sql_query(sql_str, conn)

g = df.groupby('city_name')
d = dict(list(g))
citys = []
salarys = []

for city_name in d:
    citys.append(city_name)
    salarys.append(d[city_name]['salary'])


salary_list = [pd.DataFrame(salary)['salary'].dropna() for salary in salarys]
salary_list2 = [salary[salary.str.contains('-')] for salary in salary_list]
salary_list3 = [salary.map(lambda x:x.lower().replace('k','000')) for salary in salary_list2]

salaryLow_list = [salary.map(lambda x:int(x.split('-')[0])) for salary in salary_list3]
salaryHigh_list = [salary.map(lambda x:int(x.split('-')[1])) for salary in salary_list3]


l = len(salary_list)

x = []
for i in range(l):
    city_salary_len = len(salary_list[i])
    x.append([_ for _ in range(len(x) * 2 , len(x) * 2 + city_salary_len)])

total_width, n = 0.8, l
width = total_width / n

low = []
high = []

for i in range(l): 
    low.append(salaryLow_list[i])
    high.append(salaryHigh_list[i])

colors = ['b', 'y', 'r', 'g']
tick_labels = {'北京': 'beijing', '上海': 'shanghai', '深圳': 'shenzhen', '广州': 'guangzhou'}
for i in range(len(colors)):
    plt.bar(x[i], salaryLow_list[i], width=width, label= tick_labels[citys[i]] + ' low salary', tick_label=tick_labels[citys[i]], color=colors[i])
    x[i] = [_ + width for _ in x[i] ]
    plt.bar(x[i], salaryHigh_list[i], width=width, label= tick_labels[citys[i]] + ' high salary', tick_label=tick_labels[citys[i]], color=colors[i])

plt.title('citys salary graph') 
plt.legend()
plt.show()