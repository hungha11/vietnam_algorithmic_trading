import vnquant.DataLoader as dl
import pandas as pd
import numpy_financial as npf


class SimpleForcast:
    def __init__(self, symbol):
        self.symbol = symbol




    def get_data(self):
        start = '2021-01-01'
        end = '2021-12-31'
        loader = dl.DataLoader(self.symbol, start, end, data_source='VND', minimal=True)
        data = loader.download()
        close_data = data['close'].dropna()
        data = pd.DataFrame(close_data)
        self.historical_data = data
        return self.historical_data

    def calculate_ROI(self):
        data = self.historical_data.copy().dropna()
        initial_investment = -1000000000

        symbol_string = data[self.symbol]
        price = []
        for i in symbol_string:
            price.append(i)

        number_of_stock = round(-initial_investment / (price[0] * 1000), -2)

        ROI = (price[-1] * number_of_stock -
               (price[0] * number_of_stock)) / (number_of_stock * price[0])
        ROI = round(ROI, 2)
        ROI = "{:.0%}".format(ROI)
        string = f'The ROI for {self.symbol} (1 year) is: '
        final = string + ROI
        return final




if __name__ == '__main__':
    # list = ['HAH','MSN','VIC','ACB','TCB']
    # for names in list:
    #     name = SimpleForcast(names)
    #     name.get_data()
    #     print(name.calculate_ROI())
    VHM = SimpleForcast('VHM')
    VHM.get_data()
    print(VHM.calculate_ROI())
    stocks = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/MomentumStrategy/Data/VN30.csv')
    symbol_groups = list(stocks['Ticker'])
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(symbol_groups[i])

    for name in symbol_strings:
        company = SimpleForcast(name)
        company.get_data()
        output = company.calculate_ROI()
        print(output)

