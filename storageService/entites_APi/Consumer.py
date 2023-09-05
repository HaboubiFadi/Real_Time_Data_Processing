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
from new_tickets import News_tickets

import sys
from base import Session

from Service import update_updatedtime_tickets
sys.path.append(os.path.join(path,'database'))
from postgres import insert_data

from sqlalchemy import and_,or_

def Serialization(DataFrame):
    return DataFrame.to_json()

def liste_hist_data_to_dataframe(liste_hist):
    columns=['Datetime','Open','Close','High','Low','Volume']
    dataframe=pd.DataFrame(columns=columns)
    for hist_data in liste_hist:
        dataframe.loc[len(dataframe)]=hist_data.to_list()

    return dataframe 






def liste_news_to_dataframe(liste_news):
    columns=['Source','Author','Title','Description','PublishedAt','Sentiment']
    dataframe=pd.DataFrame(columns=columns)
    for new in liste_news:
        dataframe.loc[len(dataframe)]=new.to_list()

    return dataframe 


def  get_news_filtred(request):
    ticket_id=get_news_ticket(request['query'],id=True)
    session=Session()


    if 'start_time' in request.keys() and 'end_time' in request.keys() :  
        news=session.query(News).filter(and_(News.ticket_id==ticket_id,News.publishedAt()>request['start_time'],News.publishedAt()>request['end_time'])).first()
        
        
        
        session.close()
        return liste_news_to_dataframe(news)
    elif 'start_time' in request.keys():
        news=session.query(News).filter(and_(News.ticket_id==ticket_id,News.publishedAt()>request['start_time']))
        session.close()
        return liste_news_to_dataframe(news)
    elif 'end_time' in request.keys() :
        news=session.query(News).filter(and_(News.ticket_id==ticket_id,News.publishedAt()>request['end_time']))
        session.close()
        return liste_news_to_dataframe(news)
    else:
        news=session.query(News).filter(News.ticket_id==ticket_id)
        session.close()
        return liste_news_to_dataframe(news)



def get_historical_filtred(request):
    ticket_id=get_ticket(request['query'],id=True)
    session=Session()


    if 'start_time' in request.keys() and 'end_time' in request.keys() :  
        hist_data_liste=session.query(Hist_data).filter(and_(Hist_data.ticket_id==ticket_id,Hist_data.Datetime>request['start_time'],Hist_data.Datetime()>request['end_time']))
        
        
        
        session.close()
        return liste_hist_data_to_dataframe(hist_data_liste)
    elif 'start_time' in request.keys():
        hist_data_liste=session.query(Hist_data).filter(and_(Hist_data.ticket_id==ticket_id,Hist_data.Datetime>request['start_time']))
        session.close()
        return liste_hist_data_to_dataframe(hist_data_liste)
    elif 'end_time' in request.keys() :
        hist_data_liste=session.query(Hist_data).filter(and_(Hist_data.ticket_id==ticket_id,Hist_data.Datetime>request['end_time']))
        session.close()
        return liste_hist_data_to_dataframe(hist_data_liste)
    else:
        hist_data_liste=session.query(Hist_data).filter(Hist_data.ticket_id==ticket_id)
        session.close()
        return liste_hist_data_to_dataframe(hist_data_liste)








def get_ticket(key,id=False):
    session=Session()    
    tick=session.query(Ticket).filter(Ticket.ticket_name==key).first()
    session.close()
    if id==False:
        return tick
    else:
        if tick!=None:
            return tick.id
        else:
            return -1
def get_news_ticket(key,id=False):
    session=Session()    
    tick=session.query(News_tickets).filter(News_tickets.ticket_name==key).first()
    session.close()
    if id==False:
        return tick
    else:
        if tick!=None:
            return tick.id
        else:
            return -1











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





def data_frame_to_class_objects(object,dataFrame,ticket_id=None):
    if isinstance(object,News):
        liste=[]
        print('news object')
        for i in range(len(dataFrame)):
            liste.append(News(dataFrame.iloc[i],ticket_id))
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
                print(value['Datetime1'])
                liste_price=data_frame_to_class_objects(empty_object,value)
                fetch_key=fetch_init_key(key.decode('utf-8'))
                print('im here ladies',key,value['Datetime'])
                tick_info= {'ticket_name':fetch_key['ticket_name'],
                            'last_time_updated':value['Datetime1'].max(),
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
                tick_info= {'ticket_name':key.decode('utf-8'),'last_time_updated':value['publishedAt'].max()}

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
    statue=False
    # get the Datetme column name in  the multiindex 
    i=0
    while (statue==False):
        if 'Datetime1' in multiindex.columns[i]:
            statue=True
            datecolum=multiindex.columns[i]
        i=i+1    
    dic['Datetime1']=multiindex[datecolum]
    return pd.DataFrame(dic),dic['Datetime1'].iloc[-1]   




def multi_data_into_object(full_data,all_tickets,live):
    print('sdqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',live)
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
        if live != 'live':
            for i in range(len(dic)):
                liste_hist.append(Hist_data(dic.iloc[i],ticket_id,timezone))
        else:
            liste_hist.append(Hist_data(dic.iloc[-1],ticket_id,timezone))
        print('hist_data lentgh fafafafaf',len(liste_hist))    
        ticket_updated.append((ticket_id,last_update,timezone))


    return liste_hist,ticket_updated











def Consume_auto_data(consumer,topic,all_tickets):
    print('im here in consumer auto data ')
    print('///////////////////////////////////////////////////////')

    consumer.subscribe(topic)
    dataframe_constraction_loop=False
    while True:
        message=consumer.poll(1.0)
        if message is None:
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
                live=key.split(',')[-1]
                liste_hist_price,ticket_info=multi_data_into_object(value,all_tickets,live=live)
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
                    live=key.split(',')[-1]
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
                        liste_hist_price,ticket_info=multi_data_into_object(full_data,all_tickets,live)
                        insert_data(liste_hist_price)
                        update_updatedtime_tickets(ticket_info)








def Consume_news_data(consumer,topic,all_tickets):
    print('im here in consumer news data ')
    print('///////////////////////////////////////////////////////')
    max_time_no_data=120
    time_no_data=0
    consumer.subscribe(topic)
    dataframe_constraction_loop=False
    while True:
        message=consumer.poll(1.0)
        if max_time_no_data<time_no_data:
            break

        if message is None:
            time_no_data=time_no_data+1
            continue
        if message.error():
            print(f"There might be a problem {message.error()}")

        
        else:
            time_no_data=0    
            print('data delivered successfully')

            topic = message.topic()
            key=message.key().decode('utf-8')
            value = message.value()
            value=Deserialization(value)
            empty_object=News(None)
            liste_news=data_frame_to_class_objects(empty_object,value,ticket_id=key)
            print('here the problem',value['publishedAt'])
            value=value.astype({'publishedAt': 'datetime64[ns, UTC]'})

            ticket_info=[key,value['publishedAt'].max()]
            print('my names is clear and im using clear for men',ticket_info)
            update_updatedtime_tickets(ticket_info,'news')           
            insert_data(liste_news) 
            consumer.commit()
            

