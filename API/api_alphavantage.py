from API.dowjones_tickers import scrap_tickers
import requests
import json
import re


def get_stock_timeserie_alphavantage(ticker, api_key):
    url = "https://www.alphavantage.co/query?"
    querystring = {"outputsize":"full","datatype":"json","function":"TIME_SERIES_DAILY","symbol":ticker,"apikey":api_key}
    response = requests.request("GET", url, params=querystring)
    stock_json = response.json()
    stock= stock_json['Time Series (Daily)']
    return stock


## Recuperation times series sur alphavantage
def get_stock_timeserie_alphavantage(ticker, api_key):
    url = "https://www.alphavantage.co/query?"
    querystring = {"outputsize":"full","datatype":"json","function":"TIME_SERIES_DAILY","symbol":ticker,"apikey":api_key}
    response = requests.request("GET", url, params=querystring)
    stock_json = response.json()
    print(stock_json)
    stock= stock_json['Time Series (Daily)']
    return stock

## Enlever le dot sinon impossible d'inserer dans Mongodb
def sanitize(value, is_value=True):
    if isinstance(value, dict):
        value = {sanitize(k,False):sanitize(v,True) for k, v in value.items()}
    elif isinstance(value, list):
        value = [sanitize(v, True) for v in value]
    elif isinstance(value, str):
        if not is_value:
            value = re.sub(r"[.]", "", value)        
    return value

# rajout de la date dans le dict avec comme key date
def prepare_mongo_documents(stock_json_sanitize):
    stock_json_sanitize_ready= [v for k, v in stock_json_sanitize.items()]
    for i in range(len(stock_json_sanitize)):   
        stock_json_sanitize_ready[i]['date']= list(stock_json_sanitize)[i]
    return stock_json_sanitize_ready

# Retourne un dic avec en key nom de l'action et en value l'historique de son cours 
def dow_jones_stocks (api_key):
    tickers_dic = scrap_tickers()
    dowjones_stocks={}
    for k, v in tickers_dic.items():
        stock_json= get_stock_timeserie_alphavantage(v, api_key)
        
        stock_json_sanitize = sanitize(stock_json)
        
        stock_json_sanitize_ready =prepare_mongo_documents(stock_json_sanitize)

        dowjones_stocks[k]= stock_json_sanitize_ready
        
    return dowjones_stocks