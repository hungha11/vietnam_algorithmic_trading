import pandas as pd
import vnquant.DataLoader as dl
from datetime import datetime

stocks = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/MomentumStrategy/Data/VN30.csv')
symbol_groups = list(stocks['Ticker'])
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(symbol_groups[i])
    #print(symbol_strings[i])


#%%
start = '2010-01-01'
now  = datetime.now()
end = now.strftime("%Y-%m-%d")
loader = dl.DataLoader(symbol_strings, start,end, data_source='VND', minimal=True)
data = loader.download()
close_data = data['close'].dropna()
close_data.to_csv('VN30 historical price', index = True)


#%%

