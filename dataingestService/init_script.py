from  datetime import  datetime,timedelta
import os 
path=os.getcwd()
import sys
sys.path.append(os.path.join(path,'API_fetch'))
from yf_API.yahoo_finance import fetch_init_data_per_ticket
from News_Api.new_api import reduced_news
from Service import initiat_producer,Serialization


#defined variable:

start_date=datetime(2023,8,24,10)
end_date=datetime(2023,8,21,14)



def Call_API(ticket,type='price',timezone='America/New_York',headers={}):
    if type=='price':
        dataFrame=fetch_init_data_per_ticket(ticket,start_date,timezone)
        return dataFrame
    elif type=='news':
        headers['q']=ticket
        dataFrame=reduced_news(headers)
    return dataFrame    

topic_price = 'ingest_price'
dic={'bootstrap.servers': 'broker:9092'}
ticket_list_price=['GOOG','AAPL','AMZN','AMD']
ticket_forex=['EURUSD=X','GBPUSD=X','EURJPY=X']

ticket_dic={'stock,America/New_York':ticket_list_price,'forex,Europe/London':ticket_forex}




import time

def timezone_and_last_time_update(dataframe):
    return dataframe.iloc[-1]['Datetime'],dataframe['Datetime'].max()











def produce():

    producer_price=initiat_producer(dic)
    for type_ticket,value in ticket_dic.items():
        typee,timezone=type_ticket.split(',')
        for i in range(len(value)):
            dataframe=Call_API(value[i],'price',timezone)
            if dataframe.shape[0]==0:
                continue
            serliazed=Serialization(dataframe)
            tz=timezone_and_last_time_update(dataframe)
            print('time zone,',dataframe['Datetime1'])
            key_1=str(value[i])+','+str(tz[1])+','+str(timezone)+','+str(typee)
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

