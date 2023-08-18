# Data processing (API yf) 
# using script to initiate The Consumers

from Service import Consume_data_Api_finance,Consume_reel_data_Api_finance,Initiat_Consumer
from datetime import datetime,timedelta
import time
# 0) Consumers
# 1)Consume initiate Data
# 2)wait 1 minute
# 3) Consume real time data





if __name__ =='__main__':
    c_init,c_reel=Initiat_Consumer()
    ticket='EURUSD=X'
    
    DataFrame=Consume_data_Api_finance(c_init,ticket)
    Consume_reel_data_Api_finance(c_reel,ticket,DataFrame)
   






