import requests
import os
import json
from datetime import datetime
import pandas as pd
'''# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
category='business'
country='us'
# Set the API endpoint URL
url = "https://newsapi.org/v2/top-headlines"

# Set the request headers
headers = {
    "category": category,
    "country": country,
    "apiKey" :'83ec940dd74b4342afd20676e8efdab7'
}

# Set the request parameters


# Send the GET request to the API
response = requests.get(url, params=headers)
data=response.json()
print(data.keys())
print(data['articles'][0])
'''

def get_topheadlines(*args):
    
    # Set the API endpoint URL  
    url = "https://newsapi.org/v2/top-headlines"
    print(args)
    params=args[0]
    response=requests.get(url,params=params)    
    result=response.json()
    return result


#print(get_topheadlines(headers))


def get_everything(*args):
    # Set the API endpoint URL  
    url = "https://newsapi.org/v2/everything"
    print(args)
    params=args[0]
    response=requests.get(url,params=params)    
    result=response.json()
    return result


def get_element_index_liste(key,liste):
    for i in liste:
        if i==key:
            return True 
    return False
#This function filter a dictionary from the unnecessary features (variables)
def get_required_features(dictionary,features_liste):
    
    new_dict={key:value for (key,value) in dictionary.items() if get_element_index_liste(key,features_liste)==True} 
    return new_dict
def filter_source(new_dict):
    new_dict['source']=new_dict['source']['name']
    return new_dict
def value_dictionnaire(dic,filter):
    liste=[]
    for i in filter:
        liste.append(dic[i])
    return liste


def clean_columns(json):
    filter=['source','author','title','description','publishedAt','content']
    articles=json['articles']
    Dataframe=pd.DataFrame(columns=filter)
    for article in articles:
        print(article)
        new_dic=get_required_features(article,filter)
        new_dic=filter_source(new_dic)
        Dataframe.loc[len(Dataframe)]=value_dictionnaire(new_dic,filter)
    
    return Dataframe


def initiate_data_news(headers):
    json=get_everything(headers)
    data_frame=clean_columns(json)

    return data_frame