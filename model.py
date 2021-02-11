import random
import pandas as pd
import robin_stocks as r

EP = 100
CP = EP

low_var = -0.005
up_var = 0.006
a = 0

c_start = 1.5
c_finish = 1.1
agg = 'cst' # cst or var
mod = 'quad' # lin or quad

t_max = 300

data = pd.DataFrame(columns=['CP', 'CP_avg', 'r', 'dr_dt', 'i_s', 'h', 'T', 'c', 'r_a', 'r_u', 'r_l'])
data.append({'CP': CP,
             'CP_avg': CP,
             'r': CP / EP,
             'dr_dt': 0,
             'i_s': CP / (EP * c_start),
             'h': CP / (EP * c_start),
             'T': 0,
             'c': c_start,
             'r_a': CP / EP,
             'r_u': CP / EP,
             'r_l': CP / EP,}, ignore_index=True)

r_buffer = [CP/EP]
CP_buffer = [CP]
buff_size = 12

def buffer_adjust (r, CP):
    global r_buffer, CP_buffer
    r_buffer.append(round(r, 3))
    CP_buffer.append(CP)
    if len(r_buffer) > buff_size:
        r_buffer.pop(0)

    if len(CP_buffer) > buff_size:
        CP_buffer.pop(0)

def set_data():
    data = pd.DataFrame(columns=['CP', 'CP_avg', 'r', 'dr_dt', 'i_s', 'h', 'T', 'c', 'r_a', 'r_u', 'r_l'])
    data.append({'CP': CP,
                 'CP_avg': CP,
                 'r': CP / EP,
                 'dr_dt': 0,
                 'i_s': CP / (EP * c_start),
                 'h': CP / (EP * c_start),
                 'T': 0,
                 'c': c_start,
                 'r_a': CP / EP,
                 'r_u': CP / EP,
                 'r_l': CP / EP, }, ignore_index=True)

def rates ():
    rates = []
    CPs = []
    for j in range(1, len(r_buffer)):
        r_b = r_buffer[j] * (r_buffer[j] / r_buffer[j-1])
        CP_b = CP_buffer[j] * (CP_buffer[j] / CP_buffer[j-1])
        rates.append(round(r_b, 3))
        CPs.append(round(CP_b, 3))
    rate_avg = sum(rates) / len(rates)
    rate_up = max(rates)
    rate_low = min(rates)
    CP_avg = sum(CPs) / len(CPs)
    if j > 2:
        dr_dt = rates[-1] - rates[-2]
    else: dr_dt = 0
    return rate_avg, rate_up, rate_low, CP_avg, dr_dt

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

def record_data(CP, CP_avg, r, dr_dt, i_S, h, T, c, rate_avg, rate_up, rate_low):
    global data
    data = data.append({'CP': CP,
                        'CP_avg': CP_avg,
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
    global EP, CP, low_var, up_var, c_start, c_finish, agg, mod, t_max, buff_size, a
    EP = int(parameters.get('Entry Price (EP)'))
    CP = EP
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

def set_real_CP (stock):
    global CP
    CP = round(float(r.stocks.get_latest_price(stock)[0]), 3)

def set_sim_CP():
    global CP
    CP = round(CP + random.uniform(CP * low_var, CP * up_var), 3)

def live_simulate(t, stock):
    global EP, CP, low_var, up_var, a, c_start, c_finish, t_max, data, a

    if stock == 'SIM':
        set_sim_CP()
    else: set_real_CP(stock)

    r = CP / EP
    buffer_adjust(r, CP)
    rate_avg, rate_up, rate_low, CP_avg, dr_dt = rates()
    c = aggresivity(t, agg)
    i = round(r / c, 3)
    h, T = model(i, t, mod)
    i_S = determine_i_S(h, T)
    if i_S > 1 and a == 0:
        a = 1
    record_data(CP, CP_avg, r, dr_dt, i_S, h, T, c, rate_avg, rate_up, rate_low)
    return data

def get_a():
    return a

def determine_i_S (h, T):
    i_S = h + T
    return i_S