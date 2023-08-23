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

from Service import update_updatedtime_tickets
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

def fetch_init_key(key): # fetch the key consumed from the init ingestservice   
    fetch_key=key.split(',')
    print(fetch_key)
    return {'ticket_name':fetch_key[0],'last_updated':fetch_key[1],
            'timezone':fetch_key[2],'type':fetch_key[3]}


def Consume_data(dic,topic):
    consumer=Consumer_init(dic)
    consumer.subscribe(topic)
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
            if topic=='ingest_price':
                key = message.key()
                value = message.value()
                value=Deserialization(value)
                empty_object=Hist_data(None)
                print('my name is key and i use clear for men ',key)
                liste_price=data_frame_to_class_objects(empty_object,value)
                fetch_key=fetch_init_key(key.decode('utf-8'))
                tick_info= {'ticket_name':fetch_key['ticket_name'],
                            'last_time_updated':fetch_key['last_updated'],
                            'time_zone':fetch_key['timezone'],
                            'ticket_type':fetch_key['type']
                            }

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
        

# function that concat Dataframe parts 
# function used in iteration loop
# return expected_part to be concated, return statue of the concatenation
# key is the message key that tell information about the part
def concat_part(full_data,part_data,expected_part,key):
    part_number=int(key.split(',')[0])
    if part_number==expected_part:
        full_data=pd.concat([full_data,part_data],axis=0)
        return True,full_data,expected_part+1

    else:
        return False,full_data,expected_part


def fetch_column_name(dataframe):
    liste=[]
    for name in dataframe.columns:
        if name[1]!='':
            ticket_name=str((name).split(',')[0].replace('(',''))
            if ticket_name!="'Datetime'":
                liste.append(ticket_name)


    return set(liste)



def extract_data_from_multiindex(multiindex,name):
    dic={}
    statues=['Close','High','Volume','Low','Open']

    for statue in statues:
        req=f"({name}, '{statue}')"

        dic[statue]= multiindex[req]
    dic['Datetime']=multiindex["('', 'Datetime')"]
    return pd.DataFrame(dic),dic['Datetime'].iloc[-1]   




def multi_data_into_object(full_data,all_tickets):
    columns=list(fetch_column_name(full_data))
    ticket_updated=[]
    print('list of ticket_name',columns)
    liste_hist=[]
    for name in columns:
        if name!="''" :
            na=name.replace("'",'')
            print('my name is :',na)
            ticket_serie=all_tickets[all_tickets['name']==str(na)]
            print('im here:',ticket_serie)
            if len(ticket_serie)>0:
                ticket_id=ticket_serie['id'].iloc[0]
                timezone=ticket_serie['timezone'].iloc[0]
                print('my names is ticket name',ticket_id)
            else:
                continue    
        else:
            continue
        print('im here')    
        dic,last_update=extract_data_from_multiindex(full_data,name) 
        print('put data into a dataframe to create a hist_obj object ')
        for i in range(len(dic)):
            liste_hist.append(Hist_data(dic.iloc[i],ticket_id,timezone))
        ticket_updated.append((ticket_id,last_update,timezone))


    return liste_hist,ticket_updated











def Consume_diag_data(consumer,topic,all_tickets):
    print('im here in consumer auto data ')
    print('///////////////////////////////////////////////////////')

    consumer.subscribe(topic)
    dataframe_constraction_loop=False
    while True:
        message=consumer.poll(1.0)
        if message is None:
            print('no_data')
            continue
        if message.error():
            print(f"There might be a problem {message.error()}")

        
        else:

            print('data delivered successfully')

            topic = message.topic()
            key=message.key().decode('utf-8')
            
            if 'Full' in key:
                value = message.value()
                value=Deserialization(value)
                # database_update 
                liste_hist_price,ticket_info=multi_data_into_object(full_data,all_tickets)
                insert_data(liste_hist_price)
                update_updatedtime_tickets(ticket_info)      
            
            elif 'part' in key:
                print('we are at the construction part ')
                if dataframe_constraction_loop==False:# initiate variable to accept divided dataframe
                    dataframe_constraction_loop=True
                    full_data=pd.DataFrame()
                    expected_part=1
                if dataframe_constraction_loop==True:
                    value = message.value()
                    value=Deserialization(value)
                    # concat_functions :
                    statue=concat_part(full_data,value,expected_part,key)
                    full_data=statue[1]
                    expected_part=statue[2]
                    print('this the the full data after the shape',full_data.shape[0])
                    print('key===',key)
                    if 'final' in key:
                        print(full_data)
                        dataframe_constraction_loop=False
                        # database_update
                        print('im at the database section')
                        liste_hist_price,ticket_info=multi_data_into_object(full_data,all_tickets)
                        insert_data(liste_hist_price)
                        update_updatedtime_tickets(ticket_info)



                        



                        
                  
    
