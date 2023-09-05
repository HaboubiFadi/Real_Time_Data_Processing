import requests
from datetime import datetime,timedelta
import pytz
import pandas as pd
params={'type':'historical','query':'AMD','indications':'sma cma rsi','periode':5}

address='http://localhost:8000/request'
result=requests.get(address,params)
df = pd.read_json(result.json()['value'])
print(df)
