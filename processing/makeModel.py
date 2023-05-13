import os
import json
import pandas as pd

def loadData(filename):
    jsonData = {}
    with open(filename, 'r') as file:
        jsonData = json.load(file)
    return jsonData

def prepareData(dataJson):
    selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data = pd.DataFrame.from_dict(dataJson, orient='index')
    data = data[selected_columns]
    data = data.dropna()
    return data

data = loadData("processing/data_MSFT.json")
data = prepareData(data)

print(data)

