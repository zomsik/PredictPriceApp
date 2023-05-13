import json
import os

folder = 'data/'

def checkIfFileExists(filename): 
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump([], file)


def append_symbol_to_json(filename,symbol):
    checkIfFileExists(filename)
    path = os.path.join(folder, filename)
    #filename = 'data_'+symbol+'.json'
    with open(path, 'r+') as file:
        file_data = json.load(file)
        file_data.append(symbol)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate()


def load_symbols_list(filename):
    checkIfFileExists(filename)
    path = os.path.join(folder, filename)
    with open(path, 'r') as file:
        symbols_data = json.load(file)

    symbols_list = symbols_data

    return symbols_list

def check_data_existence(filename, symbol):
    checkIfFileExists(filename)
    path = os.path.join(folder, filename)
    with open(path, 'r') as file:
        symbols_data = json.load(file)

    if symbol in symbols_data:
        return True
    else:
        return False