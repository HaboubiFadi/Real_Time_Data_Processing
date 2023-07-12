

import yfinance as yf
import pandas as pd


# Define the ticker symbol for the stock you want to retrieve data for
ticker = "AAPL"  # Example: Apple Inc.

# Use the `download` function to fetch historical data for the specified ticker
data = yf.download(tickers = 'JPYAUD=X' , start="2023-07-06",interval = '1m')
data1_new = data.reset_index(drop=False)
print(data1_new.iloc[1]['Datetime'])
