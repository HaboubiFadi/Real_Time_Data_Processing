from  datetime import  datetime,timedelta
import os 


from Service import Initiat_Consumer,Deserialization,assignment_callback,Processing_data,initiat_producer,Serialization
from sentiment_analysis import news_sentiment_analysis
# define variables
topic_price_consume= 'ingest_price'
topic_news_consume='ingest_news'
topic_price_produce= 'process_price'
topic_news_produce='process_news'
di_consume={'bootstrap.servers': 'broker:9092','group.id':'processing_consumer'}
di_producer={'bootstrap.servers': 'broker:9092'}
def Consume_data():
    consumer=Initiat_Consumer(di_consume)
    producer=initiat_producer(di_producer)
    consumer.subscribe([topic_price_consume,topic_news_consume])
    while True:
        message=consumer.poll(1.0)
        if message is None:
            print('no_data')
            continue
        if message.error():
            print(f"There might be a problem {message.error()}")

        
        else:
            print('data delivered successfully')

            topic = message.topic()
            
            if topic=='ingest_price':
                key = message.key().decode('utf-8')
                value = message.value()
                value=Deserialization(value)
                value=Processing_data(value)
                producer.produce(topic_price_produce, key=key, value=Serialization(value))
                producer.flush()
            
            print('topic:::::',topic)
            if topic==topic_news_consume:
                key = message.key().decode('utf-8')
                value = message.value()
                value=Deserialization(value)
                print('new data processed',value)

                value=news_sentiment_analysis(value)
                producer.produce(topic_news_produce, key=key, value=Serialization(value))
                producer.flush()



import time    

print('Welcome to the processing service')
time.sleep(50)
Consume_data()