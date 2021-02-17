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
    v.Window.clear_graphs(self)

    for t in range(1, int(parameters.get('Trading rounds'))):
        time.sleep(int(parameters.get('Refresh rate (s)')))
        live_data = m.live_simulate(t, stock)
        v.Window.plot(self, live_data, self.ratesGraph, graph_type=2, title='Rates', x_label='Round', y_label='AU')
        v.Window.plot(self, live_data, self.strategyGraph, graph_type=3, title='Strategy', x_label='Round', y_label='AU')
        v.Window.plot(self, live_data, self.marketGraph, graph_type=4, title='CP', x_label='Round', y_label='Price')
        App.processEvents()

        if b == 0 and m.get_a() == 1:
            SP = live_data['CP'].iloc[-1]
            v.Window.log(self, 'Sold for: ' + str(SP) + ', at round: ' + str(t))
            App.processEvents()
            b = 1
        else:
            continue

    v.Window.log(self, 'Sold for: ' + str(SP) + ', Return: ' + str(round(SP - parameters.get('Entry Price (EP)'), 3)) + ', highest was: ' + str(live_data['CP'].max()))
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

