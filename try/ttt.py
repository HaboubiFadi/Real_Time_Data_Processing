import yfinance as yf
from datetime import datetime,timedelta
# importing timezone from pytz module
from pytz import timezone
import pytz
import pandas as pd
start_date=datetime.now()-timedelta(hours=5)
now_asia = start_date.astimezone(timezone('Europe/London'))

end_date=datetime(2023,8,17,1)
name="EURUSD=X"
data = yf.download("EURUSD=X", start=now_asia,interval="1m")
data=data.reset_index(drop=False)
data.columns=pd.MultiIndex.from_product([data.columns, [name]])
data=data.swaplevel(0,1,axis=1)
print(data[name])
""""data=data.swaplevel(0,1,axis="columns")

string='SPY'
memory_usage=data.memory_usage(deep=True).sum()
print(data)
def baching_data(dataframe,max_req):    
    dataframe=dataframe.reset_index(drop=False)
    size=dataframe.memory_usage(deep=True).sum() # get dataframe size
    raw_size=int(size/dataframe.shape[0]) # get approximately of the size of each raw
    batch_size=int(max_req/raw_size)+1 # calculate how many raws feat in a batch pack 
    dataframe_liste=[]
    pack_size=size/max_req # how packs we should iterate with 
    print(int(pack_size) ,'this is the pack')
    if size>max_req:
        j=0
        for i in range(1,int(size/max_req)+2):
            if i<int(size/max_req)+1:
                data=dataframe.loc[j:(i*batch_size)-1]
                dataframe_liste.append((data,str(i)+',part'))
            else:
                data=dataframe.loc[j:]
                dataframe_liste.append((data,str(i)+',part,final'))
            j=i*batch_size
    return dataframe_liste


datalite=baching_data(data,3000)

s=0
for i in datalite:
    s=s+i[0].shape[0]
print('longeur',s)    
import pandas as pd
a=pd.concat([pd.DataFrame(),datalite[0][0],datalite[1][0]],axis=0)
print(a)

def Serialization(DataFrame):
    return DataFrame.to_json()
def Deserialization(s):

    #json_string = s.decode('utf-8')
    df = pd.read_json(s)
    
        
    return df
import json

ser_1=Serialization(datalite[0][0])
ser_2=Serialization(datalite[1][0])
des_1=Deserialization(ser_1)
des_2=Deserialization(ser_2)

a=pd.concat([pd.DataFrame(),des_1,des_2],axis=0)
print(a.columns)
liste=[]

for name in a.columns:
    if name[1]!='':
        ticket_name=str((name).split(',')[0].replace('(',''))
        if ticket_name!="'Datetime'":
            liste.append(ticket_name)

string=list(set(liste))    
print('my name is string',string)

dic={}
statues=['Close','High','Volume','Low','Open']

#req=f"('{string}', '{statue}')"
for statue in statues:
    req=f"({string[0]}, '{statue}')"

    dic[statue]= a[req]
req=f"('Datetime', '')"
dic['Datetime']= a[req]

dataframe=pd.DataFrame(dic)
print(dataframe,'imqsdqsd')
i=0
statue=False
while (statue==False):
    if 'Datetime' in a.columns[i]:
        statue=True
        print('im in the loop,',a.columns[i])
        datecolum=a.columns[i]
    i=i+1
print('datatime:',datecolum)








# importing datetime
from datetime import datetime

# importing timezone from pytz module
from pytz import timezone
import pytz
now_utc = datetime.now(pytz.UTC)
print('now time:',now_utc)
# Format the above DateTime using the strftime()

# Converting to Asia/Kolkata time zone
now_asia = now_utc.astimezone(timezone('Europe/London'))
print("SDQSQQSD",now_asia)
"""