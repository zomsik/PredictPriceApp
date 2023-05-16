import schedule
import time
import threading
from datetime import datetime, timedelta
import socket
from functions.fileManipulation import getSymbolList, loadData, saveDataToFile
from functions.downloadData import downloadData
import pandas as pd
from processing.predict import makePrediction

def check_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def makeDailyTask():
    today_date = datetime.date.today()  
    if not check_internet_connection():
        for symbol in getSymbolList("symbolsPredicted.json"):
            
            symbolData = loadData("data"+symbol+".json")
            todayData = downloadData(symbol,today_date,today_date)
            print(todayData)
            #dodać do danych dzisiejszy dzień i predyktować tydzień

    else:
        for symbol in getSymbolList("symbolsPredicted.json"):
            symbolData = loadData("data_"+symbol+".json")
            symbolData = pd.DataFrame.from_dict(symbolData, orient='index')
            symbolData.index = pd.to_datetime(symbolData.index)
            
            predictedData = loadData(symbol+"_plotData.json")
            predictedData = pd.DataFrame.from_dict(predictedData, orient='index')
            predictedData.index = pd.to_datetime(predictedData.index)
            
            todayDate = datetime.now().date()

            lastActualDataEntry = symbolData.iloc[-1]
            PreviousRows = predictedData[predictedData.index >= lastActualDataEntry.name]

            rowsToDelete = []
            for index, row in PreviousRows.iterrows():
                if index in symbolData.index or index.weekday() >= 5 or index.date() >= todayDate:
                    rowsToDelete.append(index)

            PreviousRows = PreviousRows.drop(rowsToDelete)
            
            
            
            for index, row in PreviousRows.iterrows():
                symbolData = symbolData.iloc[1:]
                
                #tworzenie data_symbol z pozostałych i dodawanie do pliku
                print()
                
                
                
            new_data = {}

            for index, row in symbolData.iterrows():
                row_dict = row.to_dict()
                new_data[index.strftime('%Y-%m-%d')] = row_dict
                        
            saveDataToFile("data_"+symbol+".json", new_data)    
            
            makePrediction(symbol)
            #do data dodać ten dzień z predykcji i od nowa predyktować tydzień








def run_schedule():
    #schedule.every(20).seconds.do(makeDailyTask)  
    
    while True:
        schedule.run_pending()

def initScheduler():
    threading.Thread(target=run_schedule).start()
