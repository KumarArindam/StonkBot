import pandas as pd
import yfinance as yf
from datetime import datetime, time, timedelta, date
from yahoofinancials import YahooFinancials
import numpy as np

yesterday = datetime.now() - timedelta(1)
start_date = datetime.strftime(yesterday, '%Y-%m-%d')
trade_date = datetime.now().date().strftime('%Y-%m-%d')

def format_output(df):
    
    res = ""
    for index, row in df.iterrows():
        res+= "{} \tEOD Data\n".format(row['stock'])
        res+= "---Date: {}\n".format(row['date'])
        res+= "---Open: {:.2f}\n".format(np.round(row['open'], 2))
        res+= "---Close: {:.2f}\n".format(np.round(row['close'], 2))
        res+= "---Low: {:.2f}\n".format(np.round(row['low'], 2))
        res+= "---High: {:.2f}\n\n".format(np.round(row['high'], 2))
        
    return res

def get_closing_data(stock_list):
    close_data = pd.DataFrame()
    for stock in stock_list:
        print("{}  ----- {}".format(stock, trade_date))

        yahoo_financials = YahooFinancials(stock)
        data = yahoo_financials.get_historical_price_data(start_date=start_date, 
                                                          end_date= trade_date,
                                                          time_interval='daily')

        data_df = pd.DataFrame(data[stock]['prices'])
        data_df = data_df.drop('date', axis=1).set_index('formatted_date')
        data_df.reset_index(inplace=True)
        data_df = data_df.rename(columns={'formatted_date':'date'})
        data_df = data_df.drop(columns = ['adjclose', 'volume'])
        data_df['stock'] = stock
        close_data = pd.concat([close_data,data_df], axis=0)

    close_data = close_data.drop_duplicates()
    close_data.reset_index(inplace=True)
    close_data.drop('index',axis=1, inplace=True)

    res =  format_output(close_data)  
    return res