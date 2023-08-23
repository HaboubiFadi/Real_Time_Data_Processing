from entites_APi.Consumer import Consume_data

from database.postgres import insert_data,initiate_database_yf
from datetime import datetime
# define variables
dic={'bootstrap.servers': 'broker:9092','group.id':'storage_consumer'}

topic_price_consume= 'ingest_price'
topic_news_consume='process_news'
import time
topic=[topic_price_consume,topic_news_consume]                  
if __name__=='__main__':
    initiate_database_yf()
    time.sleep(30)
    Consume_data(dic,topic)