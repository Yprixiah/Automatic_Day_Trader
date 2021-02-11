import robin_stocks as r
import pandas as pd
login = "pierre.a.gross@protonmail.com"
password = "#766684Radio@c"

status = {}
week_market = {}
week_market_hights = {}

def initialize ():
    r.login(login, password)
    holdings = r.build_holdings()
    for key in holdings:
        status[key] = holdings.get(key).get('price')
        week_market[key] = r.stocks.get_stock_historicals(key, interval='5minute', span='week', bounds='regular') #dict{list[dict{}]} {[{}]}
        week_market_hights[key] = {}
        for i in range(0, len(week_market.get(key))):
            week_market_hights.get(key)[i] = float(week_market.get(key)[i].get('high_price'))

def r_login():
    r.login(login, password)

def get_week_market_hights():
    df = pd.DataFrame(week_market_hights)
    return df