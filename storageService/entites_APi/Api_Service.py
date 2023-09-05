
from Consumer import  get_news_filtred,get_historical_filtred,Serialization
import json

def consume_request(consumer,producer,topic):
    consumer.subscribe([topic[0]])
    print('the topics are :',topic)
    while True :
        msg=consumer.poll(1.0)
        if msg == None :
            print('no data')
            continue
        if msg.error():
            print(f'Error kafka {msg.error()}')
        else:
            print(f'Received message succefully :')  
            key_msg=msg.key().decode('utf-8')
            value=msg.value().decode('utf-8')
            print('here are the request key',key_msg)
            value = json.loads(value)

            if value['type']=='news':
                news=get_news_filtred(value)
                producer.produce(topic[1],key=key_msg,value=Serialization(news))
            elif value['type']=='historical':
                hist_data=get_historical_filtred(value)
                if 'indications' not in value.keys():
                    producer.produce(topic[1],key=key_msg,value=Serialization(hist_data))
                    producer.flush()
                else:
                    # we will concat generated_key and the indications(str)and produce it to the processing service 
                    if 'periode' not in value.keys():
                        key_total=key_msg+','+str(value['indications'])
                    else:
                        key_total=key_msg+','+str(value['indications'])+','+str(value['periode'])

                    producer.produce(topic[2],key=key_total,value=Serialization(hist_data))
                    producer.flush()





        




