# Data ingesting (API yf) 
# using script to initiate The Producer
from API_fetch.News_Api.new_api import initiate_data_news
from Service import initiat_producer,produce_init_data
from datetime import datetime,timedelta
import time
headers = {
    
    'sortBy':'popularity',
    'from':datetime(2023,7,1),
    "apiKey" :'83ec940dd74b4342afd20676e8efdab7',
    'q':'stocks',
    'page':1
    
}


if __name__ =='__main__':
    minutes=0
    p_init=initiat_producer()
    ticket='stocks_news'
    fetched_data_init=initiate_data_news(headers)
    print(fetched_data_init)
    print("column:",fetched_data_init.keys())
    produce_init_data(p_init,fetched_data_init,ticket)