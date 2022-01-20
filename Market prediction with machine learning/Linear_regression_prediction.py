import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class LRVectorBacktester(object):
    '''
    Class for vextorized backtesting of Linear fregression-Based trading strategy

    Attributes
    ======================
    symbol: str
    start: str
    end: str
    amount: int, float
    tc: transaction cost


    Methods
    ========================
    get_data: take data from the data set
    select_data: selects a sub-set of data
    prepare_lags: preapres the lagged data for the regression
    fit_model: implements the regression step
    run_strategy: run backtester
    plot_results: plot the performance strategy compared to the symbol
    '''

    def __init__(self, symbol, start, end, amount, tc):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tc
        self.result = None
        self.get_data()

    def get_data(self):

        raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv', index_col=0,parse_dates=True).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns = {self.symbol: 'price'},inplace =True)
        raw['returns'] = np.log(raw/raw.shift(1))
        self.data = raw.dropna()

    def select_data(self, start, end):
        '''
        Selects sub-sets of the financial data
        '''
        data = self.data[(self.data.index >= start) & (self.data.index <= end)].copy()
        return data



    def prepare_lags(self, start, end):
        '''
        Prepare the lagged data for the model

        '''
        data = self.select_data(start,end)
        self.cols=[]
        for lag in range(1, self.lags +1):
            col = f'lag_{lag}'
            data[col] = data['returns'].shift(lag)
            self.cols.append(col)
        data.dropna(inplace = True)
        self.lagged_data = data

    def fit_model(self, start, end):
        '''Implemet the regression step
        '''
        self.prepare_lags(start, end)
        reg = np.linalg.lstsq(self.lagged_data[self.cols], np.sign(self.lagged_data['returns']),rcond=None)[0]
        self.reg = reg

    def run_strategy(self, start_in, end_in, start_out, end_out, lags = 3):
        '''Backtest the strategy
        '''
        self.lags = lags
        self.fit_model(start_in, end_in)
        self.results  = self.select_data(start_out,end_out).iloc[lags:]
        self.prepare_lags(start_out,end_out)
        prediction = np.sign(np.dot(self.lagged_data[self.cols],self.reg))
        self.results['prediction'] = prediction
        self.results['strategy'] = self.results['prediction'] * self.results['returns']
        # determine when a trade take place
        trades = self.results['prediction'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade take places
        self.results['strategy'][trades] -= self.tc
        self.results['creturns'] = self.amount * self.results['returns'].cumsum().apply(np.exp)
        self.results['cstrategy'] = self.amount * self.results['strategy'].cumsum().apply(np.exp)


        # absolute performance of the strategy
        aperf = self.results['cstrategy'].iloc[-1]
        # out -/underperformance of strategy
        operf = aperf - self.results['creturns'].iloc[-1]

        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        if self.results is None:
            print('No resluts to plot yet. Run a strategy')
        title = '%s | TC = %.4f' % (self.symbol, self.tc)
        self.results[['creturns', 'cstrategy']].plot(title=title, figsize=(10, 6))
        plt.show()



if __name__ == '__main__':
    lrbt = LRVectorBacktester('.SPX', '2010-01-01','2018-06-29',100000,0.0)
    print(lrbt.run_strategy('2010-01-01', '2019-12-31', '2010-01-01','2019-12-31'))





