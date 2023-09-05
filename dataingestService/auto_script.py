from  datetime import  datetime,timedelta
import os 
path=os.getcwd()
import sys
sys.path.append(os.path.join(path,'API_fetch'))
from yf_API.yahoo_finance import multi_fetch,separate_data,fetch_realtime_multidata
from Service import initiat_producer,Serialization,Deserialization,Initiat_Consumer,baching_data

import time   
di_consume={'bootstrap.servers':"broker:9092",'group.id':'dig_consume','enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}
di_producer={'bootstrap.servers': 'broker:9092'}
topic_auto='auto_ingest'     
topic_dig='diagn_price'








def cal_diagn_api(value):
    multi_data=[]
    grouped_ticket=separate_data(value,['timezone','Datetime'])# ticket are grouped by shared date (a dictionary)
    print('im the group')
    for key,value in grouped_ticket.items():
        print('im here now :',key[1],key[0])
        multi_data.append(multi_fetch(value,key[1],key[0]))
    return multi_data








def call_auto_api(value):
    multi_data=[]
    grouped_ticket=separate_data(value,'timezone')# ticket are grouped by shared date (a dictionary)
    for key,value in grouped_ticket.items():
        multi_data.append(fetch_realtime_multidata(value,key))
    return multi_data
    





def consume_diagnostic(consumer,topic_dig):
    max_no_data=100
    time_no_data=0

    while True:
        message=consumer.poll(1.0)
        if max_no_data<time_no_data:
            return []
        
        if message is None:
            time_no_data=time_no_data+1
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
  
def diagnostic_produce(value):
    max_req=100000
    producer_auto=initiat_producer(di_producer)
    
    datas=cal_diagn_api(value)
    
    for data in datas :
        print(data)
        if not data.empty:
            bached_liste=baching_data(data,max_req)
            if len(bached_liste)==0:
                    producer_auto.produce(topic_auto, key='Full', value=Serialization(data))
                    producer_auto.flush()
                    time.sleep(2)    
            else:    
                for i in bached_liste:
                    
                    producer_auto.produce(topic_auto, key=i[1], value=Serialization(i[0]))
                    producer_auto.flush()
                    time.sleep(2) 
            time.sleep(2) 
    
            
def auto_produce(value):
    max_req=100000
    producer_auto=initiat_producer(di_producer)
    datas=call_auto_api(value)
    for data in datas :
        print(data)
        if not data.empty:
            bached_liste=[]
            if len(bached_liste)==0:
                    producer_auto.produce(topic_auto, key='Full,live', value=Serialization(data))
                    producer_auto.flush()
                    time.sleep(2)    
            else:    
                for i in bached_liste:
                    
                    producer_auto.produce(topic_auto, key=i[1], value=Serialization(i[0]))
                    producer_auto.flush()
                    time.sleep(2) 


def manage_time(launch_time):
    now_sec=datetime.now().second
    if now_sec>launch_time:
        return (60+launch_time)-now_sec
    else:
        return launch_time-now_sec 

    

















if __name__=='__main__':
    launch_time=30
    print('wait for servers to establish')
    time.sleep(30)
    consumer=Initiat_Consumer(di_consume)
    consumer.subscribe([topic_dig])

    waiting_time=manage_time(launch_time)
    print('first waiting time:',waiting_time)

    time.sleep(waiting_time)

    value=consume_diagnostic(consumer,topic_dig)
    diagnostic_produce(value)
    while True:
        waiting_time=manage_time(launch_time)
        print('next waiting time:',waiting_time)
        time.sleep(waiting_time)
        auto_produce(value)



