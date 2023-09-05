import os 
print(os.getcwd())
#sys.path.append(os.path.join(os.getcwd(),"API_fetch"))
import sys

sys.path.append('/home/haboubi/Desktop/final/dataingestService/API_fetch')
from News_Api.new_api import *

start_date=datetime(2023,8,26,12,10)
end_date=datetime(2023,8,16,14)
headers = {
    
    'sortBy':'publishedAt',
    'from':start_date,
    "apiKey" :'d75e635c125f41aab9362439dd3e022c',
    'q':'',
    'page':1,
    'language':'en'
    
}
headers['q']='Stocks'
data=reduced_news(headers)
print(data['publishedAt'])