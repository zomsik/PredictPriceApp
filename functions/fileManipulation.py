import json
import os

folder = 'data/'

# Data files

def checkIfFileDataExists(filename): 
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        return True
    return False

def loadData(filename):
    if checkIfFileDataExists(filename):
        path = os.path.join(folder, filename)
        jsonData = {}
        with open(path, 'r') as file:
            jsonData = json.load(file)
        return jsonData
    pass

def checkIfDateAlreadyInFile(filename, date):
    jsonData = loadData(filename)

    if date in jsonData:
        return True
    else:
        return False

def saveDataToFile(filename, data): 
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4, allow_nan=False)

def appendData(filename, data):
    if checkIfFileDataExists(filename):
        path = os.path.join(folder, filename)
        with open(path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            #file.seek(0)
            json.dump(file_data, file, indent=4)
            #file.truncate()


#Symbol files

def checkIfFileSymbolsExists(filename): 
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump([], file)

def appendSymbol(filename,symbol):
    checkIfFileSymbolsExists(filename)
    path = os.path.join(folder, filename)
    if not checkIfSymbolInFile(filename, symbol):
        with open(path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(symbol)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            file.truncate()

def getSymbolList(filename):
    checkIfFileSymbolsExists(filename)
    path = os.path.join(folder, filename)
    symbols_data = {}
    with open(path, 'r') as file:
        symbols_data = json.load(file)

    return symbols_data

def checkIfSymbolInFile(filename, symbol):
    symbols_data = getSymbolList(filename)

    if symbol in symbols_data:
        return True
    else:
        return False