import pandas as pd
import vnquant.DataLoader as dl
from datetime import datetime



class DataCollection(object):
    def __init__(self, start):
        self.start = start
        self.collect_symbol()



    def collect_symbol(self):
        self.stocks = pd.read_csv('VN30.csv')
        self.symbol_groups = list(self.stocks['Ticker'])
        self.symbol_strings = []
        for i in range(0, len(self.symbol_groups)):
            self.symbol_strings.append(self.symbol_groups[i])
            #print(symbol_strings[i])
        return self.symbol_strings

    def load_data(self, start, end):

        self.start = start
        self.now = datetime.now()
        self.end = self.now.strftime("%Y-%m-%d")
        loader = dl.DataLoader(self.symbol_strings, self.start, self.end, data_source='VND', minimal=True)
        data = loader.download()
        close_data = data['close'].dropna()

        csv_file = close_data.to_csv('VN30 historical since 2010', index=True)

        return data




if __name__ == '__main__':
    print(DataCollection('2020-01-01'))