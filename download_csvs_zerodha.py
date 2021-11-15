import pandas as pd
import requests
from datetime import datetime
import os
from pathlib import Path


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


def download_csvs(token_df, user_id, auth_token, interval, from_date, to_date, file_path):

    cur_time = datetime.now()
    for i in range(0, len(token_df)):
        token = token_df.loc[i]['instrument_token']
        result_df = get_index_zerodha(user_id, auth_token, token, interval, from_date, to_date)
        file_path2 = "{}/{}".format(file_path, cur_time.strftime('%Y_%m_%d_%H_%M_%S'))
        Path(file_path2).mkdir(parents=True, exist_ok=True)
        if not result_df.empty:
            result_df.to_csv("{}/{}.csv".format(file_path2, str(token_df.loc[i]['tradingsymbol'])))


def get_index_zerodha(user_id, auth_token, script_token, interval, from_date, to_date):
    try:
        print(float(script_token))
        script_token = str(int(script_token))
        headers = {'Authorization': auth_token}
        url = f"https://kite.zerodha.com/oms/instruments/historical/{script_token}/{interval}" \
              f"?user_id={user_id}&oi=1&from={from_date}&to={to_date}"
        response = requests.get(url, headers=headers)
        df_response = pd.DataFrame(response.json()['data']['candles'])
        df_candle = df_response.rename(
            columns={0: "Datetime", 1: "Open", 2: "High", 3: "Low", 4: "Close", 5: "Volume", 6: "OpenInterest"}
        )
        df_candle['Datetime'] = pd.to_datetime(df_candle['Datetime'])
        df_candle['Datetime'] = df_candle['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return df_candle
    except Exception as e:
        print("exception for {} .. moving On".format(script_token))
        return pd.DataFrame()


df_tokens = get_instruments_df('C://Users//haris//Desktop//instruments.csv')
# print(get_token(df_tokens, 'NSE', 'SBIN'))
from_date = '2021-11-11'
to_date = '2021-11-11'
file_path = "C:/Users/haris/Desktop/csvs"
params = {"token_df": df_tokens,
          "user_id": "GWZ469",
          "auth_token": 'enctoken kvex9cMhcwz4FtxCMOu2Qf5KwX7fQ67CM2pVvHK6ukSSAW0mBWdKEiIsE9iF3RYlq2XAMXR6oWEy4zy5ABFOpEk2SxA7QJtjLAL1HZBWmjXIFaqV08M4zw==',
          "interval": 'day',
          "from_date": from_date,
          "to_date": to_date,
          "file_path": file_path
          }
download_csvs(**params)
