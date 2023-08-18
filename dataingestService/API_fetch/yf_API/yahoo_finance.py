import yfinance as yf
import os
import pandas as pd
from datetime import datetime,timedelta
path=os.getcwd()
print(path)
import sys
sys.path.append(path)
init_data=datetime(2023,8,10,8)


# fetch data from yahoo_fiance using yfinance api from a defned date
def fetch_data_per_ticket(start_date,ticket='AUDJPY=X',interval='1m'):
    data = yf.download(tickers = ticket ,  start=start_date,interval =interval)
    return data
# fetch 1 minute_data interval from defined date 
# (rq: we used a while loop because the yf_API can fetch data from more than 7day from defined date)
def fetch_init_data_per_ticket(ticket,start_date,end_date):
    data1=pd.DataFrame()
    date=start_date
    while date<end_date:
        data = yf.download(tickers = ticket , start=date,end=date+timedelta(days=7),interval ='1m')
        data1=pd.concat([data1,data],axis=0)
        date=date+timedelta(days=7)
    
    data1 = data1.reset_index(drop=False)
    data1=data1.drop_duplicates(subset=['Datetime'])


    #data = yf.download(tickers = ticket , start=data1.iloc[-1]['Datetime'],interval ='1m')
    return data1


# fetch real time date (only last minute data)
def fetch_reel_time(ticket):
    data = yf.download(tickers = ticket , start=datetime.now()-timedelta(minutes=3),interval ='1m')
    data = data.reset_index(drop=False)
    data=data.drop_duplicates(subset=['Datetime'])
    return data
