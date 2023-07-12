from confluent_kafka import Producer
import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance')
from requirment import resource_path
from datetime import datetime,timedelta
import time
import numpy as np


topic_init = 'init_database'
topic_real_time='real_time'
dic={{'bootstrap.servers': 'localhost:9092'}}
def Serialization(DataFrame):
    return DataFrame.to_json()



def initiat_producer(configuration_server=dic):
    producer_init = Producer(configuration_server)
    producer_real_time=Producer(configuration_server)
    
    return producer_init,producer_real_time

def produce_init_data(producer_init,data,ticket):
    serliazed=Serialization(data)
    producer_init.produce(topic_init, key=ticket, value=serliazed)
    producer_init.flush()

def produce_realtime_data(producer_real_time,data,ticket):
    serliazed=Serialization(data)
    producer_real_time.produce(topic_init, key=ticket, value=serliazed)
    producer_real_time.flush()





