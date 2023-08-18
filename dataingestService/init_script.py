from  datetime import  datetime,timedelta
import os 
path=os.getcwd()
import sys
sys.path.append(os.path.join(path,'API_fetch'))
from yf_API.yahoo_finance import fetch_init_data_per_ticket
from News_Api.new_api import reduced_news
from Service import initiat_producer,Serialization


#defined variable:

start_date=datetime(2023,8,16,10)
end_date=datetime(2023,8,16,14)
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
ticket_list_price=['GOOG','AAPL','GC=F','NQ=F','AMZN','AMD']
ticket_list_new=['google','apple','gold','nasdaq','amazon','amd']
import time
types=['price','news']
def produce():

    producer_price=initiat_producer(dic)
    producer_news=initiat_producer(dic)
    
    for i in range(len(ticket_list_price)):
        for ty in types:
            
            if ty=='price':
                dataframe=Call_API(ticket_list_price[i],ty)
                print(dataframe)
                if dataframe.shape[0]==0:
                    continue
                serliazed=Serialization(dataframe)
                
                producer_price.produce(topic_price, key=ticket_list_price[i], value=serliazed)
                print('historical price produced')
                producer_price.flush()
                time.sleep(60)            


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

if __name__=='__main__':
    print('wait for servers to establish')
    time.sleep(30)
    produce()




    




    


