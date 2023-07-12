from confluent_kafka import Producer
from datetime import datetime,timedelta
import time
import numpy as np
topic_init = 'init_database'
topic_real_time='real_time'
dic={{'bootstrap.servers': 'localhost:9092'}}
def Serialization():
    pass



def initiat_producer(configuration_server=dic):
    producer_init = Producer(configuration_server)
    producer_real_time=Producer(configuration_server)
    
    return producer_init,producer_real_time

def produce_fetch_to_database(producer_init,data,ticket):
    serliazed=Serialization(data)
    producer_init.produce(topic_init, key=ticket, value=serliazed)
    producer_init.flush()

def produce_fetch_realtime_data(producer_real_time,data,ticket):
    serliazed=Serialization(data)
    producer_real_time.produce(topic_init, key=ticket, value=serliazed)
    producer_real_time.flush()





