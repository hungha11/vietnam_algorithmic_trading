import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import vnquant.DataLoader as dl
from datetime import datetime
from scipy.optimize import brute
import matplotlib.pyplot as plt
#from Forecasting_techniques.SimpleForcasting import *
#VN30






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

#Backtesting section

###SMA strategy:
###### Things neeed to be done here!!!!!!!!!




















if __name__ =='__main__':
    # streamlit section
    # streamlit is web host for data project, with a few line of code, people can easily deploy
    # a app into web.
    '''
    #       Vietnam Algorithmic trading 
    '''


    # st.write('Algorithmic trading for Vietnam stock market (VN30 only)')
    page = st.sidebar.selectbox('Choose a page', ['Home', 'Portfolio', 'Forecast', 'Result'])

    #                                                   Home
    if page == 'Home':
        st.title('Homepage')

        st.write('Vietnam is a frontier market. In 2021, Vietnam had the highest return compared to others.')
        st.write("Although there's still a lack in the data (due to different IPO date from the companies) , "
                 " this project is still tempting to apply machine into trading activity.")
        #st.write('The project only executes for the VN30 or VN100 index.')
        st.write(""" ***""")
        image = Image.open('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/Vietnam quant/streamlit/vietnam-stock-market-graph-business-ho-chi-minh-stock-index-trading-and-analysis-investment-financial-board-display-double-exposure-money-price-stoc-2AB1HBP.jpeg')
        st.image(image, use_column_width=True)
        st.write(""" ***""")





        st.sidebar.write(""" ***""")
        st.sidebar.write('Algorithmic trading is the best combination of data science and finance!')






    #                                                   Portfolio
    if page == 'Portfolio':
        st.title("Portfolio")
        #main page
        #st.write('This is portfolio allocation')
        with st.expander("1st idea of allocation"):
            st.write("""OOPS\n
            Hey I am chilling before the next semester\n
            How interesting it is.
            """)
            st.write(""" 22222\n
                        Hey I am chilling before the next semester\n
                        How interesting it is.
                        """)


        #sidebar
        st.sidebar.write("""***""")
        st.sidebar.write("There are many tactics when it comes to portfolio allocation. This project provide you with: (on the go, not found yet)   : )"
                         "")


    #                                                   Forecast

    if page == 'Forecast':
        #mainpage
        st.title('Forecasting and Backtesting')
        st.write('The index VN30 or VN100 is also available.')
        with st.expander("Description"):
            st.write("""
            ROI\n
            ROI (Return on Investment) is a simple and provide investor the overview of the performance of the particular stock in a timeframe (1 year for example)""")
            st.write("""***""")
            st.write("""
                        SMA\n
                        There are a "fast" line and a "slow" line when it comes to this strategy. 
                        The fast line is made of the mean of a particular numbers of days (usually <52 days)
                        The slow line is made of the mean of a longer timeframe (252 for example). \n
                        When the fast line cross over the slow line, that's the signal of a bull trend.
                        On the other hand, if the fast line cross down the slow line, that's the signal of bear trend.
                        """)
            st.write("""***""")
            st.write(""" 
            Momentum\n
            Momentum trader believes in the continual trend of a particular stock. 
            If a stock is doing well (go up), it will continue that trend.  
            
            
            """)
        st.write("""***""")
        ticker = st.text_input('Please enter the stock you want to forecast: ')

        #Capitalize the symbol
        if ticker.islower() == True:
            ticker = ticker.upper()


        ##Calculate ROI for stock
        if ticker == '':
            st.write('Please enter a symbol')
        elif ticker == 'VN30':
            stocks = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/MomentumStrategy/Data/VN30.csv')
            symbol_groups = list(stocks['Ticker'])
            symbol_strings = []
            for i in range(0, len(symbol_groups)):
                symbol_strings.append(symbol_groups[i])

            for name in symbol_strings:
                company = SimpleForcast(name)
                company.get_data()
                output = company.calculate_ROI()
                st.write(output)
        elif ticker == 'VN100':
            stocks = pd.read_csv('/Users/haquochung/OneDrive/OneDrive - RMIT University/Home/PyCharm/Vietnam quant/streamlit/Data/VN100.csv')
            symbol_groups = list(stocks['Ticker'])
            symbol_strings = []
            for i in range(0, len(symbol_groups)):
                symbol_strings.append(symbol_groups[i])

            for name in symbol_strings:
                company = SimpleForcast(name)
                company.get_data()
                output = company.calculate_ROI()
                st.write(output)
        else:
            company = SimpleForcast(ticker)
            company.get_data()
            output = company.calculate_ROI()
            st.write(output)
        #sidebar
        st.sidebar.write("""***""")
        st.sidebar.write('There are a lot of techniques which can be used for forecasting.')
        st.sidebar.write('One of them are using historical performance.')
        st.sidebar.write('This project will use ROI, and backtesting strategy of SMA and Momentum.')





    #                                                   Result

    if page == 'Result':
        st.title('Result')
        st.write('Still thinking what will be in here. May be the summary of the portfolio and forecast past')

