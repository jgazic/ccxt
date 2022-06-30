import ccxt
import pandas as pd
from pprint import pprint

exchange = ccxt.binance()
orderbook = exchange.fetch_order_book('BTC/USDT')

bids = [bid[0]for bid in orderbook['bids']]
average = sum(bids)/len(bids)
print(average) 


