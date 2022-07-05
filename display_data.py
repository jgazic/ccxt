import mysql.connector
import pandas as pd
import os
import time
import credentials

username = credentials.username
password = credentials.password
clear = lambda: os.system('clear')

def read_prices(interval):
    mydb = mysql.connector.connect(
    host="localhost",
    user=f"{username}",
    password=f"{password}",
    database="ccxtdatabase"
    )
    mycursor = mydb.cursor()
    #Exchange1

    mycursor.execute(f"SELECT bid,ask FROM orderbook WHERE exchange = 'binance'")
    values = mycursor.fetchall()
    bids1 = []
    asks1 = []
    for value in values:
        
        bids1.append(value[0])
        asks1.append(value[1])

    try:
        avg_bid1 = (sum(bids1)/len(bids1))
        avg_ask1 = (sum(asks1)/len(asks1))
    except:
        avg_bid1, avg_ask1 = 'No entries  ', 'No entries  '  

   #Exchange2
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT bid,ask FROM orderbook WHERE exchange = 'kucoin' AND timestamp >= DATE_SUB(NOW(),INTERVAL {interval} MINUTE)")
    values = mycursor.fetchall()
    bids2 = []
    asks2 = []
    for value in values:
        bids2.append(value[0])
        asks2.append(value[1])

    try:
        avg_bid2 = (sum(bids2)/len(bids2))
        avg_ask2 = (sum(asks2)/len(asks2))
    except:
        avg_bid2, avg_ask2 = 'No entries  ', 'No entries  '
    return avg_bid1, avg_ask1, avg_bid2, avg_ask2

def read_diffs(interval):
    mydb = mysql.connector.connect(
    host="localhost",
    user=f"{username}",
    password=f"{password}",
    database="ccxtdatabase"
    )
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT diff_bid, diff_ask FROM orderbook WHERE timestamp >= DATE_SUB(NOW(),INTERVAL {interval} MINUTE)")
    values = mycursor.fetchall()
    
    diff_bids = []
    diff_asks = []
    for value in values:
        diff_bids.append(value[0])
        diff_asks.append(value[1])
    if len(diff_bids) and len(diff_asks) != 0:
        avg_diff_bid = (sum(diff_bids)/len(diff_bids))
        max_diff_bid = max(diff_bids, key=abs)
        avg_diff_ask = (sum(diff_asks)/len(diff_asks))
        max_diff_ask = max(diff_asks, key=abs)        

    else:
        avg_diff_bid, max_diff_bid, avg_diff_ask, max_diff_ask = 'No entries  ', 'No entries  ', 'No entries  ', 'No entries  '

    return avg_diff_bid, max_diff_bid, avg_diff_ask, max_diff_ask

def calculate_percentages(interval):
    avg_bid1, avg_ask1, avg_bid2, avg_ask2 = read_prices(interval)
    avg_diff_bid, max_diff_bid, avg_diff_ask, max_diff_ask = read_diffs(interval)
    try:
        avg_diff_bid_percentage = (avg_diff_bid/avg_bid1)*100
        max_diff_bid_percentage = (max_diff_bid/avg_bid1)*100
        avg_diff_ask_percentage = (avg_diff_ask/avg_ask1)*100
        max_diff_ask_percentage = (max_diff_ask/avg_ask1)*100
    except:
        avg_diff_bid_percentage, max_diff_bid_percentage, avg_diff_ask_percentage, max_diff_ask_percentage = 'No entries  ', 'No entries  ', 'No entries  ', 'No entries  '
    return avg_diff_bid_percentage, max_diff_bid_percentage, avg_diff_ask_percentage, max_diff_ask_percentage

def display_data(interval):
    avg_bid1, avg_ask1, avg_bid2, avg_ask2 = read_prices(interval)
    avg_diff_bid, max_diff_bid, avg_diff_ask, max_diff_ask = read_diffs(interval)
    avg_diff_bid_percentage, max_diff_bid_percentage, avg_diff_ask_percentage, max_diff_ask_percentage = calculate_percentages(interval)
    df = pd.DataFrame({
    'Binance Average': [avg_bid1, avg_ask1],
    'Kucoin Average': [avg_bid2, avg_ask2],
    'Average Diff [$]': [avg_diff_bid, avg_diff_ask],
    'Average Diff [%]': [avg_diff_bid_percentage, avg_diff_ask_percentage],
    'Max Diff [$]': [max_diff_bid, max_diff_ask],
    'Max Diff [%]': [max_diff_bid_percentage, max_diff_ask_percentage]

    },
    index=['Bids', 'Asks'])

    df.columns=["Binance Average","Kucoin Average","Average Diff [$]", "Average Diff [%]", "Max Diff [$]", "Max Diff [%]"]
    return df    
UP = "\x1B[3A"

while True:
    df1=display_data(1)
    df2=display_data(15)
    df3=display_data(60)
    df4=display_data(3600)
    clear()
    print(f'Last Minute \n{df1}\n\nLast 15 Minutes \n{df2}\n\nLast Hour \n{df3}\n\nLast Day \n{df4} ')
    time.sleep(5)