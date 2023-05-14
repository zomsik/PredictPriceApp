import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from functions.fileManipulation import loadData, saveDataToFile, appendSymbol

pastDaysNumber = 30
predictionDaysNumber = 7

def loadData(filename):
    jsonData = {}
    with open(filename, 'r') as file:
        jsonData = json.load(file)
    return jsonData

def prepareData(dataJson):
    selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data = pd.DataFrame.from_dict(dataJson, orient='index')
    data = data[selected_columns]
    data = data.fillna(method='ffill')
    y = data['Close']
    y = y.values.reshape(-1, 1)

    return data, y

def getPastAndPredictionData(y):
    X = []
    Y = []
    for i in range(pastDaysNumber, len(y) - predictionDaysNumber + 1):
        X.append(y[i - pastDaysNumber: i])
        Y.append(y[i: i + predictionDaysNumber])
    X = np.array(X)
    Y = np.array(Y)

    return X, Y

def getFittedModel(X, Y):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(pastDaysNumber, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(predictionDaysNumber))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, Y, epochs=100, batch_size=32, verbose=0)

def generatePredictions(model, scaler):
    X_ = y[- pastDaysNumber:]  # last available input sequence
    X_ = X_.reshape(1, pastDaysNumber, 1)

    Y_ = model.predict(X_).reshape(-1, 1)
    Y_ = scaler.inverse_transform(Y_)

    return X_, Y_

def getActualDataFrame(data):
    actualDF = data[['Close']].reset_index()
    actualDF.rename(columns={'index': 'Date', 'Close': 'Actual'}, inplace=True)
    actualDF['Date'] = pd.to_datetime(actualDF['Date'])
    actualDF['Forecast'] = np.nan
    actualDF['Forecast'].iloc[-1] = actualDF['Actual'].iloc[-1]

    return actualDF

def getPredictionDataFrame(actualDF, Y_):
    predictionDF = pd.DataFrame(columns=['Date', 'Actual', 'Forecast'])
    predictionDF['Date'] = pd.date_range(start=actualDF['Date'].iloc[-1] + pd.Timedelta(days=1), periods=predictionDaysNumber)
    predictionDF['Forecast'] = Y_.flatten()
    predictionDF['Actual'] = np.nan

    return predictionDF

def makePrediction(symbol):
    dataJson = loadData(symbol)
    
    data, y = prepareData(dataJson)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y)
    y = scaler.transform(y)

    X, Y = getPastAndPredictionData(y)

    model = getFittedModel(X, Y)

    X_, Y_ = generatePredictions(model, scaler)

    actualDF = getActualDataFrame(data)
    predictionDF = getPredictionDataFrame(actualDF, Y_)

    results = pd.concat([actualDF, predictionDF]).set_index('Date')
    saveDataToFile(symbol+"_plotData.json",results)
    appendSymbol("symbolsPredicted.json", symbol)