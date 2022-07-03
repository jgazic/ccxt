import ccxt
import mysql.connector
from datetime import datetime 
import time
import pandas as pd
import numpy as np 


def create_database():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE ccxtdatabase")

def create_table():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE orderbook (exchange CHAR(20), bid FLOAT(10,4), ask FLOAT(10,4), diff_bid FLOAT(10,4), diff_ask FLOAT(10,4), timestamp DATETIME)")

def get_orderbook():
    exchange1 = ccxt.binance()
    exchange2 = ccxt.kucoin()

    orderbook1 = exchange1.fetch_order_book('BTC/USDT')
    orderbook2 = exchange2.fetch_order_book('BTC/USDT')

    dict1 = orderbook1
    highest_bid1 = dict1.get('bids')[0][0]
    lowest_ask1 = dict1.get('asks')[0][0]

    dict2 = orderbook2
    highest_bid2 = dict2.get('bids')[0][0]
    lowest_ask2 = dict2.get('asks')[0][0]
    
    diff_bid = highest_bid1 - highest_bid2
    diff_ask = lowest_ask1 - lowest_ask2
    print(diff_bid)
    save_data(f"{exchange1.id}", highest_bid1,lowest_ask1,f"{exchange2.id}",highest_bid1,lowest_ask2, diff_bid, diff_ask)

def save_data(exchange1,bid1,ask1,exchange2,bid2,ask2, diff_bid, diff_ask):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO orderbook (exchange, bid, ask, diff_bid, diff_ask, timestamp) VALUES (%s, %s, %s, %s,%s,%s)"
    val = [
  (exchange1, bid1, ask1, diff_bid, diff_ask, formatted_date),
  (exchange2, bid2, ask2, diff_bid, diff_ask, formatted_date),
]
    mycursor.executemany(sql, val)
    mydb.commit()
    print('saved')
    print(formatted_date)
    time.sleep(5)
#create_database()
#create_table()
while True:
    get_orderbook()


