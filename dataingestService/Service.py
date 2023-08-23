from confluent_kafka import Producer,Consumer
import sys
import pandas as pd
from datetime import datetime,timedelta
import time
import numpy as np


topic_init = 'init-database'
topic_real_time='real-time'
dic={'bootstrap.servers': 'broker:9092'}
def Serialization(DataFrame):
    return DataFrame.to_json()

def initiat_producer(configuration_server=dic):
    producer_init = Producer(configuration_server)
    
    return producer_init


def initiat_producers(configuration_server=dic):
    producer_init = Producer(configuration_server)
    producer_real_time=Producer(configuration_server)
    
    return producer_init,producer_real_time

def produce_init_data(producer_init,data,ticket,topic_init='init-database'):
    
    
    print('/***Producer info *******\:','/n topic_sub:',topic_init)
    print('/n data_key:',ticket)

    
    
    
    serliazed=Serialization(data)
    producer_init.produce(topic_init, key=ticket, value=serliazed)
    producer_init.flush()
    time.sleep(3)

def produce_realtime_data(producer_real_time,data,ticket,topic_real_time='real-time'):
    print('/***Producer info *******\:','/n topic_sub:',topic_init)
    print('/n data_key:',ticket)


    serliazed=Serialization(data)
    producer_real_time.produce(topic_real_time, key=ticket, value=serliazed)
    producer_real_time.flush()


def Deserialization(s):

    json_string = s.decode('utf-8')
    df = pd.read_json(json_string)
    
        
    return df


def Initiat_Consumer(configuration_server=dic):
    consumer_init = Consumer(configuration_server)

    
    return consumer_init


# decompose dataframe into smaller part to fit it into kafka producer
def baching_data(dataframe,max_req):    
    size=dataframe.memory_usage(deep=True).sum() # get dataframe size
    raw_size=int(size/dataframe.shape[0]) # get approximately of the size of each raw
    batch_size=int(max_req/raw_size)+1 # calculate how many raws fit in a batch pack 
    dataframe_liste=[]
    pack_size=size/max_req # how packs we should iterate with 
    if size>max_req:
        j=0
        for i in range(1,int(size/max_req)+2):
            if i<int(size/max_req)+1:
                data=dataframe.loc[j:(i*batch_size)-1]
                dataframe_liste.append((data,str(i)+',part'))
            else:
                data=dataframe.loc[j:]
                dataframe_liste.append((data,str(i)+',part'+',final'))
            j=i*batch_size
    return dataframe_liste