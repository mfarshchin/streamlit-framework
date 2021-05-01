# herkou address: https://mfarshchin-tdi.herokuapp.com
import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
import os
import plotly.express as px

st.title('TDI Milestone Example')
st.write('An interactive chart of stock closing prices using Streamlit and Plot.ly.')
# streamlit side bar
st.sidebar.title('Select plot parameters:')
ticker = st.sidebar.text_input("Ticker (e.g. AAPL):")
year = st.sidebar.selectbox('Year',('<Select>','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020'))
month = st.sidebar.selectbox('Month',('<Select>','January','February','March','April','May','June','July','August','September','October','November','December'))


def get_stock_data(ticker, year, month):
    key = os.getenv('API_KEY')
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}&outputsize=full'.format(ticker, key)
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'],orient="index")
    df = df.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close'})
    # convert index to datetime
    df.index = pd.to_datetime(df.index)
    # filetr for year and month and return results
    # convert month name to int
    month_dict = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    return df.loc[(df.index.year == int(year)) & (df.index.month == month_dict[month]), ['open', 'high', 'low', 'close']]
    
# plot the results with plotly
def plot_stock_price(df, ticker, year, month):
    fig = px.line(df['close'])
    fig.update_layout(
        title=f"{ticker}: {month} {year}",
        xaxis_title="timestamp",
        yaxis_title="close",
        showlegend=False)
    return fig


try:
    df = get_stock_data(ticker, int(year), month)
    fig = plot_stock_price(df, ticker, int(year), month)
    st.plotly_chart(fig)
except:
    pass