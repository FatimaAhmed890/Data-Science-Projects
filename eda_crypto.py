import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from scraper import scrape_data

st.set_page_config(layout='wide')

image = Image.open('Cryptocurrency_web_app.png')
st.write(image)

st.title('Crypto Price App')
st.markdown("""
            This app retrieves cryptocurrency prices of the top 100 cryptocurrency from the **CoinMarketCap!**
            """)
with st.expander('About'):
    st.markdown("""
                * **Python Libraries:** pandas, numpy, streamlit, matplotlib, bs4, base64, requests, json, time
                * **Data Source:** [CoinMarketCap](https://coinmarketcap.com)
                """)
# Divide the page layout
col1 = st.sidebar
col2, col3 = st.columns((2,1))

col1.header("Input Options")

@st.cache_data
def load_data():
    df = scrape_data()
    return df

df = load_data()

sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrencies', sorted_coin, default=['AAVE', 'BTC', 'ETC', 'ETH'])

df_selected_coins = df[(df['coin_symbol'].isin(selected_coin))]
if len(selected_coin) != 0:
    num_coins = col1.slider('Display N coins from selected coins', 1, len(selected_coin), len(selected_coin))
    df_coins = df_selected_coins[:num_coins]

    percent_timeframe = col1.selectbox('Percent change time frame',
                                        ['7d','24h', '1h'])
    percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
    selected_percent_timeframe = percent_dict[percent_timeframe]

    sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])


    col2.subheader('Price Data of Selected Cryptocurrency')
    col2.write('Data Dimension: ' + str(df_selected_coins.shape[0]) + ' rows and ' + str(df_selected_coins.shape[1]) + ' columns.')

    col2.dataframe(df_coins)

    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
        return href

    col2.markdown(filedownload(df_selected_coins), unsafe_allow_html=True)

    # Preparing data for Bar plot of % Price change
    col2.subheader('Table of % Price Change')
    df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
    df_change = df_change.set_index('coin_symbol')
    df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
    df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
    df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
    col2.dataframe(df_change)

    # Conditional creation of Bar plot (time frame)
    col3.subheader('Bar plot of % Price Change')

    if percent_timeframe == '7d':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_7d'])
        col3.write('*7 days period*')
        plt.figure(figsize=(5,25))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    elif percent_timeframe == '24h':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_24h'])
        col3.write('*24 hour period*')
        plt.figure(figsize=(5,25))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
    else:
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_1h'])
        col3.write('*1 hour period*')
        plt.figure(figsize=(5,25))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
        col3.pyplot(plt)
else: 
    st.write('Oops! Nothing to display. Atleast one cryptocurrency must be selected.')