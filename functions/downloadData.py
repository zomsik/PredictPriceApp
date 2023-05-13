import yfinance as yf

def downloadData(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data
