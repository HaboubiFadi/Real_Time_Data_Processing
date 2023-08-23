from entites_APi.Service import get_all_ticket,initiat_producer,Serialization
dic_reel={'bootstrap.servers': 'broker:9092'}
dig_topic='dig_hist'
def diagnostic_script():
    produce=initiat_producer(dic_reel)
    all_ticket=get_all_ticket() 
    print(all_ticket)
    key='dig'
    produce.Produce(dig_topic,key=key,value=Serialization(all_ticket))
    produce.flush()


