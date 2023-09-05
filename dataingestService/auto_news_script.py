from  datetime import  datetime,timedelta
import os 
path=os.getcwd()
import sys
import time
from Service import initiat_producer,Serialization,Deserialization,Initiat_Consumer,baching_data
from auto_script import consume_diagnostic
from init_script import Call_API
di_consume={'bootstrap.servers':"broker:9092",'group.id':'dig_consume_news','enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}
di_producer={'bootstrap.servers': 'broker:9092'}
topic_ingest_news='auto_ingest_news'     
topic_dig='diagn_news'
key='83ec940dd74b4342afd20676e8efdab7'
headers = {
    
    'sortBy':'publishedAt',
    'from':'',
    "apiKey" :key,
    'q':'',
    'page':1,
    'language':'en'
    
}




def produce(value,di_producer):
    producer_news=initiat_producer(di_producer)

    for i in range(len(value)):
        headers['from']=value.iloc[i]['Datetime']+timedelta(minutes=1)
        dataframe=Call_API(value.iloc[i]['name'],type='news',headers=headers)
        if dataframe.shape[0]==0:
            print('no new data')
            continue
        serliazed=Serialization(dataframe)
        key=str(value.iloc[i]['id'])
        print('id my id id:',key)

        producer_news.produce(topic_ingest_news, key=key, value=serliazed)
        print('news produced successfully')
        producer_news.flush()
        time.sleep(5) 






if __name__=='__main__':
    print('wait for servers to establish')
    time.sleep(40)

    consumer=Initiat_Consumer(di_consume)
    consumer.subscribe([topic_dig])

    print('first waiting time:')


    value=consume_diagnostic(consumer,topic_dig)
    print(value)
    produce(value,di_producer)
    