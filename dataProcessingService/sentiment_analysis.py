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
def sentiment_numtotext():
    pass

def news_sentiment_analysis(data):

    with open('model_sentiment_analysis/model.pk','rb') as f: # open ML model using pickle
        model=pickle.load(f)
    with open('model_sentiment_analysis/CounterVectorizer.pk','rb') as f: # open ML model using pickle
        CounterVectorizer=pickle.load(f)    
    # Vectorize  data using CounterVectorizer 
    data_new=pd.DataFrame(data,columns=['contenu'])
    data_new=data_new['Ner'].apply(lambda txt:NER(txt))

    # apply the vectorizer to the corpus
    X = CounterVectorizer.transform(data.Ner)

    y_pred=model.predict(X)
    return y_pred