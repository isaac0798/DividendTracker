import streamlit as st
import numpy as np
import time
import pandas
from collections import defaultdict

st.write('Dividend Tracker')

tickerTotal = defaultdict(float)
df = pandas.read_csv('from_2024-05-01_to_2024-12-13.csv')

for index, row in df.iterrows():
    tickerTotal[row['Ticker']] += row['Total']

#print(tickerTotal)

totalVal = 0
for k, v in tickerTotal.items():
    totalVal += v
    
#print(round(totalVal, 2))

st.write('Total', round(totalVal, 2))

print(df)

options = ["North", "East", "South", "West"]
selection = st.pills("Directions", options, selection_mode="multi")
st.markdown(f"Your selected options: {selection}.")

st.bar_chart(tickerTotal)
st.button("Re-run")
