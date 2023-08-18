from confluent_kafka import Producer
import sys

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




