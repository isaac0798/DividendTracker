import streamlit as st
import numpy as np
import time
import pandas
from collections import defaultdict

st.write('Dividend Tracker')

uploaded_file = st.file_uploader("Choose a file")

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

if uploaded_file is not None:
    tickerTotal = defaultdict(float)
    divvies = {}
    df = pandas.read_csv(uploaded_file)

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
                            'total': row['Total'],
                            'ticker': row['Ticker']
                        }
                else:
                    divvies[year][month][day] = {
                            row['Ticker']: {
                                'name': row['Name'],
                                'time': row['Time'],
                                'total': row['Total'],
                                'ticker': row['Ticker']
                            }
                    }
            else:
                divvies[year][month] = {
                        day: {
                            row['Ticker']: {
                                'name': row['Name'],
                                'time': row['Time'],
                                'total': row['Total'],
                                'ticker': row['Ticker']
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
                            'total': row['Total'],
                            'ticker': row['Ticker']
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

    yearSelected = st.selectbox(
        "Pick Year",
        divvies.keys(),
    )

    monthSelected = st.selectbox(
        "Pick Month",
        divvies[year].keys(),
    )

    st.write("You selected:", yearSelected, monthSelected)


    monthlyTickerTotal = defaultdict(float)
    def getTotalValuesFromMonth(monthlyDivvies):
        for dailyDivvies in monthlyDivvies:
            for div in monthlyDivvies[dailyDivvies]:
                monthlyTickerTotal[div] = monthlyDivvies[dailyDivvies][div]['total']


    getTotalValuesFromMonth(divvies[yearSelected][monthSelected])

    monthlyVal = 0
    for k, v in monthlyTickerTotal.items():
        monthlyVal += v

    st.write('Total', round(monthlyVal, 2))
    
    def getTotalValueFromDate():
        uptoDivvies = {}
        for year in divvies.keys():
            if year not in uptoDivvies:
                uptoDivvies[year] = {}
            
            if year == yearSelected:
                for month in divvies[year].keys():
                    if month not in uptoDivvies[year]:
                        uptoDivvies[year][month] = {}
            
                    if monthSelected == month:
                        break
                    else:
                        uptoDivvies[year][month] = divvies[year][month]

        return uptoDivvies
                        
    divviesUptoMonth = getTotalValueFromDate()
    startingValueFromMonth = 0
    for year in divviesUptoMonth:
        for month in divviesUptoMonth[year]:
            for day in divviesUptoMonth[year][month].keys():
                for divvie in divviesUptoMonth[year][month][day].keys():
                    startingValueFromMonth += divviesUptoMonth[year][month][day][divvie]['total']
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.write('you started with that month with', round(startingValueFromMonth, 2))
        if startingValueFromMonth == 0:
            st.write('no prev monthly data')
        else:
            st.write('with a monthly increase of: ', round((monthlyVal / startingValueFromMonth) * 100,2))
        st.bar_chart(monthlyTickerTotal)
    with col2:
        monthlyAcc = st.radio(
            "Would you like total increase or percentage for year (includes current month)",
            ["total", "percentage"],
            index=None,
        )

        st.write("You selected:", monthlyAcc)
        st.write("only total works now - percentage percent of total dividends by E.O.M")
        
        monthlyTotals = defaultdict(float)
        percentageTotals = defaultdict(float)
        
        uptoTotalVal = 0
        for month in divvies[yearSelected]:
            val = 0
            pVal = 0
            for day in divvies[year][month].keys():
                for divvie in divvies[year][month][day].keys():
                    val += divvies[year][month][day][divvie]['total']
                    uptoTotalVal += divvies[year][month][day][divvie]['total']
            

            pVal = round((val / uptoTotalVal), 2)
            monthlyTotals[month] = round(val, 2)
            percentageTotals[month] = pVal
        
        if monthlyAcc is None:
            st.bar_chart(monthlyTotals)
        
        if monthlyAcc == 'total':
            st.bar_chart(monthlyTotals)
            
        if monthlyAcc == 'percentage':
            st.bar_chart(percentageTotals)
        
        
    st.button("Re-run")