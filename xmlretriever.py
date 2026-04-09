# -*- coding: utf-8 -*-

# With thanks to https://stackoverflow.com/users/6792743/perl

# Import libraries

import pandas as pd 
import requests
import xml.etree.ElementTree as ET
import io
from io import StringIO  
import time 
import datetime

# Get values for the current year, month, and day
dt = datetime.datetime.today()

year = dt.year
month = dt.month
day = dt.day-1 # day stores the previous day

print(year,month,day)

# Define XML query URL based on the date

url = f"https://fogos.icnf.pt/localizador/webserviceocorrencias.asp" \
f"?ANO={year}" \
f"&MES={month}" \
f"&DIA={day}" \


# Load the latest local update

df_actual=pd.read_csv("icnf_2022_raw.csv")

# XML query

# Get data

resp = requests.get(url)

# Parse XML
et = ET.parse(io.StringIO(resp.text))

# Create DataFrame

df = pd.DataFrame([
    {f.tag: f.text for f in e.findall('./')} for e in et.findall('./')]
)

df = df.reset_index()

# Append only new records

df_actual.append(df[df.isin(df_actual) == False])

df_sorted = df_actual.sort_values(["ANO","MES","DIA"])

df_sorted.reset_index()

# Save to CSV

df_sorted.to_csv("icnf_2022_raw.csv",index=False)
