from functions.initScheduler import initScheduler
from server.initServer import server
import datetime

#end_date = datetime.date.today()
#start_date = end_date - datetime.timedelta(days=90)
#symbol = "CL=F" 
#data = loadData(symbol, start_date, end_date)
initScheduler()

server.run(host='localhost', port=8000, debug=True) 