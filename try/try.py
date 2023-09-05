import yfinance as yf
from datetime import datetime
start_date=datetime(2023,8,15,1)
end_date=datetime(2023,8,17,1)

"""
data = yf.download("GOOG AAPL AMZN AMD", start=start_date,end=end_date,interval="1m")
string='SPY'
print(data['Close'])
memory_usage=data.memory_usage(deep=True).sum()
print(memory_usage)
print(data.shape[0])

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


datalite=baching_data(data,8000)
print(datalite)

s=0
for i in datalite:
    s=s+i[0].shape[0]
print('longeur',s)    
data = data.reset_index(drop=False)
print(data['Close']['AAPL'])
"""
import pandas as pd
df=pd.DataFrame([[datetime(2023,12,15,1,1,1),'goog','1','france'],[datetime(2023,12,15,1,2,1),'amd','2','tunisia'],[datetime(2023,12,15,1,1,1),"apple",'3','france']],columns=['date','name','ticket_id','timezone'],)     
print(df)



date=datetime(2023,12,15,1,1,1)
def fix_date(date) :# function return sec to 0 in datetime
    date=datetime(date.year,date.month,date.day,date.hour,date.minute,0)
    return date

df['date']=df['date'].apply(lambda date:fix_date(date))
df_group=df.groupby('date')



a=df.groupby(['timezone','date']).groups
# group data by date

print(a)




def separate_data(data): # create a dictionnary that combine key (date) with (ticket_names)
    dic=data.groupby(['timezone','date']).groups
    string=''
    dictionnaire={}
    for key,value in dic.items():
        string=''
        print(key)
        for v in value:
            string =string+' '+str(data['name'].iloc[v])
        dictionnaire[key]=string[1:]
    return dictionnaire

a=separate_data(df)
print(a)
'''name='apple'
print(df[df['name']==name]['ticket_id'].iloc[0])'''
string='amd'
a=string.split(" ")
print(a)

'''
import pandas as pd
data1=pd.DataFrame()
for i in datalite:
    data1=pd.concat([data1,i[0]],axis=0)
print(data1['Datetime'])
'''