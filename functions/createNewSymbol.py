import datetime
from threading import Thread
from functions.downloadData import downloadData
from functions.fileManipulation import saveDataToFile, checkIfSymbolInFile, appendSymbol
from server.initScheduler import check_internet_connection
from processing.predict import makePrediction

def downloadNewSymbolData(symbol):
    today_date = datetime.date.today()  
    start_date = today_date - datetime.timedelta(days=90)
    symbol = symbol.upper()
    if check_internet_connection():
        if not checkIfSymbolInFile("symbols.json", symbol):
            newDownloadedData = downloadData(symbol,start_date,today_date)
            if not newDownloadedData.empty:
                thread = Thread(target=workWithNewData, args=(newDownloadedData, symbol))
                thread.start()

                return "Pobrano nowy symbol. Będzie on dostępny do wybrania po predykcji", "success"
            else:
                return "Brak danych dla symbolu - możliwe, że nie istnieje", "error"
        else:
            return "Symbol już został dodany", "info"
    else:
        return "Brak internetu", "error"

def workWithNewData(newDownloadedData, symbol):
    
    new_data = {}
    newDownloadedData['Real'] = True

    for index, row in newDownloadedData.iterrows():
        row_dict = row.to_dict()
        new_data[index.strftime('%Y-%m-%d')] = row_dict
                
    saveDataToFile("data_"+symbol+".json", new_data)
    appendSymbol('symbols.json',symbol)
    
    makePrediction(symbol)