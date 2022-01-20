from Momentum_backtesting_strategy import *



class MRVectorBacktester(MomVectorBacktester):
    '''
    Class for the vectorized backtesting of mean reversion-based trading strategies

    Attributes:
    ======
    symbol: str
    Start
    end
    amount: int, float // amount to invest at the beginning
    tc: float // proportional transaction costs per trade

    Methods
    =========
    get_data
    run_strategy
    plot_results
    '''

    def run_strategy(self, SMA, threshold):
        '''
        Beck testing the strategy
        '''

        data = self.data.copy().dropna()
        data['sma'] = data['price'].rolling(SMA).mean()
        data['distance'] = data['price'] - data['sma']
        data.dropna(inplace = True)

        #sell signals
        data['positions'] = np.where(data['distance']  > threshold, -1, np.nan)

        #buy signal
        data['positions'] = np.where(data['distance'] < -threshold, 1, data['positions'])

        #crossing of current price and SMA (zero distance
        data['positions'] = np.where(data['distance']*data['distance'].shift(1)<0, 0, data['positions'])
        data['positions'] = data['positions'].ffill().fillna(0)
        data['strategy'] = data['positions'].shift(1)*data['return']


        #determine when a trade take place
        trades = data['positions'].diff().fillna(0) != 0
        #subtract transaction costs from return when trade take places
        data['strategy'][trades] -= self.tc
        data['creturns'] = self.amount * data['return'].cumsum().apply(np.exp)
        data['cstrategy'] = self.amount * data['strategy'].cumsum().apply(np.exp)
        self.result = data

        #absolute performance of the strategy
        aperf = self.result['cstrategy'].iloc[-1]
        #out -/underperformance of strategy
        operf = aperf - self.result['creturns'].iloc[-1]

        return round(aperf,2), round(operf,2)
if __name__ == '__main__':
    mrbt = MRVectorBacktester('VIC','2019-01-01','2021-12-31', 100000, 0.0)
    #mombt  = MomVectorBacktester('VIC', '2020-01-01', ' 2022-01-14',10000000, 0.003)
    print(mrbt.run_strategy(SMA=25, threshold=5))
    mrbt = MRVectorBacktester('VHM','2018-01-01','2022-01-16',1000000000,0.003)
    print(mrbt.run_strategy(SMA = 22, threshold=7.5))






