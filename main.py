import streamlit as st
import numpy as np
import time
import pandas
from collections import defaultdict

st.write('Dividend Tracker')

def getYearFromTime(time):
    timeio = time.split()
    YYYYMMDD = timeio[0].split('-')
    
    return int(YYYYMMDD[0])

def getMonthFromTime(time):
    timeio = time.split()
    YYYYMMDD = timeio[0].split('-')
    
    return int(YYYYMMDD[1])

def getDayFromTime(time):
    timeio = time.split()
    YYYYMMDD = timeio[0].split('-')
    
    return int(YYYYMMDD[2])

tickerTotal = defaultdict(float)
divvies = {}
df = pandas.read_csv('from_2024-05-01_to_2024-12-13.csv')

for index, row in df.iterrows():
    tickerTotal[row['Ticker']] += row['Total']
    
    month = getMonthFromTime(row['Time'])
    day = getDayFromTime(row['Time'])
    year = getYearFromTime(row['Time'])
    
    if year in divvies:
        if month in divvies[year]:
            if day in divvies[year][month]:
                if row['Ticker'] in divvies[year][month][day]:
                    # multiple payment scenario
                    print('multiple payment issue')
                else:
                    divvies[year][month][day][row['Ticker']] = {
                        'name': row['Name'],
                        'time': row['Time'],
                        'total': row['Total']
                    }
            else:
                divvies[year][month][day] = {
                        row['Ticker']: {
                            'name': row['Name'],
                            'time': row['Time'],
                            'total': row['Total']
                        }
                }
        else:
            divvies[year][month] = {
                    day: {
                        row['Ticker']: {
                            'name': row['Name'],
                            'time': row['Time'],
                            'total': row['Total']
                        }
                    }
                }
    else:
        divvies[year] = {
            month: {
                day: {
                    row['Ticker']: {
                        'name': row['Name'],
                        'time': row['Time'],
                        'total': row['Total']
                    }
                }
            }
        }
        

#print(tickerTotal)

totalVal = 0
for k, v in tickerTotal.items():
    totalVal += v
    
#print(round(totalVal, 2))

st.write('Total', round(totalVal, 2))
st.bar_chart(tickerTotal)

st.write(divvies)
st.button("Re-run")