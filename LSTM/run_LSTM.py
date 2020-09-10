from database.mongodb import Database
from LSTM.LSTM_model import lstm_run_model


import pandas as pd
import pickle
from keras import models

#Chercher les collections dans la bdd

database= Database('DowJonesStocks')

#recuperer un dic de dataframes 
dic_df={}
for i in database.get_list_collections():
        stock_i=list(database.find(i,None))
        df_i = pd.DataFrame(stock_i)
        dic_df[i]= df_i

# Run and save model
dic_pred_rmse={}
for k, v in dic_df.items():
    pred,rmse, model= lstm_run_model(v)
    dic_pred_rmse[k]= {'rmse':rmse, 'pred':pred}
    model.save('./LSTM/{}_LSTM'.format(k))

print(dic_pred_rmse)
    

