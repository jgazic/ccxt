import ccxt
import mysql.connector
from datetime import datetime 
import time
import credentials

username = credentials.username
password = credentials.password

def create_database():
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user=f"{username}",
        password=f"{password}",
        )

        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE ccxtdatabase")
    except:
        return False

def create_table():
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user=f"{username}",
        password=f"{password}",
        database="ccxtdatabase"
        )

        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE orderbook (exchange CHAR(20), bid FLOAT(10,4), ask FLOAT(10,4), diff_bid FLOAT(10,4), diff_ask FLOAT(10,4), timestamp DATETIME)")
    except:
        return False

def get_orderbook():
    myexchanges = ['binance', 'kucoin']

    exchange1 = eval("ccxt." + myexchanges[0] + "()")
    exchange2 = eval("ccxt." + myexchanges[1] + "()")
    orderbook1 = exchange1.fetch_order_book('BTC/USDT')
    orderbook2 = exchange2.fetch_order_book('BTC/USDT')

    highest_bid1 = orderbook1.get('bids')[0][0]
    lowest_ask1 = orderbook1.get('asks')[0][0]

    highest_bid2 = orderbook2.get('bids')[0][0]
    lowest_ask2 = orderbook2.get('asks')[0][0]
    
    diff_bid = highest_bid1 - highest_bid2
    diff_ask = lowest_ask1 - lowest_ask2
    
    save_data(f"{exchange1.id}", highest_bid1,lowest_ask1,f"{exchange2.id}",highest_bid2,lowest_ask2, diff_bid, diff_ask)
    #print(f'Binance Bid: {highest_bid1}\n Binance Ask:{lowest_ask1}\n Kucoin Bid:{highest_bid2}\n Kucoin Ask: {lowest_ask2}')

def save_data(exchange1,bid1,ask1,exchange2,bid2,ask2, diff_bid, diff_ask):
    mydb = mysql.connector.connect(
    host="localhost",
    user=f"{username}",
    password=f"{password}",
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

create_database()
create_table()

while True:
    get_orderbook()


