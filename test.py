import csv
import pandas as pd
import mysql.connector as mysql
import matplotlib.pyplot as plt
from tabulate import tabulate
import plotly.express as px







mydb = mysql.connect(host='cloudprojects-mysqlserver.mysql.database.azure.com',
    user='flszhwhgye',
    password='5Q36145E87LWYMIQ$',
    db='homeworkcc')
cursor = mydb.cursor()

hshd_num_filter = input("Enter HSHD_NUM filter:")
print("the HSHD no: " + hshd_num_filter)


print("\nTable of top 10 entries based on HSHD_NUM selected by the user \n")

query = ("select t.PRODUCT_NUM,t.BASKET_NUM,t.HSHD_NUM,t.PURCHASE_,t.SPEND,t.UNITS,t.STORE_R,t.WEEK_NUM,t.YEAR,p.DEPARTMENT,p.COMMODITY,p.BRAND_TY,p.NATURAL_ORGANIC_FLAG,h.L,h.AGE_RANGE,h.MARITAL,h.INCOME_RANGE,h.HOMEOWNER,h.HSHD_COMPOSITION,h.HH_SIZE,h.CHILDREN \
    from homeworkcc.transactions as t \
    inner join homeworkcc.products as p on t.PRODUCT_NUM=p.PRODUCT_NUM \
    inner join homeworkcc.households as h on t.HSHD_NUM = h.HSHD_NUM \
    where t.HSHD_NUM = "+ hshd_num_filter+" limit 10")

cursor.execute(query)
result = cursor.fetchall()
df = pd.DataFrame(result, columns=['PRODUCT_NUM','BASKET_NUM','HSHD_NUM','PURCHASE_','SPEND','UNITS','STORE_R','WEEK_NUM','YEAR','DEPARTMENT','COMMODITY','BRAND_TY','NATURAL_ORGANIC_FLAG','L','AGE_RANGE','MARITAL','INCOME_RANGE','HOMEOWNER','HSHD_COMPOSITION','HH_SIZE','CHILDREN'])
for x in df:
    df.add(df)
cursor.close()


mydb.commit()

print(tabulate(df, headers = ['PRODUCT_NUM','BASKET_NUM','HSHD_NUM','PURCHASE_','SPEND','UNITS','STORE_R','WEEK_NUM','YEAR','DEPARTMENT','COMMODITY','BRAND_TY','NATURAL_ORGANIC_FLAG','L','AGE_RANGE','MARITAL','INCOME_RANGE','HOMEOWNER','HSHD_COMPOSITION','HH_SIZE','CHILDREN'] ))





cursor = mydb.cursor()
query = ("select YEAR,sum(SPEND) as TOTAL_SPEND from homeworkcc.transactions group by YEAR")

cursor.execute(query)
result = cursor.fetchall()
df_2 = pd.DataFrame(result, columns=['YEAR','TOTAL_SPEND'])
for x in df_2:
    df_2.add(df_2)
cursor.close()
mydb.commit()


ax = df_2.plot.bar(x='YEAR', y='TOTAL_SPEND',title = 'Bar graph displaying Total spend per year',rot=0)





cursor = mydb.cursor()
query = ("select p.COMMODITY,sum(t.SPEND) as TOTAL_SPEND from homeworkcc.transactions as t \
    inner join homeworkcc.products as p on t.PRODUCT_NUM=p.PRODUCT_NUM group by p.COMMODITY")
cursor.execute(query)
result = cursor.fetchall()
df_3 = pd.DataFrame(result, columns=['COMMODITY','TOTAL_SPEND'])
for x in df_3:
    df_3.add(df_3)
cursor.close()

ax = df_3.plot.line(x='COMMODITY', y='TOTAL_SPEND', title = 'Line chart showing total spend per commodity',rot=0)






cursor = mydb.cursor()
query = ("select h.INCOME_RANGE,sum(t.SPEND) as TOTAL_SPEND from homeworkcc.transactions as t \
    inner join homeworkcc.households as h on t.HSHD_NUM = h.HSHD_NUM group by h.INCOME_RANGE" )
cursor.execute(query)

result = cursor.fetchall()
df_4 = pd.DataFrame(result, columns=['INCOME_RANGE','TOTAL_SPEND'])
for x in df_4:
    df_4.add(df_4)
cursor.close()
mydb.commit()


ax = df_4.plot.line(x='INCOME_RANGE', y='TOTAL_SPEND',title = 'Line chart showing total spend per Income range',rot=0)      



cursor = mydb.cursor()
query = ("select h.HOMEOWNER,sum(t.SPEND) as TOTAL_SPEND from homeworkcc.transactions as t \
    inner join homeworkcc.households as h on t.HSHD_NUM = h.HSHD_NUM group by h.HOMEOWNER" )
 
cursor.execute(query)
result = cursor.fetchall()
df_5 = pd.DataFrame(result, columns=['HOMEOWNER','TOTAL_SPEND'])
for x in df_5:
    df_5.add(df_5)
cursor.close()
mydb.commit()


ax = df_5.plot.bar(x='HOMEOWNER', y='TOTAL_SPEND',title ='Bar chart showing total spend per Homewoner', rot=0)