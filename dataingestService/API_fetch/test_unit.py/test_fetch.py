import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance/dataingestService/API_fetch')
from yahoo_finance import fetch_data_per_ticket,fetch_init_data_per_ticket
from datetime import datetime,timedelta
"""
now=datetime.now()-timedelta(minutes=50)
data =fetch_data_per_ticket(start_date=now)
print(data)
"""
data=fetch_init_data_per_ticket('AUDJPY=X')
print(data.columns)