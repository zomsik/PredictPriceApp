import datetime
from functions.downloadData import downloadData
from functions.fileManipulation import check_data_existence, append_symbol_to_json
from functions.initScheduler import check_internet_connection

def downloadNewSymbolData(symbol):
    today_date = datetime.date.today()  
    start_date = today_date - datetime.timedelta(days=90)

    if check_internet_connection():
        if not check_data_existence("symbols.json", symbol):
            threeMonthData = downloadData(symbol,start_date,today_date)
            if not threeMonthData.empty:
                #append_data_to_json("data_"+symbol+".json", threeMonthData)
                append_symbol_to_json('symbols.json',symbol)
                #predyktowanie
                return "Pobrano nowy symbol"
            else:
                return "Brak danych dla symbolu - możliwe, że nie istnieje"
        else:
            return "symbol już został dodany"
    else:
        return "Brak internetu"
