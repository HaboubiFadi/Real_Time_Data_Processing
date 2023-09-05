from datetime import datetime,timedelta
import pandas as pd 
import pytz 
import yfinance as yf
def fetch_realtime_multidata(tickets,timezone):
    start_date=datetime.now()-timedelta(minutes=3)
    timezone_date = start_date.astimezone(pytz.timezone(timezone))


    data = yf.download(tickets, start=timezone_date,interval="1m")
    data = data.reset_index(drop=False)
    if len(tickets.split(' '))==1:
        data.columns=pd.MultiIndex.from_product([data.columns, [tickets]])
        

    return data


import time
import calendar
import time

current_GMT = time.gmtime()

time_stamp = calendar.timegm(current_GMT)
print("Current timestamp:", time_stamp)
fo=fetch_realtime_multidata('EURUSD=X','Europe/London')
def convert_datetime_timestamp(date):
    real_time=date.astimezone(pytz.UTC)
    return real_time.timestamp()    

#fo['Datetime']=fo['Datetime'].apply(lambda date: convert_datetime_timestamp(date))
print(len(fo.iloc[-1]))



#date=datetime.fromtimestamp(fo['Datetime'].iloc[-1],pytz.UTC)
#print(fo)