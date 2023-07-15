import pandas as pd

dataframe=pd.DataFrame([[1,2,3,4,5]],columns=['a','b','c','d','s'])
print(dataframe)
cs=pd.DataFrame([[1,2,3]],columns=['a','b','c'])
k=pd.concat([cs,dataframe],axis=0)
print(k)