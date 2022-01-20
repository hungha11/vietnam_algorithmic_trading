import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


url = 'https://tcinvest.tcbs.com.vn/tc-price/tc-analysis/dashboard?ticker=TCB'
r = requests.get(url)
soup = bs(r.content,'html.parser')
market_cap = soup.find('img', {'alt':'Avatar'})['src']


#data = requests.get(api).json()
#print(data)