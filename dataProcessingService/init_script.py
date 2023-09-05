from  datetime import  datetime,timedelta
import os 


from Service import Initiat_Consumer,Deserialization,assignment_callback,Processing_data,initiat_producer,Serialization
from sentiment_analysis import news_sentiment_analysis
# define variables
reception_news=os.environ.get('reception_news')
emission_news=os.environ.get('emission_news')
reception_price=os.environ.get('reception_price')
emission_price=os.environ.get('emission_price')




di_consume={'bootstrap.servers': 'broker:9092','group.id':'processing_consumer','enable.auto.commit': True,
        'auto.offset.reset': 'earliest'}
di_producer={'bootstrap.servers': 'broker:9092'}
def Consume_data():
    max_time_no_data=1000
    time_no_data=0
    consumer=Initiat_Consumer(di_consume)
    producer=initiat_producer(di_producer)
    consumer.subscribe([reception_price,reception_news])
    while True:
        message=consumer.poll(1.0)
        if max_time_no_data<time_no_data:
            break

        if message is None:
            time_no_data=time_no_data+1
            continue

        if message.error():
            print(f"There might be a problem {message.error()}")

        
        else:
            time_no_data=0
            print('data delivered successfully')

            topic = message.topic()
            
            if topic==reception_price:
                # process price data for Api request 
                key = message.key().decode('utf-8')
                print('keyqsdqsdqsd',key)
                key_msg=key.split(',')
                key=key_msg[0]
                indication_choice=key_msg[1]
                if len(key_msg)>2:
                    periode=int(key_msg[2])
                else:
                    periode=14    
                value = message.value()
                value=Deserialization(value)
                value=Processing_data(value,indication_choice,periode)
                producer.produce(emission_price, key=key, value=Serialization(value))
                producer.flush()
            
            print('topic::',topic)
            if topic==reception_news :
                key = message.key().decode('utf-8')
                value = message.value()
                value=Deserialization(value)
                #print('new data processed',value)
                print('key in process',key)
                value=news_sentiment_analysis(value)
                if topic==reception_news:
                    producer.produce(emission_news, key=key, value=Serialization(value))
                    producer.flush()
                
                    


import time    

if __name__=='__main__':

    print('Welcome to the processing service')
    time.sleep(4)
    Consume_data()

