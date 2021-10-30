import pandas as pd
import requests


def download_latest_instruments(file_path):
    url = 'http://api.kite.trade/instruments'
    req = requests.get(url)
    url_content = req.content
    csv_file = open(file_path, 'wb')
    csv_file.write(url_content)
    csv_file.close()


def get_instruments_df(file_path):
    download_latest_instruments(file_path)
    df_master = pd.read_csv(file_path)
    return df_master


def get_token(df, exchange, symbol):
    return int(df.loc[(df['exchange'] == exchange) & (df['tradingsymbol'] == symbol)]['instrument_token'])


df_tokens = get_instruments_df('C://Users//haris//Desktop//instruments.csv')
print(get_token(df_tokens, 'NSE', 'SBIN'))
