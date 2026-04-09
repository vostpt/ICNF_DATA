# -*- coding: utf-8 -*-


# This script is intended to run only once

# Import required libraries
import pandas as pd
import os
import glob
import plotly.express as px
import datetime 


# Use glob to collect all CSV files in the current folder
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))


li = []

for filename in csv_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)


#print(df.info())

frame = pd.concat(li, axis=0, ignore_index=True)

frame.reset_index()  


frame = frame.drop(['Unnamed: 0'], axis = 1)

frame = frame.sort_values(["ANO", "MES", "DIA"], ascending=True)

frame.to_csv('ICNF_2013_2022_full.csv',index=False)




 