from entites_APi.Consumer import Consume_news_data,Consumer_init

from database.postgres import insert_data,initiate_database_yf
from datetime import datetime
from entites_APi.Service import get_all_ticket_list,initiat_producer,Serialization

from entites_APi.Api_Service import consume_request
import os
import time

reception_storage_from_api=os.environ.get('reception_storage_from_api')
emission_storage_from_api=os.environ.get('emission_storage_to_api')
emission_storage_from_process=os.environ.get('emission_storage_to_process')



kafka_server_confi={'bootstrap.servers':"broker:9092",'group.id':'storage_consumer_api','enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}

if __name__=='__main__':
    time.sleep(15)
    topic=[reception_storage_from_api,emission_storage_from_api,emission_storage_from_process]
    #producer=initiat_producer(dic_reel)
    consume=Consumer_init(kafka_server_confi)
    produce=initiat_producer(kafka_server_confi)
    print('Api_Storage_Service_initiated')
    consume_request(consume,produce,topic)
    