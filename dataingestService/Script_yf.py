# Data ingesting (API yf) 
# using script to initiate The Producer
from API_fetch.yahoo_finance import fetch_init_data_per_ticket,fetch_reel_time
from Service import initiat_producer,produce_init_data,produce_realtime_data
from datetime import datetime,timedelta
import time
# 0) initiat_producers
# 1)fetch init data and produce it to the topic
# 2)wait 1 minute
# 3) start producing real time data





if __name__ =='__main__':
    minutes=0
    p_init,p_reel=initiat_producer()
    ticket='EURUSD=X'
    fetched_data_init=fetch_init_data_per_ticket(ticket)
    last_datetime=fetched_data_init.iloc[-1]['Datetime']
    #print("column:",fetched_data_init.columns())
    produce_init_data(p_init,fetched_data_init,ticket)
    
    print('flag0')
    second=datetime.now().second
    print(second)
    time.sleep(63-second)
    while True:
        data_reel=fetch_reel_time(ticket)
        print(data_reel)
        if (last_datetime==data_reel.iloc[-1]['Datetime']):
            print('flag1')
            time.sleep(5)
            continue
        
        else:
            last_datetime=data_reel.iloc[-1]['Datetime']

            data_reel=data_reel.drop([*range(len(data_reel)-1)],axis=0)
            data_reel=data_reel.reset_index(drop=True)
            print(data_reel)
            produce_realtime_data(p_reel,data_reel,ticket)
            print('flag2')

            second=datetime.now().second
            time.sleep(60-second)
        minutes=minutes+1

