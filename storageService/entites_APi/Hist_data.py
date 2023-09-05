from sqlalchemy import Column,Table,Integer,String,DateTime,ForeignKey,FLOAT
from sqlalchemy.orm import relationship
import pytz
from datetime import datetime
from base import Base
import pandas as pd


class Hist_data(Base):
    __tablename__='Hist_datas'

    id=Column(Integer,primary_key=True)
    Datetime=Column(DateTime)
    open=Column(FLOAT)
    close=Column(FLOAT)
    high=Column(FLOAT)
    low=Column(FLOAT)
    volume=Column(FLOAT)
    ticket_id=Column(Integer,ForeignKey('tickets.id'))
   
    
    def __init__(self,dic,ticket_id=None,timezone=None):
        if isinstance(dic,list)==True:
            self.Datetime=dic[0]
            self.open=dic[1]
            self.close=dic[4]
            self.high=dic[2]
            self.low=dic[3]
            self.volume=dic[6]

        
        
        
        
        if isinstance(dic,type(None))==False:
            date=datetime.fromtimestamp(dic['Datetime1'],pytz.UTC)
            self.Datetime=date
            self.open=dic['Open']
            self.close=dic['Close']
            self.high=dic['High']
            self.low=dic['Low']
            self.volume=dic['Volume']
            
        else:
            print('None')
            pass     
        if ticket_id!=None:
            date=datetime.fromtimestamp(dic['Datetime1'],pytz.UTC)

            self.Datetime=date
            self.open=dic['Open']
            self.close=dic['Close']
            self.high=dic['High']
            self.low=dic['Low']
            self.volume=dic['Volume']
            self.ticket_id=ticket_id

    

        
    def get_date(self):
        return self.Datetime
    def to_list(self):
        return [self.Datetime,self.open,self.close,self.high,self.low,self.volume]    
        