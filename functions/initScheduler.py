import schedule
import time
import threading
import datetime
import socket
from functions.fileManipulation import getSymbolList
from functions.downloadData import downloadData

def check_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def makeDailyTask():
    today_date = datetime.date.today()  
    if check_internet_connection():
        for symbol in getSymbolList("symbols.json"):
            todayData = downloadData(symbol,today_date,today_date)
            print(todayData)
            #dodać do danych dzisiejszy dzień i predyktować tydzień

    else:
        print("Brak internetu")
        #do data dodać ten dzień z predykcji i od nowa predyktować tydzień

def run_schedule():
    #schedule.every(20).seconds.do(makeDailyTask)  
    
    while True:
        schedule.run_pending()

def initScheduler():
    threading.Thread(target=run_schedule).start()
