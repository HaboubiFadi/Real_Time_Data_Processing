from entites_APi.Consumer import Consume_auto_data,Consumer_init

from database.postgres import insert_data,initiate_database_yf
from datetime import datetime
from entites_APi.Service import get_all_ticket_list,initiat_producer,Serialization

import time   
cong={'bootstrap.servers': 'broker:9092'}
topic_dig='diagn_price'

topic_auto='auto_ingest'     


            

di_consume={'bootstrap.servers': 'broker:9092','group.id':'ingest_consumer','enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}
di_producer={'bootstrap.servers': 'broker:9092'}
dic_reel={'bootstrap.servers': 'broker:9092'}
def diagnostic_script(produce):
    all_ticket=get_all_ticket_list()
    print(all_ticket)
    key='dig'
    produce.produce(topic_dig,key=key,value=Serialization(all_ticket))
    produce.flush()
    return all_ticket



topic_auto='auto_ingest'     

if __name__=='__main__':
    time.sleep(26)
    producer=initiat_producer(dic_reel)
    consume=Consumer_init(di_consume)
    get_tickets=diagnostic_script(producer)
    print(get_tickets)
    time.sleep(10)
    print('im here now after initiate p/c and waitin for data')
    Consume_diag_data(consume,[topic_auto],get_tickets)
                  