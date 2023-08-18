import os 
print(os.getcwd())
import sys
sys.path.append(os.path.join(os.getcwd(),"API_fetch"))
sys.path.append('/home/haboubi/Desktop/try_container/dataingestService/API_fetch')

from News_Api.new_api import *

start_date=datetime(2023,8,10)
end_date=datetime(2023,8,16,14)
headers = {
    
    'sortBy':'popularity',
    'from':start_date,
    "apiKey" :'d75e635c125f41aab9362439dd3e022c',
    'q':'',
    'page':1,
    'language':'en'
    
}
headers['q']='amd'
data=reduced_news(headers)
print(data['description'])