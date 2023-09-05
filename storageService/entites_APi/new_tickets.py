from sqlalchemy import Column,Table,Integer,String,DateTime
from sqlalchemy.orm import relationship
import pandas as pd
from base import Base


class News_tickets(Base):
    __tablename__='news_tickets'

    id =Column(Integer,primary_key=True)
    ticket_name=Column(String)

    last_time_updated=Column(DateTime)
    news=relationship('News',uselist=True,cascade='all, delete-orphan',lazy='dynamic')

    def __init__(self,dic):
        self.ticket_name=dic['ticket_name']
        self.last_time_updated=dic['last_time_updated']

    def __init__(self,dic):
        self.ticket_name=dic['ticket_name']
        self.last_time_updated=dic['last_time_updated']


        
    def set_updated_time(self,datetime):
        self.last_update_day=datetime
    
  
    def get_dattime(self):
        return self.last_time_updated
    def set_dateyime(self,last_date):
        self.last_time_updated=last_date
    def getname(self):
        return self.ticket_name 


    def set_news(self,news_items):
        self.news=news_items
    
    def update_news(self,news_items):
        if isinstance(news_items,list):
            for i in news_items:
                self.news.append(i)     
        else:
            self.hist_data.append(news_items)  
    def to_list(self):
        return [self.id,self.ticket_name,self.last_time_updated]