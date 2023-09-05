import yfinance as yf
from datetime import datetime
start_date=datetime(2023,8,23,18,19)
end_date=datetime(2023,8,17,1)

string='EURUSD=X GBPUSD=X'
data = yf.download(string,start=start_date,interval="1m")
string='SPY'
print(data)
data=data.reset_index(drop=False)
data=data.swaplevel(0,1,axis="columns")
'''
print(data1['AAPL']['Open'])
print('/////////////////////////////////////')
print(data['Open']['AAPL'])
'''
print(data.iloc[-1]['EURUSD=X']['Close'])

