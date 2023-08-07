from confluent_kafka import Consumer
import pandas as pd
from datetime import datetime,timedelta
import time
import numpy as np
import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance')
from requirment import resource_path
import json


topic_init = 'init-database'
topic_real_time='real-time'
dic={'bootstrap.servers': 'localhost:9092','group.id':'EUR/USD_init'}
dic_reel={'bootstrap.servers': 'localhost:9092','group.id':'EUR/USD_reel'}

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




import json
def Deserialization(s):

    json_string = s.decode('utf-8')
    print(json_string)
    df = pd.read_json(json_string)
    
        
    return df


def Initiat_Consumer(configuration_server=dic):
    consumer_init = Consumer(dic)
    consumer_init.subscribe([topic_init],on_assign=assignment_callback)
    consumer_reel_time=Consumer(dic_reel)
    consumer_reel_time.subscribe([topic_real_time],on_assign=assignment_callback)

    
    return consumer_init,consumer_reel_time


def Simple_Moving_average(DataFrame,periode=14):
    DataFrame['SMA']=DataFrame['Close'].rolling(window=periode).mean()
    return DataFrame
def Exponential_Moving_Average(DataFrame,periode=14,alpha=0.7):
    DataFrame['EMA']=DataFrame['Close'].ewm(span=periode,alpha=alpha).mean()
    return DataFrame

def Cumulative_Moving_Average(DataFrame):
    DataFrame['CMV']=DataFrame['Close'].expanding().mean()
    return DataFrame
#Relative 
def RSI(DataFrame,periode=14):
    Data_copy=DataFrame.copy()
    Data_copy['diff']=Data_copy['Close'].diff()
    Data_copy['pos_diff']=np.zeros(len(Data_copy))
    Data_copy['neg_diff']=np.zeros(len(Data_copy))
    Data_copy.loc[Data_copy['diff']>0,'pos_diff']=Data_copy['diff']
    Data_copy.loc[Data_copy['diff']<0,'neg_diff']=Data_copy['diff']
    Data_copy['avg_gain']=Data_copy['pos_diff'].rolling(window=periode).mean()
    Data_copy['avg_loss']=Data_copy['neg_diff'].rolling(window=periode).mean()
    Data_copy['RSI']=100 - (100/(1 + (Data_copy['avg_gain']/(-1)*Data_copy['avg_loss'])))
    DataFrame['RSI']=Data_copy['RSI']
    return DataFrame



def Processing_data(DataFrame):

    DataFrame=Simple_Moving_average(DataFrame)
    DataFrame=Cumulative_Moving_Average(DataFrame)
    DataFrame=RSI(DataFrame)     
    return DataFrame


def processing_reel_time_data(DataFrame,real_time):
    DataFrame=pd.concat([DataFrame,real_time],axis=0)
    DataFrame = DataFrame.reset_index(drop=True)

    return DataFrame







def Write_in_text(key,value):
    print(key)
    value=Deserialization(value)
    value=Processing_data(value)
    ful_path=resource_path+str(key.decode('utf-8'))+'.txt'
    text_file=open(ful_path,'a')  
    """text_file.write(liste_to_str(value.columns.to_list()))
    text_file.write('\n')"""

    for i in range(len(value)):
        line=liste_to_str(value.iloc[i].values.tolist())
        text_file.write('\n')
        text_file.write(line)
    text_file.close()
    return value

def Write_reel_data_text(key,value,DataFrame):

    print(key)
    
    reel_value=Deserialization(value)
    DataFrame=processing_reel_time_data(DataFrame,reel_value)
    DataFrame=Processing_data(DataFrame)
    ful_path=resource_path+str(key.decode('utf-8'))+'.txt'
    text_file=open(ful_path,'a')  
    """text_file.write(liste_to_str(value.columns.to_list()))
    text_file.write('\n')"""

    print(DataFrame.iloc[-1])
    line=liste_to_str(DataFrame.iloc[-1].values.tolist())
    text_file.write('\n')
    text_file.write(line)
    text_file.close()
    return DataFrame






def Consume_data_Api_finance(consumer,key):
    
    while True:
        msg=consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"There might be a problem {msg.error()}")
        

        print(msg.value())
        DataFrame=Write_in_text(msg.key(),msg.value())
        print(DataFrame)
        break
    return DataFrame   

def Consume_reel_data_Api_finance(consumer,key,DataFrame):
    
    while True:
        msg=consumer.poll(1.0)

        if msg is None:
            print('im waiting for reel time feed')
            continue
        if msg.error():
            print(f"There might be a problem {msg.error()}")
        

        print(DataFrame)
        DataFrame=Write_reel_data_text(msg.key(),msg.value(),DataFrame)
    