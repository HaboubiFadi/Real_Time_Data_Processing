from base import  Base ,engine,Session
from Hist_data import Hist_data
from tickets import Ticket
from news import News

import sys
from datetime import datetime
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance')
from requirment import resource_path
def init_database_postgres():
    print('Postgres')
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
def get_all_ticket():
    session=Session()    
    tickets=session.query(Ticket).all()
    session.close()
    return tickets





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

def update_all_in_database():
    tickets=get_all_ticket()
    for i in range(len(tickets)):
        tickets[i]=updated_object_from_txt(tickets[i])

    return tickets











if __name__=='__main__':
    init_database_postgres()

        


    



