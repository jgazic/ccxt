import ccxt
import mysql.connector
from datetime import datetime 
import json
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
    mycursor.execute("CREATE TABLE orderbook (exchange CHAR(20), bid DECIMAL(10,4), ask DECIMAL(10,4), timestamp DATETIME)")
#create_database()
#create_table()

# this needs to be another thread
def display_data():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT bid, exchange  FROM orderbook WHERE timestamp >= DATE_SUB(NOW(),INTERVAL 1 MINUTE)")

    myresult = mycursor.fetchall()
    print (json.dumps(str(myresult),indent=4),) 

def save_data(exchange1,bid1,ask1,exchange2,bid2,ask2):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()

    now = datetime.now()
    id = 1
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO orderbook (exchange, bid, ask, timestamp) VALUES (%s, %s, %s, %s)"
    val = [
  (exchange1, bid1, ask1, formatted_date),
  (exchange2, bid2, ask2, formatted_date),
]
    mycursor.executemany(sql, val)
    mydb.commit()
    print('saved')
    print(formatted_date)

def get_orderbook():
    while True:
        exchange1 = ccxt.binance()
        exchange2 = ccxt.kucoin()

        orderbook1 = exchange1.fetch_order_book('BTC/USDT')
        orderbook2 = exchange2.fetch_order_book('BTC/USDT')

        dict1 = orderbook1
        highest_bid1 = dict1.get('bids')[0]
        lowest_ask1 = dict1.get('asks')[0]

        dict2 = orderbook2
        highest_bid2 = dict2.get('bids')[0]
        lowest_ask2 = dict2.get('asks')[0]
        
        diff_bid = highest_bid1[0] - highest_bid2[0]
        now = datetime.now()
        
        print(f'{exchange1}\n bid:{highest_bid1[0]}\n quantity: {highest_bid1[1]}\n ask:{lowest_ask1[0]}\n quantity: {lowest_ask1[1]}\n ')
        print(f'{exchange2}\n bid:{highest_bid2[0]}\n quantity: {highest_bid2[1]}\n ask:{lowest_ask2[0]}\n quantity: {lowest_ask2[1]}\n ')
        print(diff_bid)
        print(now)

        #modify database to also store diff, this does not affect performance much

get_orderbook()


