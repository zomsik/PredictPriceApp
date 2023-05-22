import schedule
import threading
from datetime import timedelta, date
import socket
from functions.fileManipulation import getSymbolList, loadData, saveDataToFile
from functions.downloadData import downloadData
import pandas as pd
from processing.predict import makePrediction
import numpy as np

def check_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def internetTask():
    todayDate = date.today()
    for symbol in getSymbolList("symbolsPredicted.json"):
        symbolData = loadData("data_"+symbol+".json")
        
        symbolData = pd.DataFrame.from_dict(symbolData, orient='index')
        symbolData.index = pd.to_datetime(symbolData.index)

        previousDate = symbolData.iloc[-1].name + timedelta(days=1)
        
        newDownloadedData = downloadData(symbol,previousDate,todayDate)
        newDownloadedData['Real'] = True  
        
        symbolData = pd.concat([symbolData, newDownloadedData])
        symbolData = symbolData.iloc[len(newDownloadedData.index):] 
            
        symbolData = symbolData.replace(np.nan,None)
        new_data = {}

        for index, row in symbolData.iterrows():
            row_dict = row.to_dict()
            new_data[index.strftime('%Y-%m-%d')] = row_dict
        
        saveDataToFile("data_"+symbol+".json", new_data)
        makePrediction(symbol)

        

def noInternetTask():
    todayDate = date.today()
    for symbol in getSymbolList("symbolsPredicted.json"):
        symbolData = loadData("data_"+symbol+".json")
        symbolData = pd.DataFrame.from_dict(symbolData, orient='index')
        symbolData.index = pd.to_datetime(symbolData.index)
           
        predictedData = loadData(symbol+"_plotData.json")
        predictedData = pd.DataFrame.from_dict(predictedData, orient='index')
        predictedData.index = pd.to_datetime(predictedData.index)

        lastActualDataEntry = symbolData.iloc[-1]
        PreviousRows = predictedData[predictedData.index >= lastActualDataEntry.name]

        rowsToDelete = []
        for index, row in PreviousRows.iterrows():
            if index in symbolData.index or index.weekday() >= 5 or index.date() >= todayDate:
                rowsToDelete.append(index)

        PreviousRows = PreviousRows.drop(rowsToDelete)
        
        for index, row in PreviousRows.iterrows():
            symbolData = symbolData.iloc[1:]
            lastClose = symbolData.iloc[-1]["Close"]
            
            
            newPredictedPrice = row["Future"]
            
            if np.isnan(newPredictedPrice):
                newPredictedPrice = row["Predicted"]
            
            newRow = {
                "Date": index,
                "Open": lastClose,
                "High": [None],
                "Low": [None],
                "Close": newPredictedPrice,
                "Adj Close": newPredictedPrice,
                "Volume": [None],
                "Real": [False]
            }

            newRowDataFrame = pd.DataFrame(newRow)
            newRowDataFrame = newRowDataFrame.set_index("Date")
        
            symbolData = pd.concat([symbolData, newRowDataFrame])

        symbolData = symbolData.replace(np.nan,None)
        new_data = {}

        for index, row in symbolData.iterrows():
            row_dict = row.to_dict()
            new_data[index.strftime('%Y-%m-%d')] = row_dict
        

        saveDataToFile("data_"+symbol+".json", new_data)    
        
        makePrediction(symbol)
    
   

def makeDailyTask():
    if check_internet_connection():
        internetTask()
    else:
        noInternetTask()


def run_schedule():
    schedule.every().day.at("10:00").do(makeDailyTask)

    while True:
        schedule.run_pending()

def initScheduler():
    threading.Thread(target=run_schedule).start()
