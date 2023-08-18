from sqlalchemy import Column,Table,Integer,String,DateTime,ForeignKey,FLOAT
from sqlalchemy.orm import relationship

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
   
    sma=Column(FLOAT)
    cmv=Column(FLOAT)
    rsi=Column(FLOAT)
    def __init__(self,dic):
        if isinstance(dic,list)==True:
            self.Datetime=dic[0]
            self.open=dic[1]
            self.close=dic[4]
            self.high=dic[2]
            self.low=dic[3]
            self.volume=dic[6]

        
        
        
        
        if isinstance(dic,type(None))==False:

            self.Datetime=dic['Datetime']
            self.open=dic['Open']
            self.close=dic['Close']
            self.high=dic['High']
            self.low=dic['Low']
            self.volume=dic['Volume']
            self.sma=dic['SMA']
            self.cmv=dic['CMV']
            self.rsi=dic['RSI']
        else:
            print('None')
            pass     

    

        
    def get_date(self):
        return self.Datetime
    