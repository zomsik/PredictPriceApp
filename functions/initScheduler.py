import schedule
import time
import threading
from datetime import datetime


def function_A():
    now = datetime.now()
    czas = now.strftime("%d/%m/%Y %H:%M:%S")
    print(czas)
    print("Wywołanie funkcji A")

def run_schedule():
    schedule.every(20).seconds.do(function_A)  
    
    while True:
        schedule.run_pending()

def initScheduler():
    threading.Thread(target=run_schedule).start()
