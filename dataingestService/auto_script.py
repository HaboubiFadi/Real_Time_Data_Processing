from  datetime import  datetime,timedelta
import os 
path=os.getcwd()
import sys
sys.path.append(os.path.join(path,'API_fetch'))
from yf_API.yahoo_finance import multi_fetch,separate_data
from Service import initiat_producer,Serialization,Deserialization,Initiat_Consumer,baching_data

import time   
di_consume={'bootstrap.servers':"broker:9092",'group.id':'dig_consume','enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}
di_producer={'bootstrap.servers': 'broker:9092'}
topic_auto='auto_ingest'     
topic_dig='diagn_price'








def cal_diagn_api(value):
    multi_data=[]
    grouped_ticket=separate_data(value)# ticket are grouped by shared date (a dictionary)
    print('im here you mother fucker:',grouped_ticket)
    for key,value in grouped_ticket.items():
        multi_data.append(multi_fetch(value,key))
    return multi_data






    
    





def consume_diagnostic():
    consumer=Initiat_Consumer(di_consume)
    consumer.subscribe([topic_dig])

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
            
            if topic==topic_dig:
                key = message.key().decode('utf-8')
                value = message.value()
                value=Deserialization(value)
                return value     
  
def auto_produce(value):
    max_req=7500
    producer_auto=initiat_producer(di_producer)
    
    datas=cal_diagn_api(value)

    for data in datas[1:] :
        print(data)
        bached_liste=baching_data(data,max_req)
        if len(bached_liste)==0:
                producer_auto.produce(topic_auto, key='Full', value=Serialization(data))
                producer_auto.flush()
                time.sleep(2)    
        else:    
            for i in bached_liste:
                
                producer_auto.produce(topic_auto, key=i[1], value=Serialization(i[0]))
                producer_auto.flush()
                time.sleep(5) 
        time.sleep(5) 

            

if __name__=='__main__':
    print('wait for servers to establish')
    time.sleep(30)
    value=consume_diagnostic()
    auto_produce(value)



