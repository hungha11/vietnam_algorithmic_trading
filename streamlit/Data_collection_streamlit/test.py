import pandas as pd
import vnquant.DataLoader as dl
from datetime import datetime


def collect_symbol(index):
    symbol_strings = []
    if index == 'VN30':
        stocks = pd.read_csv('VN30.csv')
        symbol_groups = list(stocks['Ticker'])
        for i in range(0, len(symbol_groups)):
            symbol_strings.append(symbol_groups[i])
            # print(symbol_strings[i])
    elif index == 'VN100':
        stocks = pd.read_csv('VN100.csv')
        symbol_groups = list(stocks['Ticker'])
        for i in range(0, len(symbol_groups)):
            symbol_strings.append(symbol_groups[i])
            # print(symbol_strings[i])
    else:
        print('Wrong index.\nPlease try again.')



    return symbol_strings
    
def load_data(index):
    start = '2010-01-01'
    now = datetime.now()
    end = now.strftime("%Y-%m-%d")
    loader = dl.DataLoader(collect_symbol(index), start,end, data_source='VND', minimal=True)
    data = loader.download()
    close_data = data['close'].dropna()

    csv_file = close_data.to_csv(f'{index} historical since 2010', index=True)

    return data


if __name__ == '__main__':
    load_data('VN30')

#compare to the sytematic and procedure way, this quite lower and not as effeicient as.