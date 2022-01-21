#ROI section:
class SimpleForcast:
    def __init__(self, symbol):
        self.symbol = symbol
    def get_data(self):
        start = '2021-01-01'
        end = '2021-12-31'
        loader = dl.DataLoader(self.symbol, start, end, data_source='VND', minimal=True)
        data = loader.download()
        close_data = data['close'].dropna()

        self.historical_data = pd.DataFrame(close_data)
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
        string = f'The ROI for {self.symbol} (2021 only) is: '
        final = string + ROI
        return final