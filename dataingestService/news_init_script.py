from  datetime import  datetime,timedelta

from init_script import Call_API
from Service import initiat_producer,Serialization
import time
start_date=datetime(2023,8,21,10)
end_date=datetime(2023,8,21,14)
key='d75e635c125f41aab9362439dd3e022c'
headers = {
    
    'sortBy':'publishedAt',
    'from':start_date,
    "apiKey" :key,
    'q':'',
    'page':1,
    'language':'en'
    
}


topic_news='ingest_news'
dic={'bootstrap.servers': 'broker:9092'}
ticket_list_new=['google','apple','gold','nasdaq','amazon','amd','forex','Stocks']

def produce():
    producer_news=initiat_producer(dic)
    for new_request in ticket_list_new:
        dataframe=Call_API(new_request,type='news',headers=headers)
        if dataframe.shape[0]==0:
            continue
        serliazed=Serialization(dataframe)
        producer_news.produce(topic_news, key=new_request, value=serliazed)
        print('news produced successfully')

        producer_news.flush()
        time.sleep(5) 


if __name__=='__main__':
    print('wait for servers to establish')
    time.sleep(30)
    produce()




