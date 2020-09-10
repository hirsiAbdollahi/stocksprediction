
from bs4 import BeautifulSoup
import requests
import re

def scrap_tickers():
    url = 'https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI'
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html.parser')

    tickers_dic={}
    for i in soup.findAll('tbody'):
        for j in i.findAll('tr'):
                ticker = j.find('td').text
                name= j.findAll('td')[1].text
                tickers_dic[name]=ticker
    #remove dots
    tickers_dic={re.sub(r"\.+", "", k):v for k,v in tickers_dic.items()}     
    
    return tickers_dic


