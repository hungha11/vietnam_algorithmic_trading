import pandas as pd
import vnquant.DataLoader as dl
import numpy_financial as npf
import numpy as np


symbol_list = ['MSN','MCH','PET','DGW','PNJ','MWG']
start = '2021-01-01'
end = '2021-12-31'
loader = dl.DataLoader(symbol_list, start,end, data_source='VND', minimal=True)
data = loader.download()
close_data = data['close'].dropna()
data = pd.DataFrame(close_data)



initial_investment = -1000000000


#%%
def calculate_ROI(symbol):
    symbol_string = data[symbol]
    price =[]
    for i in symbol_string:
        price.append(i)
    number_of_stock = round(-initial_investment/ (price[0]* 1000),-2)

    ROI = (price[-1]*number_of_stock-
           (price[0]*number_of_stock))/(number_of_stock*price[0])
    ROI = round(ROI,2)
    ROI = "{:.0%}".format(ROI)
    string = f'The ROI for {symbol} is: '
    final = string + ROI
    return  final





for i in symbol_list:
    print(calculate_ROI(i))