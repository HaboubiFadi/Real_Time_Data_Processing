import pandas as pd
"""
dataframe=pd.DataFrame([[1,2,3,4,5]],columns=['a','b','c','d','s'])
print(dataframe)
cs=pd.DataFrame([[1,2,3]],columns=['a','b','c'])
k=pd.concat([cs,dataframe],axis=0)"""
dict = {'Geeks': 10,
        'for': 20,
        'geeks': 30}
serie=pd.Series(dict)
print(isinstance(serie,pd.Series))                              

print('it me mario',isinstance(pd.DataFrame(serie),pd.Series))                      
