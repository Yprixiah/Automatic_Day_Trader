import random
from random import randint
import matplotlib.pyplot as plt

#Generate market related collections and parameters
market0 = {'t1': randint(10, 100),
          't2': randint(10, 100),
          't3': randint(10, 100),
          't4': randint(10, 100),
          't5': randint(10, 100),
          't6': randint(10, 100),
          't7': randint(10, 100),
          't8': randint(10, 100),
          't9': randint(10, 100),
          't10': randint(10, 100)}
stocks_var = {'t1': {},
          't2': {},
          't3': {},
          't4': {},
          't5': {},
          't6': {},
          't7': {},
          't8': {},
          't9': {},
          't10': {}}
up_var = 0.022
low_var = -0.018

#Declare initial investement conditions
ini = 200
r = ini/10
reserve = 20

#Generate initial portfolio
#           0               1                     2            3      4           5               6
#header: buy/sell_round, last_action_price, total_investment, share, exces, last_action, number_last_action
portfolio = {'t1': [0, market0.get('t1'), r, round(r / market0.get('t1'), 3), 0, 'b', 1],
             't2': [0, market0.get('t2'), r, round(r / market0.get('t2'), 3), 0, 'b', 1],
             't3': [0, market0.get('t3'), r, round(r / market0.get('t3'), 3), 0, 'b', 1],
             't4': [0, market0.get('t4'), r, round(r / market0.get('t4'), 3), 0, 'b', 1],
             't5': [0, market0.get('t5'), r, round(r / market0.get('t5'), 3), 0, 'b', 1],
             't6': [0, market0.get('t6'), r, round(r / market0.get('t6'), 3), 0, 'b', 1],
             't7': [0, market0.get('t7'), r, round(r / market0.get('t7'), 3), 0, 'b', 1],
             't8': [0, market0.get('t8'), r, round(r / market0.get('t8'), 3), 0, 'b', 1],
             't9': [0, market0.get('t9'), r, round(r / market0.get('t9'), 3), 0, 'b', 1],
             't10': [0, market0.get('t10'), r, round(r / market0.get('t10'), 3), 0, 'b', 1]}
# print('Initial', portfolio)

#Determine investement strategie and collections
buy_rate = -0.05
sell_rate = 0.5
buy_power = {}
buy_power[0] = reserve

#Declare plotting collections
value_per_stock = {'t1': r,
          't2': r,
          't3': r,
          't4': r,
          't5': r,
          't6': r,
          't7': r,
          't8': r,
          't9': r,
          't10': r}
share_per_stock = {'t1': {},
          't2': {},
          't3': {},
          't4': {},
          't5': {},
          't6': {},
          't7': {},
          't8': {},
          't9': {},
          't10': {}}
running = {}

def buy (self, key, gap, i):
    global reserve

    n = portfolio.get(key)[6]
    if portfolio.get(key)[5] == 'b':
        n = n + 1
    elif portfolio.get(key)[5] == 's':
        n = 1

    inv = int(portfolio.get(key)[4])
    if inv == 0:
        inv = abs(portfolio.get(key)[1] * gap*portfolio.get(key)[3])

    share_bought = inv / market0.get(key)
    reserve = reserve - inv
    portfolio[key] = [i,
                      market0.get(key),
                      round(portfolio.get(key)[2] + inv, 3),
                      round(portfolio.get(key)[3] + share_bought, 3),
                      0,
                      'b',
                      n]

def sell(self, key, gap, i):
    global reserve

    n = portfolio.get(key)[6]
    if portfolio.get(key)[5] == 's':
        n = n + 1
    elif portfolio.get(key)[5] == 'b':
        n = 1

    share_sold = abs(portfolio.get(key)[3] * gap)
    if share_sold > 1:
        share_sold = 1
    gain = round(portfolio.get(key)[3] * (market0.get(key) - portfolio.get(key)[1]), 3)
    reserve = reserve + gain
    portfolio[key] = [i,
                      market0.get(key),
                      portfolio.get(key)[2],
                      round(portfolio.get(key)[3] - share_sold, 3),
                      round(gain, 3),
                      's',
                      n]

def simulate(self):
    global reserve
    for i in range(1,250):

        for key in portfolio:
            # Update market with new rate
            rate = round(random.uniform(low_var * market0.get(key), up_var * market0.get(key)), 3)
            market0[key] = round(market0[key] + rate, 3)

            #Determine the change rate compared to the last action for that stock
            gap = (market0.get(key) - portfolio.get(key)[1]) / portfolio.get(key)[1]

            #test if buying or selling that stock
            if (portfolio.get(key)[5] == 'b' and portfolio.get(key)[6] < 3 and gap <= buy_rate and reserve > 0):
                self.buy(key, gap, i)

            elif (portfolio.get(key)[5] == 'b' and gap >= sell_rate):
                self.sell(key, gap, i)

            elif (portfolio.get(key)[5] == 's' and portfolio.get(key)[6] < 3 and gap >= sell_rate):
                self.sell(key, gap, i)

            elif (portfolio.get(key)[5] == 's' and gap <= buy_rate and reserve > 0):
                self.buy(key, gap, i)
            else:
                pass

            #Populate plotting collextions
            stocks_var.get(key)[i] = market0.get(key)
            share_per_stock.get(key)[i] = portfolio.get(key)[3]
            value_per_stock[key] = portfolio.get(key)[3] * market0.get(key)

        running[i] = sum(value_per_stock.values()) + reserve
        buy_power[i] = reserve

simulate()

#Plot results of simulation
fig1, ax = plt.subplots()
for key in stocks_var:
    line = ax.data(*zip(*sorted(stocks_var[key].items())), label = key)
    ax.legend()
plt.title("Market")

fig3, ax = plt.subplots()
for key in stocks_var:
    line = ax.data(*zip(*sorted(share_per_stock[key].items())), label = key)
    ax.legend()
plt.title("Shares")

fig4, ax = plt.subplots()
ax.data(*zip(*sorted(buy_power.items())))
plt.title('Cash Reserve')

fig5, ax = plt.subplots()
ax.data(*zip(*sorted(running.items())))
plt.title('Total Value')

print('End', portfolio)
# print(running)
rate = (running.get(249) - running.get(1)) / running.get(1)
print(rate * 100)
plt.show()