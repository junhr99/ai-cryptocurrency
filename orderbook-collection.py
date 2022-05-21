import requests
import time
import pandas as pd
import datetime
import os

while(1):

    book = {}

    try:
        response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
        book = response.json()
    except:
        book=None

    if book is None or not book :
        continue

    data = book['data']
    
    timestamp=datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    req_time = req_timestamp.split(' ')[0] #파일이름명에 쓰일 내용
    #print(req_timestamp)
    #print(req_time)
    
    #print (data)
    
    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0 

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    df = bids.append(asks)
    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    #print (df)

    filename="%s-%s-%s-orderbook.csv"%(req_time, "bithumb", "btc")     
    should_write_header = os.path.exists(filename)
    if should_write_header == False:
        df.to_csv(filename, index=False, header=True, mode = 'a')
    else:
        df.to_csv(filename, index=False, header=False, mode = 'a')
    #df.to_csv("2022-05-11-bithumb-BTC-orderbook.csv")
    
    time.sleep(1)
