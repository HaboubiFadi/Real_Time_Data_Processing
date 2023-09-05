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
# (rq: we used a while loop because the yf_API can't fetch data from more than 7day from defined date)



'''def fetch_init_data_per_ticket(ticket,start_date,end_date):
    data1=pd.DataFrame()
    date=start_date
    while date<end_date:
        data = yf.download(tickers = ticket , start=date,end=date+timedelta(days=7),interval ='1m')
        data1=pd.concat([data1,data],axis=0)
        date=date+timedelta(days=7)
    
    data1 = data1.reset_index(drop=False)
    data1=data1.drop_duplicates(subset=['Datetime'])


    #data = yf.download(tickers = ticket , start=data1.iloc[-1]['Datetime'],interval ='1m')
    return data1'''



# fetch 1 minute_data interval from defined date 
# (rq: we used a while loop because the yf_API can't fetch data from more than 7day from defined date)
import pytz
def fetch_init_data_per_ticket(ticket,start_date,timezone):
    data1=pd.DataFrame()
    date=start_date.astimezone(pytz.timezone(timezone))
    
    
    now_utc = datetime.now(pytz.UTC)
    timezone_date = now_utc.astimezone(pytz.timezone(timezone))
    final_end=timezone_date
    end_data=date
    while end_data<final_end:
        if end_data+timedelta(days=7)<final_end:
            end_data=date+timedelta(days=7)
        else :
            end_data=final_end

        
        
        
        
        data = yf.download(tickers = ticket , start=date,end=end_data,interval ='1m')
        data1=pd.concat([data1,data],axis=0)
        date=date+timedelta(days=7)
    data1 = data1.reset_index(drop=False)
    data1=data1.drop_duplicates(subset=['Datetime'])
    data1['Datetime1']=data1['Datetime'].apply(lambda date: convert_datetime_timestamp(date))


    #data = yf.download(tickers = ticket , start=data1.iloc[-1]['Datetime'],interval ='1m')
    return data1









# fetch real time date (only last minute data)
def fetch_reel_time(ticket):
    data = yf.download(tickers = ticket , start=datetime.now()-timedelta(minutes=3),interval ='1m')
    data = data.reset_index(drop=False)
    data=data.drop_duplicates(subset=['Datetime'])
    return data



#data['Datetime']=data['Datetime'].apply(lambda date:fix_date(date))



# function return sec to 0 in datetime
def fix_date(date) :
    date=datetime(date.year,date.month,date.day,date.hour,date.minute,0)
    return date

# group data by date
def separate_data(data,groups='Datetime'): # create a dictionnary that combine key (date) with (ticket_names)
    
    data['Datetime']=data['Datetime'].apply(lambda date:fix_date(date))
    dic=data.groupby(groups).groups
    
    
    string=''
    dictionnaire={}
    for key,value in dic.items():
        string=''
        print(key)
        for v in value:
            string =string+' '+str(data['name'].iloc[v])
        dictionnaire[key]=string[1:]
    return dictionnaire


def convert_datetime_timestamp(date):

    real_time=date.astimezone(pytz.UTC)
    return int(real_time.timestamp())






def multi_fetch(tickets,start_date,timezone):
    #date=start_date.astimezone(pytz.timezone(timezone))


    start_date=pytz.UTC.localize(start_date)




    start_date=start_date.to_pydatetime()+timedelta(minutes=1)
    
    
    start_date=start_date.astimezone(pytz.timezone(timezone))

    print('this is the time zone your looking for',start_date.tzinfo)
    #timezone_date = now_utc.astimezone(pytz.timezone(timezone))
    data = yf.download(tickets, start=start_date,interval="1m")
    data = data.reset_index(drop=False)
    if len(tickets.split(' '))==1 and data.empty==False:
        data.columns=pd.MultiIndex.from_product([data.columns, [tickets]])
        data['Datetime1']=data['Datetime'][tickets].apply(lambda date: convert_datetime_timestamp(date))
        data=data.swaplevel(0,1,axis="columns")

        return data
    if not data.empty:
        data['Datetime1']=data['Datetime'].apply(lambda date: convert_datetime_timestamp(date))

        data=data.swaplevel(0,1,axis="columns")
    return data



def fetch_realtime_multidata(tickets,timezone):
    start_date=datetime.now()-timedelta(minutes=3)
    timezone_date = start_date.astimezone(pytz.timezone(timezone))


    data = yf.download(tickets, start=timezone_date,interval="1m")
    data = data.reset_index(drop=False)
    if len(tickets.split(' '))==1 and data.empty==False:
        data.columns=pd.MultiIndex.from_product([data.columns, [tickets]])
        data['Datetime1']=data['Datetime'][tickets].apply(lambda date: convert_datetime_timestamp(date))
        data=data.swaplevel(0,1,axis="columns")

        return data
    if not data.empty:
        print(data.columns)
        data['Datetime1']=data['Datetime'].apply(lambda date: convert_datetime_timestamp(date))

        data=data.swaplevel(0,1,axis="columns")

    return data