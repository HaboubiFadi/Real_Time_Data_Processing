from  datetime import  datetime,timedelta
import os 
path=os.getcwd()
import sys
sys.path.append(os.path.join(path,'API_fetch'))
from yf_API.yahoo_finance import fetch_init_data_per_ticket
from News_Api.new_api import reduced_news
from Service import initiat_producer,Serialization


#defined variable:

start_date=datetime(2023,8,21,10)
end_date=datetime(2023,8,21,14)
headers = {
    
    'sortBy':'popularity',
    'from':datetime(2023,8,16),
    "apiKey" :'d75e635c125f41aab9362439dd3e022c',
    'q':'',
    'page':1,
    'language':'en'
    
}


def Call_API(ticket,type='price'):
    if type=='price':
        dataFrame=fetch_init_data_per_ticket(ticket,start_date,end_date)
        return dataFrame
    elif type=='news':
        print('im here')
        headers['q']=ticket
        dataFrame=reduced_news(headers)
    return dataFrame    
topic_price = 'ingest_price'
topic_news='ingest_news'
dic={'bootstrap.servers': 'broker:9092'}
ticket_list_price=['GOOG','AAPL','AMZN','AMD']
ticket_forex=['EURUSD=X','GBPUSD=X','EURJPY=X']

ticket_dic={'stock':ticket_list_price,'forex':ticket_forex}




ticket_list_new=['google','apple','gold','nasdaq','amazon','amd']
import time
types=['price','newsss']

def timezone_and_last_time_update(dataframe):
    return dataframe.iloc[-1]['Datetime'].tzinfo,dataframe.iloc[-1]['Datetime']











def produce():

    producer_price=initiat_producer(dic)
    producer_news=initiat_producer(dic)
    for type_ticket,value in ticket_dic.items():
        for i in range(len(value)):
            dataframe=Call_API(value[i],'price')
            if dataframe.shape[0]==0:
                continue
            serliazed=Serialization(dataframe)
            tz=timezone_and_last_time_update(dataframe)
            print('time zone,',tz)
            key_1=str(value[i])+','+str(tz[1])+','+str(tz[0])+','+str(type_ticket)
            print('key',key_1)
            producer_price.produce(topic_price, key=str(key_1), value=serliazed)
            print('historical price produced')
            producer_price.flush()
            time.sleep(5)                
            
            
            


                       

if __name__=='__main__':
    print('wait for servers to establish')
    time.sleep(30)
    produce()


"""
if ty=='news':
                dataframe=Call_API(ticket_list_new[i],ty)
                print(dataframe)
                if dataframe.shape[0]==0:
                    continue
                serliazed=Serialization(dataframe)
                producer_news.produce(topic_news, key=ticket_list_new[i], value=serliazed)
                print('news produced')

                producer_news.flush()
                time.sleep(60) 
    




    
"""

