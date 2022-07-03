import mysql.connector
import pandas as pd
import numpy as np
import time
import sys



def display_data():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT bid, ask, diff_bid, diff_ask, exchange  FROM orderbook WHERE timestamp >= DATE_SUB(NOW(),INTERVAL 15 MINUTE)")

    myresult = mycursor.fetchall()
    print (myresult)
#display_data()

def get_stats(interval):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ccxtdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT diff_bid FROM orderbook WHERE timestamp >= DATE_SUB(NOW(),INTERVAL {interval} MINUTE)")

    result = mycursor.fetchall()
    diff_bids_list = []
    for item in result:
        diff_bids_list.append(item[0])
    if not len(diff_bids_list) == 0:
        avg_diff_bid = (sum(diff_bids_list)/len(diff_bids_list))
        max_diff_bid = max(diff_bids_list, key=abs)
        print(max_diff_bid, end = "\r")
        #print(max_diff_bid, flush=True)
    else:
        avg_diff_bid, max_diff_bid = 'No entries'   

    return avg_diff_bid, max_diff_bid

while True:
    get_stats(1)
