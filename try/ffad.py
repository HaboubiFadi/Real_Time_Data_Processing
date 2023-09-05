from datetime import datetime ,timedelta
import pytz
import yfinance as yf
date=datetime.now()
ddd= datetime(2023,8,24,15,59)+timedelta(minutes=1)
#ddd=ddd.astimezone(pytz.timezone('America/New_York'))
date=date.astimezone(pytz.timezone('America/New_York'))
data = yf.download('AMD AAPL', start=ddd,interval="1m")
print(data)