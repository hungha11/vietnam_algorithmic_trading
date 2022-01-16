import numpy as np
import pandas as pd
import vnquant.DataLoader as dl

stocks = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/MomentumStrategy/Data/VN30.csv')
symbol_groups = list(stocks['Ticker'])
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(symbol_groups[i])
    #print(symbol_strings[i])


#%%

loader = dl.DataLoader(symbol_strings, '2015-01-01','2022-01-16', data_source='VND', minimal=True)
data = loader.download()
close_data = data['close'].dropna()
close_data.to_csv('VN30 historial price', index = True)