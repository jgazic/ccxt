import ccxt
import mysql.connector

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
    mycursor.execute("CREATE TABLE orderbook (exchange CHAR(20), bid DECIMAL(10,4), ask DECIMAL(10,4), timestamp TIMESTAMP)")
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
    mycursor.execute("SELECT * FROM orderbook")

    myresult = mycursor.fetchall()
    print(myresult)

def save_data(exchange1,bid1,ask1,timestamp1,exchange2,bid2,ask2,timestamp2):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO orderbooks (exchange, bid, ask, timestamp) VALUES (%s, %s, %s, %s)"
    val = [
  (f'{exchange1}', f'{bid1}', f'{ask1}', f'{timestamp1}'),
  (f'{exchange2}', f'{bid2}', f'{ask2}', f'{timestamp2}'),
]


def get_orderbook():
    exchange1 = ccxt.binance()
    exchange2 = ccxt.kucoin()
    while True:

        orderbook1 = exchange1.fetch_order_book('BTC/USDT')
        orderbook2 = exchange2.fetch_order_book('BTC/USDT')
        
        timestamp = exchange1.iso8601(exchange1.milliseconds())
        
        print(orderbook1['asks'][0], orderbook1['bids'][0])
        print(f"Kucoin {orderbook2['asks'][0], orderbook2['bids'][0]}")


get_orderbook()

