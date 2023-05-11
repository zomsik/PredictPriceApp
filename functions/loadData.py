import yfinance as yf

def loadData(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data
