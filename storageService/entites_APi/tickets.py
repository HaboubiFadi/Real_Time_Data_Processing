from sqlalchemy import Column,Table,Integer,String,DateTime
from sqlalchemy.orm import relationship
import pandas as pd
from base import Base
import pytz
from datetime import datetime

class Ticket(Base):
    __tablename__='tickets'

    id =Column(Integer,primary_key=True)
    ticket_name=Column(String)
    ticket_type=Column(String)
    time_zone=Column(String)
    last_time_updated=Column(DateTime)
    hist_data=relationship('Hist_data',uselist=True,cascade='all, delete-orphan',lazy='dynamic')
    
    def __init__(self,dic):
        self.ticket_name=dic['ticket_name']
        self.ticket_type=dic['ticket_type']
        self.time_zone=dic['time_zone']

        date=datetime.fromtimestamp(dic['last_time_updated'],pytz.UTC)


        self.last_time_updated=date


        
    def set_updated_time(self,datetime):
        self.last_update_day=datetime
    def set_Hist_data(self,Hist_data):
        self.hist_data=Hist_data
    
    def update_historical_data(self,Hist_data_items):
        if isinstance(Hist_data_items,list):
            for i in Hist_data_items:
                self.hist_data.append(i)     
        else:
            self.hist_data.append(Hist_data_items)        

    def get_dattime(self):
        return self.last_time_updated
    def set_dateyime(self,last_date):
        self.last_time_updated=last_date
    def getname(self):
        return self.ticket_name 
    def to_list(self):
        return [self.id,self.ticket_name,self.last_time_updated,self.time_zone]


 
