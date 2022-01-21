import numpy as np
import pandas as pd
from scipy.optimize import brute
import streamlit as st
import matplotlib.pyplot as plt
import vnquant.DataLoader as dl
from datetime import datetime
import plotly.figure_factory as ff




class SMAVectorBacktester(object):
    '''
    Class for vextorized backtesting of SMA-Based trading strategy

    Attributes
    ======================
    symbol: str
    SMA1: int // time window in days for shorter SMA
    SMA2: int // time window in days for longer SMA
    start: str
    end: str


    Methods
    ========================
    get_data: take data from the data set
    set_parameters: set one or two new SMA
    run_strategy: run backtester
    plot_results: plot the performance strategy compared to the symbol
    update_and_run: update SMA parameters and returns the (negative) absolute performance
    optimize_parameters: implement a brute force optimization for the two SMA parameters
    '''


    def __init__(self, symbol, SMA1, SMA2, start, end):
        self.symbol = symbol
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.start = start
        self.end = end
        self.results = None
        self.get_data()



    def get_data(self):
        '''Retrieves and prepares the data
        '''
        #raw = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/Vietnam quant/Data_collection/VN30 historical price', index_col=0, parse_dates=True).dropna()
        start = '2010-01-01'
        now = datetime.now()
        end = now.strftime("%Y-%m-%d")
        loader = dl.DataLoader(self.symbol, start, end, data_source='VND', minimal=True)
        pricedata = loader.download()
        close_data = pricedata['close'].dropna()



        #raw = close_data[self.symbol]
        raw = close_data.loc[self.start: self.end]
        raw.rename(columns = {self.symbol:'price'}, inplace = True)
        raw['return'] = np.log(raw/raw.shift(1))
        raw['SMA1'] = raw['price'].rolling(self.SMA1).mean()
        raw['SMA2'] = raw['price'].rolling(self.SMA2).mean()
        self.data = raw

    def set_parameters(self, SMA1=None, SMA2 = None):
        '''
        Updates SMA paremeters and resp. time series
        '''
        if SMA1 is not None:
            self.SMA1 = SMA1
            self.data['SMA1'] = self.data['price'].rolling(self.SMA1).mean()
        if SMA2 is not None:
            self.SMA2 = SMA2
            self.data['SMA2'] = self.data['price'].rolling(self.SMA2).mean()


    def run_strategy(self):
        '''
        Backtesting the trading strategy
        '''
        data = self.data.copy().dropna()
        data['position'] = np.where(data['SMA1'] > data['SMA2'],1,-1)
        data['strategy'] = data['position'].shift(1) * data['return']
        data.dropna(inplace=True)
        data['creturns'] = data['return'].cumsum().apply(np.exp)
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data
        #gross performance
        aperf = data['cstrategy'].iloc[-1]
        #out-/ underperformance of the strategy
        operf = aperf - data['creturns'].iloc[-1]
        return round(aperf,2), round(operf,2)


    def plot_results(self):
        '''
        Plot the cumulative performance of the strategy compared to the symbol
        '''
        if self.results is None:
            print('No result to plot yet. Please run the strategy.')
        #plt.style.use('seaborn')
        #mpl.rcParams['savefig.dpi'] = 300
        #mpl.rcParams['font.family']= 'serif'
        title = '%s | SMA1 = %d, SMA2=%d' % (self.symbol, self.SMA1, self.SMA2)
        self.results[['creturns', 'cstrategy']].plot(title = title, figsize = (10,6))
        plt.show()
    def st_plot_results(self):
        '''
        Plot the cumulative performance of the strategy compared to the symbol
        '''
        if self.results is None:
            print('No result to plot yet. Please run the strategy.')
        # plt.style.use('seaborn')
        # mpl.rcParams['savefig.dpi'] = 300
        # mpl.rcParams['font.family']= 'serif'
        title = '%s | SMA1 = %d, SMA2=%d' % (self.symbol, self.SMA1, self.SMA2)
        self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(10, 6))
        fig,ax= plt.subplot()
        ax.line()
        st.pyplot(fig)

    def update_and_run(self, SMA):
        '''
        Updates SMA parameters and returns negative absolute performance (for minimization algorithms)
        Parameters
        ========
        SMA: tuples// SMA parameter tuple
        '''

        self.set_parameters(int(SMA[0]), int(SMA[1]))
        return -self.run_strategy()[0]

    def optimization_parameters(self, SMA1_range, SMA2_range):
        '''
        Parameter
        ========
        SMA1_range, SMA2_range: tuple //tuple of the form (start, end, step size)
        '''
        opt = brute(self.update_and_run, (SMA1_range, SMA2_range), finish= None)
        return opt, -self.update_and_run(opt)

if __name__ =='__main__':
    # smabt = SMAVectorBacktester('HAH', 52, 252, '2019-01-01','2022-01-14')
    # print(smabt.run_strategy())
    # smabt.plot_results()
    ticker = input('Enter a string')
    slow = int(input('enter a number'))
    fast = int(input('enter a number'))
    smabt = SMAVectorBacktester(ticker, slow, fast, '2019-01-01','2022-01-14')
    print(smabt.run_strategy())
    smabt.plot_results()
    #print(smabt.optimization_parameters((30,56,4),(200,300,4)))
    #smabt.plot_results()



