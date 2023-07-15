import yfinance as yf

import pandas as pd
from datetime import datetime,timedelta
import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/dataingestService/API_fetch/')
from requirments import init_data

def fetch_data_per_ticket(start_date,ticket='AUDJPY=X'):
    data = yf.download(tickers = ticket ,  start=start_date,interval ='1m')
    return data

def fetch_init_data_per_ticket(ticket,start_date=init_data):
    date=init_data
    data1=pd.DataFrame()
    while date<datetime.now():
        data = yf.download(tickers = ticket , start=date,end=date+timedelta(days=7),interval ='1m')
        data1=pd.concat([data1,data],axis=0)
        date=date+timedelta(days=7)
    
    data1 = data1.reset_index(drop=False)
    data1=data1.drop_duplicates(subset=['Datetime'])


    #data = yf.download(tickers = ticket , start=data1.iloc[-1]['Datetime'],interval ='1m')
    return data1



def fetch_reel_time(ticket):
    data = yf.download(tickers = ticket , start=datetime.now()-timedelta(minutes=3),interval ='1m')
    data = data.reset_index(drop=False)
    data=data.drop_duplicates(subset=['Datetime'])
    return data
