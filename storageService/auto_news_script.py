from entites_APi.Consumer import Consume_news_data,Consumer_init

from database.postgres import insert_data,initiate_database_yf
from datetime import datetime
from entites_APi.Service import get_all_ticket_list,initiat_producer,Serialization

import time   
cong={'bootstrap.servers': 'broker:9092'}
topic_dig='diagn_news'

topic_process_news='auto_process_news'     


            

di_consume={'bootstrap.servers': 'broker:9092','group.id':'ingest_consumer_news','enable.auto.commit': True
        }
di_producer={'bootstrap.servers': 'broker:9092'}
dic_reel={'bootstrap.servers': 'broker:9092'}
def produce_database_diagnostic(produce,topic):
    all_ticket=get_all_ticket_list(type='news')
    print(all_ticket)
    key='dig'
    produce.produce(topic_dig,key=key,value=Serialization(all_ticket))
    produce.flush()
    return all_ticket




if __name__=='__main__':
    time.sleep(26)
    producer=initiat_producer(dic_reel)
    consume=Consumer_init(di_consume)
    get_tickets_news=produce_database_diagnostic(producer,topic_dig)
    print(get_tickets_news)
    time.sleep(10)
    print('im here now after initiate p/c and waitin for data')
    Consume_news_data(consume,[topic_process_news],get_tickets_news)
                  