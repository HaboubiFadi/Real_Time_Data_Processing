from confluent_kafka import Consumer
import pandas as pd
from news import News
from Hist_data import Hist_data
from tickets import Ticket
from datetime import datetime
import sys
from base import Session
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/storageService/database')
from postgres import insert_data







def get_ticket(key):
    session=Session()    
    tick=session.query(Ticket).filter(Ticket.ticket_name==key).first()
    session.close()
    return tick












topic_init = 'init-database'
topic_real_time='real-time'
dic={'bootstrap.servers': 'localhost:9092','group.id':'trial'}


def Deserialization(s):

    json_string = s.decode('utf-8')
    df = pd.read_json(json_string)
    return df


def Initiat_Consumer(configuration_server=dic):
    consumer_init = Consumer(dic)
    consumer_init.subscribe([topic_init])
    print('Consumer is successfully initiated')
    return consumer_init

def data_frame_toc_class_objects(object,dataFrame):
    if isinstance(object,News):
        liste=[]
        for i in range(len(dataFrame)):
            liste.append(News(dataFrame.iloc[i]))
        return liste
    if isinstance(object,Hist_data):
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
                liste_news=data_frame_toc_class_objects(empty_object,dataframe)
                
                
                ticket=get_ticket(msg.key().decode('utf-8'))
                
                if ticket ==None:
                    tick_info= {'ticket_name':msg.key().decode('utf-8'),'last_time_updated':datetime.now()}

                    ticket=Ticket(tick_info)
                    ticket.set_news(liste_news)
                else:

                    ticket.set_updated_time(datetime.now())
                    ticket.update_news(liste_news)

                insert_data(ticket)

        







    

#cons=Initiat_Consumer()
#Consume_data_into_database(cons)