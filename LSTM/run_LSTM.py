from database.mongodb import Database
# from LSTM.LSTM_model import *
import pandas as pd

#Chercher les collections dans la bdd

database= Database('DowJonesStocks')

#recupere un dic de dataframes 
dic_df={}
for i in database.get_list_collections():
        stock_i=list(database.find(i,None))
        df_i = pd.DataFrame(stock_i)
        dic_df[i]= df_i

print(dic_df)

    

