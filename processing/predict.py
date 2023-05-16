import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from functions.fileManipulation import loadData, saveDataToFile, appendSymbol
from processing.plotCreation import createPlot
pastDaysNumber = 30
predictionDaysNumber = 7

def prepareData(dataJson):
    selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data = pd.DataFrame.from_dict(dataJson, orient='index')
    pastPredicted = data['Real']
    data = data[selected_columns]
    data = data.fillna(method='ffill')
    y = data['Close']
    y = y.values.reshape(-1, 1)

    return data, y, pastPredicted

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

    return model

def generatePredictions(model, scaler, y):
    X_ = y[- pastDaysNumber:]
    X_ = X_.reshape(1, pastDaysNumber, 1)

    Y_ = model.predict(X_).reshape(-1, 1)
    Y_ = scaler.inverse_transform(Y_)

    return X_, Y_

def getActualDataFrame(data):
    actualDF = data[['Close', 'Real']].reset_index()
    actualDF.rename(columns={'index': 'Date', 'Close': 'Actual', 'Real': 'Real'}, inplace=True)
    actualDF['Date'] = pd.to_datetime(actualDF['Date'])
    actualDF['Future'] = None
    actualDF.loc[actualDF.index[-1], 'Future'] = actualDF.loc[actualDF.index[-1], 'Actual']

    actualDF['Predicted'] = None
    
    actualDF['RealPom'] = True
    
    for indexDate, row in actualDF.iterrows():  
        if row['Real'] is False:
            actualDF.loc[indexDate, 'RealPom'] = False
            
            if indexDate-1 in actualDF.index:
                actualDF.loc[indexDate-1, 'RealPom'] = False
        
            if indexDate+1 in actualDF.index:
                actualDF.loc[indexDate+1, 'RealPom'] = False
                

    actualDF.loc[~actualDF['RealPom'], 'Predicted'] = actualDF.loc[~actualDF['RealPom'], 'Actual']
    actualDF.loc[~actualDF['Real'], 'Actual'] = None
    del actualDF['Real']
    del actualDF['RealPom']
    
    return actualDF

def getPredictionDataFrame(actualDF, Y_):
    predictionDF = pd.DataFrame(columns=['Date', 'Actual', 'Future'])
    predictionDF['Date'] = pd.date_range(start=actualDF['Date'].iloc[-1] + pd.Timedelta(days=1), periods=predictionDaysNumber)
    predictionDF['Future'] = Y_.flatten()
    predictionDF['Actual'] = None
    predictionDF['Predicted'] = None

    return predictionDF

def makePrediction(symbol):
    dataJson = loadData("data_"+symbol+".json")
    
    data, y, pastIsReal = prepareData(dataJson)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y)
    y = scaler.transform(y)

    X, Y = getPastAndPredictionData(y)

    if X.size == 0 or y.size == 0:
        return
    
    model = getFittedModel(X, Y)

    X_, Y_ = generatePredictions(model, scaler, y)
    
    dataWithReals = data.join(pastIsReal)
    actualDF = getActualDataFrame(dataWithReals)
    predictionDF = getPredictionDataFrame(actualDF, Y_)

    results = pd.concat([actualDF, predictionDF]).set_index('Date')
    results = results.replace(np.nan,None)
    resultsJson = {}
    
    for index, row in results.iterrows():
        row_dict = row.to_dict()
        resultsJson[index.strftime('%Y-%m-%d')] = row_dict
    
    saveDataToFile(symbol+"_plotData.json", resultsJson)
    createPlot(symbol)
    appendSymbol("symbolsPredicted.json", symbol)
    