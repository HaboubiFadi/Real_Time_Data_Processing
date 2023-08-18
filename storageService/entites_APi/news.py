from sqlalchemy import Column,Table,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
import pandas as pd
from base import Base


class News(Base):
    __tablename__='news'

    
    id=Column(Integer,primary_key=True)
    source=Column(String)
    author=Column(String)
    title=Column(String)
    description=Column(String)
    publishedAt=Column(DateTime)
    content=Column(String)
    sentiment=Column(String)

    ticket_id=Column(Integer,ForeignKey('news_tickets.id'))
   
      


   
    def __init__(self,serie=None):
        if isinstance(serie,type(None))==False:
            self.source=serie['source']
            self.author=serie['author']
            self.title=serie['title']
            self.description=serie['description']
            self.publishedAt=serie['publishedAt']
            self.content=serie['content']
            self.sentiment=serie['sentiment']

        else:
            print('None')
            pass
        