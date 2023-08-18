from sentiment_analysis import news_sentiment_analysis


if __name__ =='__main__':
    pridct=['Sales hit record high last quarter','Operating profit fell to 10 EUR   from 20 EUR   in 2007   including vessel sales gain of EUR 12 3 mn ','sales decrease last quarter','i went to the shop','more efficient in workplace','Congratulations! you have won  Walmart gift card','profit rise from 100 to 2000']
    print(news_sentiment_analysis(pridct))