from confluent_kafka import Consumer
import pandas as pd
import os
path=os.getcwd()
import sys
sys.path.append(os.path.join(path,'entites_APi'))
from news import News
from Hist_data import Hist_data
from tickets import Ticket
from datetime import datetime
from entites_APi.new_tickets import News_tickets

import sys
from base import Session


sys.path.append(os.path.join(path,'database'))
from postgres import insert_data







def get_ticket(key):
    session=Session()    
    tick=session.query(Ticket).filter(Ticket.ticket_name==key).first()
    session.close()
    return tick












topic_init = 'init-database'
topic_real_time='real-time'


def Deserialization(s):

    json_string = s.decode('utf-8')
    df = pd.read_json(json_string)
    return df


def Initiat_Consumer(configuration_server):
    consumer_init = Consumer(configuration_server)
    consumer_init.subscribe([topic_init])
    print('Consumer is successfully initiated')
    return consumer_init

def Consumer_init(configuration_server):
    consumer_init = Consumer(configuration_server)
    print('Consumer is successfully initiated')
    return consumer_init





def data_frame_to_class_objects(object,dataFrame):
    if isinstance(object,News):
        liste=[]
        print('news object')
        for i in range(len(dataFrame)):
            liste.append(News(dataFrame.iloc[i]))
        return liste
    if isinstance(object,Hist_data):
        liste=[]
        print('hist object')

        for i in range(len(dataFrame)):
            liste.append(Hist_data(dataFrame.iloc[i]))
        return liste





def Consume_data_into_database(consumer):
    

    while True:
        msg=consumer.poll(1.0)
        if msg==None:
            continue
        if msg.error():
            print(f"There might be a problem {msg.error()}")
        if msg!= None:
            print('data received succefully')
            print('msg.key()',msg.key().decode('utf-8'))    
            if 'news' in  msg.key().decode('utf-8'):
                print('data is news information')
                dataframe=Deserialization(msg.value())
                print(dataframe)

                empty_object=News(None)
                liste_news=data_frame_to_class_objects(empty_object,dataframe)
                
                
                ticket=get_ticket(msg.key().decode('utf-8'))
                
                if ticket ==None:
                    tick_info= {'ticket_name':msg.key().decode('utf-8'),'last_time_updated':datetime.now()}

                    ticket=Ticket(tick_info)
                    ticket.set_news(liste_news)
                else:

                    ticket.set_updated_time(datetime.now())
                    ticket.update_news(liste_news)

                insert_data(ticket)

topic_price_consume= 'process_price'
topic_news_consume='process_news'   


def Consume_data(dic):
    consumer=Consumer_init(dic)
    consumer.subscribe([topic_price_consume,topic_news_consume])
    while True:
        message=consumer.poll(1.0)
        if message is None:
            print('im waiting for reel time feed')
            continue
        if message.error():
            print(f"There might be a problem {message.error()}")

        else:
            print('data delivered successfully')
            topic = message.topic()
            if topic=='process_price':
                key = message.key()
                value = message.value()
                value=Deserialization(value)
                empty_object=Hist_data(None)
                liste_price=data_frame_to_class_objects(empty_object,value)
                tick_info= {'ticket_name':key.decode('utf-8'),'last_time_updated':datetime.now()}

                ticket=Ticket(tick_info)
                ticket.set_Hist_data(liste_price)
                insert_data(ticket)

            if topic=='process_news':
                key = message.key()
                value = message.value()
                value=Deserialization(value)
                empty_object=News(None)
                liste_news=data_frame_to_class_objects(empty_object,value)
                tick_info= {'ticket_name':key.decode('utf-8'),'last_time_updated':datetime.now()}

                ticket_news=News_tickets(tick_info)
                ticket_news.set_news(liste_news)
                insert_data(ticket_news)          
        







    

#cons=Initiat_Consumer()
#Consume_data_into_database(cons)