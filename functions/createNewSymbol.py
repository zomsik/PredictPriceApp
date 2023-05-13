import datetime
from functions.downloadData import downloadData
from fileManipulation import check_data_existence, append_data_to_json
from functions.initScheduler import check_internet_connection

def downloadNewSymbolData(symbol):
    today_date = datetime.date.today()  
    start_date = today_date - datetime.timedelta(days=90)

    if check_internet_connection():
        if not check_data_existence():
            threeMonthData = downloadData(symbol,start_date,today_date)
            if not threeMonthData.empty:
                append_data_to_json("data_"+symbol+".json", threeMonthData)
                #predyktowanie
            else:
                return "Brak danych dla symbolu - możliwe, że nie istnieje"
        else:
            return "symbol już został dodany"
    else:
        return "Brak internetu"
