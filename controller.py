import datetime as dt
import sys
from PyQt5.QtWidgets import *
import model as m
import time
import view as v
import robinhood as rh

App = QApplication(sys.argv)

def run(self):
    global App
    b = 0
    SP = 0
    stock = 'TSLA'
    v.Window.log(self, str(dt.datetime.now().hour) + ":" + \
                    str(dt.datetime.now().minute) + ":" + \
                    str(dt.datetime.now().second) + \
                    ": Trading start")

    parameters = v.Window.get_parameters(self)
    m.set_parameters(parameters)

    if v.Window.get_trading_type(self) == 'fs':
        v.Window.log(self, str(dt.datetime.now().hour) + ":" + \
                     str(dt.datetime.now().minute) + ":" + \
                     str(dt.datetime.now().second) + \
                     ": Full Simulator")

    elif v.Window.get_trading_type(self) == 'rs':
        m.set_f(stock)
        v.Window.log(self, str(dt.datetime.now().hour) + ":" + \
                     str(dt.datetime.now().minute) + ":" + \
                     str(dt.datetime.now().second) + \
                     ": Simulating " + str(round(m.get_f(), 3)) + " of " + stock)

    elif v.Window.get_trading_type(self) == 'rh':
        m.set_f(stock)
        v.Window.log(self, str(dt.datetime.now().hour) + ":" + \
                     str(dt.datetime.now().minute) + ":" + \
                     str(dt.datetime.now().second) + \
                     ": Live trading " + str(round(m.get_f(), 3)) + " of " + stock)

    v.Window.clear_graphs(self)

    for t in range(1, int(parameters.get('Trading rounds'))):
        time.sleep(int(parameters.get('Refresh rate (s)')))
        live_data = m.live_simulate(t, stock)
        v.Window.plot(self, live_data, self.marketGraph, graph_type=1, title=stock, x_label='Round', y_label='Market price ($)')
        v.Window.plot(self, live_data, self.ratesGraph, graph_type=2, title='Rates', x_label='Round', y_label='rate')
        v.Window.plot(self, live_data, self.strategyGraph, graph_type=3, title='Strategy', x_label='Round', y_label='')
        v.Window.plot(self, live_data, self.valueGraph, graph_type=4, title='VP', x_label='Round', y_label='Value ($)')
        App.processEvents()

        if b == 0 and m.get_a() == 1:
            SP = live_data['VP'].iloc[-1]
            v.Window.log(self, 'Sold for: ' + str(SP) + ', at round: ' + str(t))
            App.processEvents()
            b = 1
        else:
            continue

    v.Window.log(self, 'Sold for: ' + str(SP) + ', Return: ' + str(round(SP - parameters.get('Entry Price (EP)'), 3)) + ', highest was: ' + str(live_data['VP'].max()))
    v.Window.log(self, str(dt.datetime.now().hour) + ":" + \
                    str(dt.datetime.now().minute) + ":" + \
                    str(dt.datetime.now().second) + \
                    ": Trading done")

def stop(self):
    sys.exit()

def prompt_login(self):
    self.login_window = v.login_window()

def rh_login (self):
    rh.set_credentials(v.Window.get_credentials(self))
    rh.login(self)
    # v.Window.log(str(dt.datetime.now().hour) + ":" + \
    #                   str(dt.datetime.now().minute) + ":" + \
    #                   str(dt.datetime.now().second) + \
    #                   ": Logged into Robinhood!")
    m.set_trading_type(v.Window.get_trading_type(self))


if __name__ == '__main__':
    window = v.Window()
    sys.exit(App.exec())

