import pickle
import spacy 
import pandas as pd
nlp=spacy.load('en_core_web_sm')
def lemmatize(text):
    doc=nlp(text)   
    tokens=[token.lemma_ for token in doc if not (token.is_stop or token.is_punct or len(token.lemma_)<=2)]

    return ' '.join(tokens)
def POS(text):
    doc=nlp(text)   
    pos=[token.pos_ for token in doc if not (token.is_stop or len(token.lemma_)<=2)]

    return ' '.join(pos)
def NER(text):
    doc=nlp(text)   

    tokens=[token.lemma_ for token in doc if not (token.is_stop )]

    ner=[]
    for i in tokens:
        j=False
        for ent in doc.ents:
            if i in ent.text:
                ner.append(ent.label_)
                j=True

        if j==False:
            ner.append(i)
    return ' '.join(ner)

def sentiment_numtotext(predicition):
    dic={0:'neutral',1:'positive',2:'negative'}
    return dic[predicition]
import re 


# and remove all the html tags

def Clean_text_from_html(text):
    text = re.sub("<[^>]*>",' ', str(text))
    return text







def news_sentiment_analysis(data_new):

    with open('model_sentiment_analysis/model.pk','rb') as f: # open ML model using pickle
        model=pickle.load(f)
    with open('model_sentiment_analysis/CounterVectorizer.pk','rb') as f: # open ML model using pickle
        CounterVectorizer=pickle.load(f)    
    
    
    #clean description from html tags 
    data_new['description']=data_new['description'].apply(lambda txt:Clean_text_from_html(txt))

    
    # Vectorize  data using CounterVectorizer 
    data_new['Ner']=data_new['description'].apply(lambda txt:NER(txt))
    
    # apply the vectorizer to the corpus
    X = CounterVectorizer.transform(data_new.Ner)

    y_pred=model.predict(X)
    data_new['sentiment']=y_pred
    data_new['sentiment']=data_new['sentiment'].apply(lambda txt:sentiment_numtotext(txt))
    return data_new