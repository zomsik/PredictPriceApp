import json
import os
import yfinance as yf

path = 'data/'

def append_data_to_json(filename,data):
    filename = path+filename
    #filename = 'data_'+symbol+'.json'
    if not os.path.isfile(filename):
        # Jeśli plik nie istnieje, utwórz nowy pusty plik JSON
        with open(filename, 'w') as file:
            json.dump([], file)

    with open(filename, 'r+') as file:
        file_data = json.load(file)


        file_data.append( data.to_dict())
        file.seek(0)

        json.dump(file_data, file, indent=4)
        file.truncate()


def load_symbols_list(filename):
    filename = path+filename
    with open(filename, 'r') as file:
        symbols_data = json.load(file)

    symbols_list = symbols_data  # Założenie: plik JSON zawiera listę bezpośrednio

    return symbols_list

def check_data_existence(filename, symbol):
    filename = path+filename
    with open(filename, 'r') as file:
        symbols_data = json.load(file)

    if symbol in symbols_data:
        return True
    else:
        return False