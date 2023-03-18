import pandas as pd 
import numpy as np 
import streamlit as st 
import plotly.express as px 

## Read the data
@st.cache
df=pd.read_excel('DATA\month_data_hospital.xlsx')

# preprocessing the data 
df.columns=df.columns.str.strip()

df['REVENUES CATEGORY']=df['REVENUES CATEGORY'].str.replace(" ","")

# convert the date to a date time format
df['DATE']=pd.to_datetime(df['DATE'])
#extract the month name 
df['MONAT']=df['DATE'].dt.month_name()

st.title('HOSPITAL PERFORMANCE DASHBOARD')