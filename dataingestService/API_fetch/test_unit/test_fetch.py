import sys
import os 
path=os.getcwd()
last_stalsh=path[-1::-1].index('/')
precedent_folder=path[:-1*last_stalsh]  # get the precedent directory
sys.path.append(precedent_folder)
from yahoo_finance import fetch_data_per_ticket,fetch_init_data_per_ticket
from datetime import datetime,timedelta
"""
now=datetime.now()-timedelta(minutes=50)
data =fetch_data_per_ticket(start_date=now)
print(data)
"""
data=fetch_init_data_per_ticket('AUDJPY=X')
print(data.columns)