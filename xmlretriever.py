# -*- coding: utf-8 -*-

# With thanks to https://stackoverflow.com/users/6792743/perl 

# import libraries

import pandas as pd 
import requests
import xml.etree.ElementTree as ET
import io
from io import StringIO  
import time 

# Get last update 

df_actual=pd.read_csv("icnf_2021_raw.csv")

# XML Query 
# Get data
resp = requests.get(
    'https://fogos.icnf.pt/localizador/webserviceocorrencias.asp?ANO=2021&MES=06')

# Parse XML
et = ET.parse(io.StringIO(resp.text))

# Create DataFrame

df = pd.DataFrame([
    {f.tag: f.text for f in e.findall('./')} for e in et.findall('./')]
)

# Append only new records 

df_actual.append(df[df.isin(df_actual) == False])

# Save to CSV 

df_actual.to_csv("icnf_2021_raw.csv")
