
#* IMPORTING LIBRARIES
 
import pandas as pd
import streamlit as st, yfinance as yf
import plotly.express as px, plotly.graph_objects as go
from datetime import date,datetime,timedelta

#* PAGE TITLES
st.set_page_config(
    page_title='STOCKS DASHBOARD',
    page_icon='📊',
    layout='wide')

st.title('STOCK MARKET DASHBOARD📊')
st.markdown('##')

#! VARIABLES
tickers_list = ['AAPL','GOOGL','MSFT','META','TSLA','AMZN']


#* SIDEBAR
with st.sidebar:
    st.title('HELLO THERE !👋')
    st.subheader('My Name is Abdul Hadi.')
    st.markdown('''
- Welcome to My Financial Insights Dashboard
- Explore comprehensive financial data at your fingertips.
- Analyze stock prices and make informed investment decisions.
''')
    st.markdown('---')
    st.header('SELECT THE DATE')
    start = st.date_input('Start Date',date.today()-timedelta(days=365))
    end = st.date_input('End Date',date.today())

    st.header('SELECT THE COMPANY')
    ticker = st.selectbox('Select',tickers_list)
    st.markdown('---')
    st.markdown('''
- Selecting the date filters the data between that time.
- Selecting the company filters the data of respective company.
- The KPI's tells about the filtered data and respective information.
- The Visualization tells about
    - The rate changes of filtered date and company.
    - The latest volume stocks of each company.
    - The volume changes of each company.
    - The rate changess of each company.
                ''')

#! IMPORT DATA

df = yf.download(tickers=ticker,start=start,end=end)
df.insert(0,'Date',df.index,True)
df.reset_index(drop=True,inplace=True)

dataframes = []
for ticker in tickers_list:
    dfo = yf.download(ticker, start=start , end=end)
    dfo['Company'] = ticker  
    dataframes.append(dfo)

combined_df = pd.concat(dataframes)
combined_df.insert(0,'Date',combined_df.index,True)
combined_df.reset_index(drop=True,inplace=True)

#* MAIN PAGE

#! KPI'S
latest_closing= round(df['Close'].iloc[-1],2)
shares_volume= int(df['Volume'].iloc[-1])
weekly_average= round((df['Close'].tail(5)).mean(),2)

col_1, col_2,col_3 = st.columns(3)
with col_1:
    st.subheader('LATEST CLOSE :')
    st.subheader(f'${latest_closing} USD')
with col_2:
    st.subheader('VOLUME OF STOCKS :')
    st.subheader(f'{shares_volume:,} SHARES')
with col_3:
    st.subheader('WEEKLY AVERAGE CLOSING :')
    st.subheader(f'${weekly_average} USD')

st.markdown('---')

#* VISUALIZATIONS 

col_1 , col_2 = st.columns(2)
with col_1:    
#! LINE CHART
    col = st.selectbox('SELECT THE COLUMN :',df.columns[1:])
    fig_line = px.line(df,x='Date',y=col)
    fig_line.update_traces(line=dict(color='green'))
    fig_line.update_layout(
        title='VARIATION OF RATE',width=800,height=500)
    st.plotly_chart(fig_line)
#! AREA CHART
    fig_area=px.area(combined_df,x='Date',y='Volume',facet_col='Company',facet_col_wrap=2,color='Company')
    fig_area.update_layout(
        title="VARIATION OF VOLUME STOCKS",width=800,height=600)
    st.plotly_chart(fig_area)


with col_2:
#! PIE CHART    
    latest_vol = combined_df.groupby('Company').tail(1)
    fig_pie = px.pie(latest_vol,values='Volume',names='Company',color_discrete_sequence=px.colors.qualitative.D3)
    fig_pie.update_traces(hoverinfo='label+percent',marker=dict(line=dict(color='#000000',width=2)))
    fig_pie.update_layout(
        title='LATEST SHARES OF EACH COMPANY',
        width=800,height=500)

    st.plotly_chart(fig_pie)
#! AREA CHART
    col2 = st.selectbox('SELECT THE COLUMN :',combined_df.columns[1:6])
    fig_area=px.area(combined_df,x='Date',y=col2,facet_col='Company',facet_col_wrap=2,color='Company')
    fig_area.update_layout(
        title="VARIATION OF RATES FOR ALL COMPANIES",width=800,height=600)
    st.plotly_chart(fig_area)