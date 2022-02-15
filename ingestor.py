# import necessary libraries
import pandas as pd
import os
import glob
import plotly.express as px
import datetime 


# use glob to get all the csv files
# in the folder
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))


li = []

for filename in csv_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.reset_index()

df_sorted = frame.sort_values(["ANO", "MES", "DIA"])


df_heatmap = df_sorted.groupby(['ANO','DISTRITO','CONCELHO'])[['NCCO']].nunique().reset_index()



#df_heatmap['DATAALERTA']=pd.to_datetime(df['DATAALERTA'])

#print(df_heatmap.info())

df_heatmap.to_csv('heatmap_full.csv')




#events_year = df_sorted.groupby(["DATAALERTA","ANO","DISTRITO"])[["NCCO"]].nunique().reset_index()

#events_year['ANO']=events_year['ANO'].astype(str)





#print(events_year)

#fig = px.bar(events_year,x='ANO',y='NCCO',color='ANO')
#fig.show()
