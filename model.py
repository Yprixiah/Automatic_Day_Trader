import random
import pandas as pd
import robin_stocks as r
import robinhood as rh

EP = 0
MP = 0
f = 1
VP = EP * f

low_var = 0
up_var = 0
a = 0

c_start = 0
c_finish = 0
agg = 'cst' # cst or var
mod = 'quad' # lin or quad

t_max = 0

data = pd.DataFrame(columns=['MP', 'VP', 'VP_avg', 'r', 'dr_dt', 'i_s', 'h', 'T', 'c', 'r_a', 'r_u', 'r_l'])
data.append({'MP' : MP,
             'VP': VP,
             'VP_avg': VP,
             'r': VP / EP,
             'dr_dt': 0,
             'i_s': VP / (EP * c_start),
             'h': VP / (EP * c_start),
             'T': 0,
             'c': c_start,
             'r_a': VP / EP,
             'r_u': VP / EP,
             'r_l': VP / EP, }, ignore_index=True)

r_buffer = [VP / EP]
VP_buffer = [VP]
buff_size = 12

trading_type = 'fs'

def buffer_adjust (r, VP):
    global r_buffer, VP_buffer

    r_buffer.append(round(r, 3))
    VP_buffer.append(VP)

    if len(r_buffer) > buff_size:
        r_buffer.pop(0)

    if len(VP_buffer) > buff_size:
        VP_buffer.pop(0)

def set_data():
    data = pd.DataFrame(columns=['MP', 'VP', 'VP_avg', 'r', 'dr_dt', 'i_s', 'h', 'T', 'c', 'r_a', 'r_u', 'r_l'])
    data.append({'MP' : MP,
                 'VP': VP,
                 'VP_avg': VP,
                 'r': VP / EP,
                 'dr_dt': 0,
                 'i_s': VP / (EP * c_start),
                 'h': VP / (EP * c_start),
                 'T': 0,
                 'c': c_start,
                 'r_a': VP / EP,
                 'r_u': VP / EP,
                 'r_l': VP / EP, }, ignore_index=True)

def rates ():
    rates = []
    VPs = []

    for j in range(1, len(r_buffer)):
        r_b = r_buffer[j] * (r_buffer[j] / r_buffer[j-1])
        VP_b = VP_buffer[j] * (VP_buffer[j] / VP_buffer[j - 1])
        rates.append(round(r_b, 3))
        VPs.append(round(VP_b, 3))

    rate_avg = sum(rates) / len(rates)
    rate_up = max(rates)
    rate_low = min(rates)
    VP_avg = sum(VPs) / len(VPs)

    if j > 2:
        dr_dt = rates[-1] - rates[-2]
    else: dr_dt = 0

    return rate_avg, rate_up, rate_low, VP_avg, dr_dt

def tendancy ():
    pass

def model (i, t, mod):
    if mod == 'lin':
        h = -(i / t_max) * t + i
        T = (i + (1.01 - i)) / t_max * t
    elif mod == 'quad':
        h = (-i / (t_max**2)) * t**2 + i
        T = (1 / ((t_max - 1)**2)) * t**2
    return h, T

def aggresivity (t, agg):
    if agg == 'cst':
        c = c_finish
    elif agg == 'var':
        c = ((c_finish - c_start) / t_max) * t + c_start
    return c

def record_data(MP, VP, VP_avg, r, dr_dt, i_S, h, T, c, rate_avg, rate_up, rate_low):
    global data
    data = data.append({'MP' : MP,
                        'VP': VP,
                        'VP_avg': VP_avg,
                        'r': r,
                        'dr_dt': dr_dt,
                        'h': h,
                        'T': T,
                        'i_s': i_S,
                        'c': c,
                        'r_a': rate_avg,
                        'r_u': rate_up,
                        'r_l': rate_low}, ignore_index=True)

def set_parameters (parameters):
    global EP, VP, low_var, up_var, c_start, c_finish, agg, mod, t_max, buff_size, a

    EP = int(parameters.get('Entry Price (EP)'))
    VP = EP
    low_var = float(parameters.get('Lower Market Variation Limit'))
    up_var = float(parameters.get('Upper Market Variation Limit'))
    # c_start = 1.5
    c_finish = float(parameters.get('c_factor'))
    # agg = 'var'  # cst or var
    if parameters.get('Model (1 for lin, 2 for quad)') == 1:
        mod = 'lin'
    elif parameters.get('Model (1 for lin, 2 for quad)') == 2:
        mod = 'quad'
    t_max = int(parameters.get('Trading rounds'))
    buff_size = int(parameters.get('Buffer size'))
    a = 0
    set_data()

def set_real_VP (stock):
    global MP, f, VP
    MP = round(float(rh.get_latest_stock_price(stock)[0]), 3)
    VP = MP * f
    return VP

def set_sim_VP ():
    global VP
    VP = round(VP + random.uniform(VP * low_var, VP * up_var), 3)
    return VP

def live_simulate (t, stock):
    global EP, MP, f, VP, low_var, up_var, a, c_start, c_finish, t_max, data, a

    if trading_type == 'rs' or trading_type == 'rh':
        VP = set_real_VP(stock)
    elif trading_type == 'fs':
        VP = set_sim_VP()

    r = VP / EP
    buffer_adjust(r, VP)

    rate_avg, rate_up, rate_low, VP_avg, dr_dt = rates()
    c = aggresivity(t, agg)
    i = round(r / c, 3)
    h, T = model(i, t, mod)
    i_S = determine_i_S(h, T)
    if i_S > 1 and a == 0:
        a = 1
    record_data(MP, VP, VP_avg, r, dr_dt, i_S, h, T, c, rate_avg, rate_up, rate_low)
    return data

def get_a():
    return a

def determine_i_S (h, T):
    i_S = h + T
    return i_S

def set_trading_type(type):
    global trading_type
    trading_type = type


def generate_dataset(u):
    global EP, VP, low_var, up_var, a, c_start, c_finish, t_max, data, a, trading_type

    t_max = u

    set_trading_type('fs')

    for t in range(t_max):
        live_simulate(t, stock='SIM')

    return data

def set_f (stock):
    global f
    MP = round(float(rh.get_latest_stock_price(stock)[0]), 3)
    f = EP / MP

def get_f ():
    return f

