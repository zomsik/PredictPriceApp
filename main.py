from data.loadData import loadData
from server.initServer import server
import datetime

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=90)
symbol = "CL=F" 



def main():
    data = loadData(symbol, start_date, end_date)
    server.run(host='localhost', port=8000, debug=True)

    

     
if __name__ == '__main__':
     main()     