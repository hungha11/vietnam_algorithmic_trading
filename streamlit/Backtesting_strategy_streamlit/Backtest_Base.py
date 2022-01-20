import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl,plt
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'




class BacktestBase(object):
    '''
    base class for event-based backtesting of trading strategies


    Attributes
    =========
    symbol: str
    Start
    end
    amount: int, float // amount to invest at the beginning
    ftc: float // fixed transaction per trade (buy or sell)
    ptc: float // proportional transaction costs per trade


    Methods
    =========
    get_data:
    plot_data:
    get_date_price: return dates and price for the given bar
    print_balance: print out the current cash balance
    print_net_wealth: print out the current net wealth
    place_buy_order: place a buy order
    place_sell_order: place a sell order
    close_out: close position
    '''


    def __init__(self, symbol,start, end, amount, ftc =0.0, ptc = 0.0, verbose = True):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = ptc
        self.units = 0
        self.position = 0
        self.trades = 0
        self.verbose = verbose
        self.get_data()

    def get_data(self):

        #raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv', index_col=0,parse_dates=True).dropna()
        raw = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/Vietnam quant/Data_collection/VN30 historical since 2010', index_col=0,parse_dates=True).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns = {self.symbol: 'price'},inplace =True)
        raw['returns'] = np.log(raw/raw.shift(1))
        self.data = raw.dropna()
    def plot_data(self, cols = None):
        '''Plot the closing price for symbol
        '''
        if cols is None:
            cols = ['price']
        self.data['price'].plot(figsize = (10,6), title = self.symbol)
        plt.show()

    def get_date_price(self, bar):
        '''Return date and price for bar
        '''
        date = str(self.data.index[bar])[:10]
        price = self.data.price.iloc[bar]
        return date, price



    def print_balance(self, bar):
        date, price = self.get_date_price(bar)
        print(f'{date} | current balance {self.initial_amount:.2f}')


    def print_net_wealth(self, bar):
        date, price = self.get_date_price(bar)
        net_wealth = self.units * price +self.amount
        print(f'{net_wealth} | current net wealth {net_wealth:.2f}')

    def place_buy_order(self, bar,units= None, amount = None):
        '''place a buy order
        '''
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount/price)
        self.amount -= (units*price) * (1+self.ptc) + self.ftc
        self.units += units
        self.trades +=1
        if self.verbose:
            print(f'{date} | selling {units} units at {price:.2f}')
            self.print_balance(bar)
            self.print_net_wealth(bar)

    def sell_buy_order(self, bar,units = None, amount = None):
        '''Place a sell order
        '''
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount/price)
        self.amount += (units*price) * (1+self.ptc) - self.ftc
        self.units -= units
        self.trades +=1
        if self.verbose:
            print(f'{date} | selling {units} units at {price:.2f}')
            self.print_balance(bar)
            self.print_net_wealth(bar)
    
    
    def close_out(self, bar):
        '''Closing a position
        '''
        
        date, price = self.get_date_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades +=1
        if self.verbose:
            print(f'{date} | inventory {self.units} units at {price:.2f}')
            print('=' * 55)
        print('Final balance    [VND] {:.2f'.format(self.amount))
        perf = ((self.amount - self.initial_amount)/self.initial_amount  * 100)
        print('Net performance [%] {:.2f}'.format(perf))
        print('Trade Execute [#] {:.2f}'.format(self.trades))
        print('='*55)
        
if __name__ == '__main__':
    #bb = BacktestBase('AAPL.O', ' 2018-01-01','2020-01-01', 1000000)
    bb = BacktestBase('VPB', ' 2018-01-01','2022-1-16', 1000000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()

        





