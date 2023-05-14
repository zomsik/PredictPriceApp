import datetime
import threading
from functions.downloadData import downloadData
from functions.fileManipulation import saveDataToFile, checkIfSymbolInFile, appendSymbol
from functions.initScheduler import check_internet_connection
from processing.predict import makePrediction

def downloadNewSymbolData(symbol):
    today_date = datetime.date.today()  
    start_date = today_date - datetime.timedelta(days=30)

    if check_internet_connection():
        if not checkIfSymbolInFile("symbols.json", symbol):
            newDownloadedData = downloadData(symbol,start_date,today_date)
            if not newDownloadedData.empty:
                threading.Thread(target=workWithNewData(newDownloadedData, symbol)).start()
                return "Pobrano nowy symbol. Będzie on dostępny do wybrania po predykcji"
            else:
                return "Brak danych dla symbolu - możliwe, że nie istnieje"
        else:
            return "symbol już został dodany"
    else:
        return "Brak internetu"

def workWithNewData(newDownloadedData, symbol):
    
    new_data = {}
    newDownloadedData['Status'] = "Real"

    for index, row in newDownloadedData.iterrows():
        row_dict = row.to_dict()
        new_data[index.strftime('%Y-%m-%d')] = row_dict
                
    saveDataToFile("data_"+symbol+".json", new_data)
    appendSymbol('symbols.json',symbol)
    
    makePrediction(symbol)