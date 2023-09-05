from base import  Base ,engine,Session
from Hist_data import Hist_data
from tickets import Ticket
from new_tickets import News_tickets
from news import News
from confluent_kafka import Producer
import pandas as pd
import os
from datetime import datetime
import pytz
resource_path=os.path.join(os.getcwd(),'resources')


def init_database_postgres():
    print(Base)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


    
def insert_txt_into_object(key):
    resource_text=resource_path+str(key)+'.txt'
    data=open(resource_text,'r').read()
    lines=data.split('\n')
    liste=[]
    for line in lines:
        tab =line.split(',')
        hist_data=Hist_data(tab)

        liste.append(hist_data)
    last_date=liste[-1].get_date()
    print('last_time_updated:',last_date)    

    ticket=Ticket({'ticket_name':key,'last_time_updated':last_date})   
    ticket.set_Hist_data(liste)
    print('last_updated',ticket.get_dattime())
    return ticket
def get_ticket(key):
    session=Session()    
    tick=session.query(Ticket).filter(Ticket.ticket_name==key).first()
    session.close()
    return tick
def get_all_ticket_list(type='price'):
    session=Session() 
    if type=='price':
        tickets=session.query(Ticket).all()
        session.close()
        dataframe=pd.DataFrame([],columns=['id','name','Datetime','timezone'])
        for ticket in tickets:
            dataframe.loc[len(dataframe)]=ticket.to_list()
        return dataframe  
    elif type=='news':
        tickets=session.query(News_tickets).all()
        session.close()
        dataframe=pd.DataFrame([],columns=['id','name','Datetime'])
        for ticket in tickets:
            dataframe.loc[len(dataframe)]=ticket.to_list()
        return dataframe  


def Serialization(DataFrame):
    return DataFrame.to_json()

def initiat_producer(configuration_server):
    producer_init = Producer(configuration_server)
    
    return producer_init  







# read txt and dump it in the database
def updated_object_from_txt(ticket):
    key=ticket.getname()
    updated_time=ticket.get_dattime()
    
    resource_text=resource_path+str(key)+'.txt'
    data=open(resource_text,'r').read()
    lines=data.split('\n')
    liste=[]
    for line in lines:
        tab =line.split(',')
        datetime_object = datetime.strptime(tab[0], "%Y-%m-%d %H:%M:%S")

        if datetime_object>updated_time:
            tab =line.split(',')
            hist_data=Hist_data(tab)

            liste.append(hist_data)
    print(liste)
    if len(liste)>0:     
        last_date=liste[-1].get_date()
        print('last_time_updated:',last_date)   
        ticket.update_historical_data(liste)
        print('last_updated',ticket.get_dattime())
        ticket.set_dateyime(last_date)
        return ticket
    return ticket
# update tickets table using liste of (id,timeupdate)

def update_updatedtime_tickets(liste_info,type='price'):
    session=Session()
    if type=='price':
        for info in liste_info:
            ticket=session.query(Ticket).filter_by(id=info[0]).first()
            print('ticket.info')
            print(ticket.getname(),ticket.ticket_type)
            date=datetime.fromtimestamp(info[1],pytz.UTC)
            

            ticket.last_time_updated=date
        session.commit()
    elif type=='news':
        print('fadfadoud:',liste_info)
        ticket_news=session.query(News_tickets).filter_by(id=liste_info[0]).first()
        print('update news_tickets:ticket_news.getname()')
        ticket_news.last_time_updated=liste_info[1]
        session.commit()




    session.close()















if __name__=='__main__':
    init_database_postgres()

        


    



