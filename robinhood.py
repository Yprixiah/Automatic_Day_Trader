import robin_stocks as r
import view as v
import datetime as dt

credentials = []

def login(self):
    r.login(credentials[0], credentials[1])

def set_credentials (list):
    global credentials
    credentials = list

def get_latest_stock_price(stock):
    price = r.get_latest_price(stock)
    return price