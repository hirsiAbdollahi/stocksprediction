from database.mongodb import Database
from API.api_alphavantage import dow_jones_stocks
from creds import key_api_alphavantage



#init database
database= Database('DowJonesStocks')

# API Alphavantage
dowjones_stocks_dic = dow_jones_stocks(key_api_alphavantage)

# Insert/update l'historique des 30 valeurs
for k, v in dowjones_stocks_dic.items():
    if len(list(database.find(k,None)))== 0:
        database.insert(k,v)
    else:
        database.update_one(k,{},{"$set": v})




