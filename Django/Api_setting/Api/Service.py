dic={'type':['historical','news']}
from datetime import datetime,timedelta
from confluent_kafka import Producer,Consumer
import os
import json 


def initiat_producer(configuration_server=dic):
    producer_init = Producer(configuration_server)
    
    return producer_init


def Initiat_Consumer(configuration_server=dic):
    consumer_init = Consumer(configuration_server)

    
    return consumer_init


def verifier_request(request):
    type=request.GET.get('type')

    
    query_parameters = request.GET

    key_list=query_parameters.keys()
    start_time='start_time'
    end_time='end_time'
    query='query'
    if type not in dic['type']:
        return False,'subject does not exit try again'
    if query not in  key_list:
        return False,'insert a query for example stoc name such as (AMD) is obligatoire'
    

    if start_time in key_list:
        start_date= datetime.strptime(request.GET.get('start_time'), "%Y-%m-%d %H:%M:%S.%f")

        if start_date>datetime.now():
            return False,'Error in the start_time , start_time is impossible'
        if end_time in key_list:
            end_date= datetime.strptime(request.GET.get('end_time'), "%Y-%m-%d %H:%M:%S.%f")

            if end_date<start_date:
                return False,'Error in the end_time , end_time should be come after start_time'

        
    return True,'All in place chef'





import numpy as np



def Create_json(request):
     query_parameters = request.GET

     
     
     return json.dumps(query_parameters)










def produce_request(producer,request_json,emission_topic):

    request_json
    # generate a random key 
    # this key will be specifically used when the view re_send the data to the client
    key=np.random.randint(0,1000)
    print('im your random generated key',key)
    producer.produce(emission_topic,key=str(key),value=request_json)
    producer.flush()
    return key

def Consume_data(consumer,key):
    
    while True :
        msg=consumer.poll(1.0)
        if msg == None :
            print('randonas',key)
            continue
        if msg.error():
            print(f'Error kafka {msg.error()}')
        else:
            print(f'Received message succefully :')  
            key_msg=msg.key().decode('utf-8')
            print('this is the key',key)
            if str(key)==key_msg :
                consumer.close()
                return msg.value().decode('utf-8')



    