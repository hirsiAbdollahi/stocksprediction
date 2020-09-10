import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split



# preprocessing de la df (index time series, stocks en float)
def preprocess_timeserie(df):
    df.drop('_id', axis=1, inplace =True)
    df[['1 open','2 high','3 low','4 close','5 volume']]=df[['1 open','2 high','3 low','4 close','5 volume']].astype(float)
    df.rename(columns={'1 open':"open", '2 high':"high", '3 low':"low", '4 close':"close", '5 volume':"volume"}, inplace=True)
    df['date']=pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(axis = 0, inplace=True) 
    return df

def scale_data (data):
    scaler = MinMaxScaler() 
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler
    

def prepare_lstm (df_ts):
    
    #Nous allons utiliser le cours à la fermeture (close)
    data = df['close'].to_frame().values
    #scale
    scaled_data, scaler= scale_data(data)
    # train data
    train_data = scaled_data[0:int(len(data)*0.8), : ]
    #split x_train/ y_train
    x_train=[]
    y_train = []
    for i in range(60,len(train_data)):
        x_train.append(train_data[i-60:i,0])
        y_train.append(train_data[i,0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    #reshape
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    
    return data, scaled_data, scaler, x_train, y_train

def lstm_model (x_train,y_train):
    model = Sequential()
    
    model.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    
    model.add(LSTM(units = 50, return_sequences = True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(units = 50, return_sequences = True))
    model.add(Dropout(0.2))
   
    model.add(LSTM(units = 50))
    model.add(Dropout(0.2))
    
    model.add(Dense(units = 1))

   
    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    model.fit(x_train, y_train, epochs = 5, batch_size = 32)
    
    return model 

def test_lstm_model(scaled_data,data):
    #Test data set
    test_data = scaled_data[int(len(scaled_data)*0.8) - 60: , : ]
    #test data
    x_test = []
    y_test =  data[int(len(scaled_data)*0.8) : , : ] 
    for i in range(60,len(test_data)):
        x_test.append(test_data[i-60:i,0])
        
    x_test = np.array(x_test)
    #Reshape 
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
    return x_test, y_test

def predict_lstm_model (model, x_test, scaler):
    pred = model.predict(x_test) 
    pred = scaler.inverse_transform(pred)
    return pred
    
def cal_rmse (pred, y_test):
    rmse=np.sqrt(np.mean(((pred- y_test)**2)))
    return rmse

def run_lstm (df):

    df_ts = preprocess_timeserie(df)
    data,scaled_data, scaler, x_train, y_train= prepare_lstm (df_ts)
    model = lstm_model (x_train,y_train)
    x_test, y_test= test_lstm_model(scaled_data,data)
    pred = predict_lstm_model (model,x_test,scaler)
    rmse=cal_rmse (pred, y_test)
    
    return pred,rmse
    

    