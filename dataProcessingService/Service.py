from confluent_kafka import Consumer
import pandas as pd
from datetime import datetime,timedelta
import time
import numpy as np
import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance')
from requirment import resource_path


topic_init = 'init_database'
topic_real_time='real_time'
dic={{'bootstrap.servers': 'localhost:9092'}}
def liste_to_str(list,split=','):
    s=''
    for i in list:
        s=s+str(i)
        if list.index(i)!=len(list)-1:
            s=s+','
    return s   

def assignment_callback(consumer,topic_partitions):
    for tp in topic_partitions:
        print(tp.topic)
        print(tp.partition)
        print(tp.offset)





def Deserialization(json):
    DataFrame = pd.read_json(json, orient ='index')
    return DataFrame


def Initiat_Consumer(configuration_server=dic):
    consumer_init = Consumer(configuration_server)
    consumer_init.subscribe([topic_init],on_assign=assignment_callback)
    consumer_reel_time=Consumer(configuration_server)
    consumer_reel_time.subscribe([topic_real_time],on_assign=assignment_callback)

    
    return consumer_init,consumer_reel_time


def Simple_Moving_average(DataFrame,periode):
    DataFrame['SMA']=DataFrame['Close'].rolling(window=periode).mean()
    return DataFrame
def Exponential_Moving_Average(DataFrame,periode,alpha):
    DataFrame['EMA']=DataFrame['Close'].ewm(span=periode,alpha=alpha).mean()
    return DataFrame

def Cumulative_Moving_Average(DataFrame):
    DataFrame['CMV']=DataFrame['Close'].expanding().mean()
#Relative 
def RSI(DataFrame,periode):
    Data_copy=DataFrame.copy()
    Data_copy['diff']=Data_copy.diff()
    Data_copy['pos_diff']=np.zeros(len(Data_copy))
    Data_copy['neg_diff']=np.zeros(len(Data_copy))
    Data_copy.loc[Data_copy['diff']>0,'pos_diff']=Data_copy['diff']
    Data_copy.loc[Data_copy['diff']<0,'neg_diff']=Data_copy['diff']
    Data_copy['avg_gain']=Data_copy['pos_diff'].rolling(windows=periode).mean()
    Data_copy['avg_loss']=Data_copy['neg_diff'].rolling(windows=periode).mean()
    Data_copy['RSI']=100 - (100/(1 + (Data_copy['avg_gain']/Data_copy['avg_loss'])))
    DataFrame['RSI']=Data_copy['RSI']
    return DataFrame



def Processing_data(DataFrame):
    DataFrame=Simple_Moving_average(DataFrame)
    DataFrame=Cumulative_Moving_Average(DataFrame)
    DataFrame=RSI(DataFrame)     
    return DataFrame    

def Write_in_text(headers):
    key,value=headers
    value=Deserialization(value)
    ful_path=resource_path+str(key.decode('utf-8'))
    text_file=open(ful_path,'a')  
    """text_file.write(liste_to_str(value.columns.to_list()))
    text_file.write('\n')"""

    for i in len(value):
        line=liste_to_str(value.iloc[i].values.tolist())
        text_file.write('\n')
        text_file.write(line)
    text_file.close()







def Consume_data_Api_finance(consumer,key):
    
    while True:
        msg=consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"There might be a problem {msg.error()}")
        
        Write_in_text(msg.headers())
    


    