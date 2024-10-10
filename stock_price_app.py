import yfinance as yf
import pandas as pd
import streamlit as st

st.write(
"""
# Simple Stock Price App
Shown are the stock closing price and volume of Google
"""
)

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

st.header('Stock Closing Price')
st.line_chart(tickerDf.Close)
st.write(
"""
***
"""
)
st.header('Stock Volume Price')
st.line_chart(tickerDf.Volume)