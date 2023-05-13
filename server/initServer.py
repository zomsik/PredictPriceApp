from flask import Flask, redirect, render_template, request
import matplotlib

from functions.createNewSymbol import downloadNewSymbolData
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from functions.fileManipulation import load_symbols_list

server = Flask(__name__, template_folder='../templates', static_folder='../static')


@server.route('/')
def index():
    komunikat = request.args.get('komunikat')

    report_data = {
        'title': 'Raport predykcji cen akcji',
        'content': 'Przykładowa zawartość raportu'
    }
    
    return render_template('index.html', data=report_data, symbols=load_symbols_list())



@server.route('/add_symbol', methods=['POST'])
def add_symbol():
    symbol = request.form['symbol']

    response = downloadNewSymbolData(symbol)
    return redirect('/?komunikat='+response)

@server.route('/generate_plot')
def generate_plot():
    symbol = request.args.get('symbol')

    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Wykres dla symbolu {symbol}')
    plt.grid(True)

    # Zapisz wykres do pliku PNG
    plot_filename = f'plot_{symbol}.png'
    plt.savefig(os.path.join('static','plots',plot_filename))

    # Zwolnij zasoby wykorzystywane przez matplotlib
    plt.clf()

    # Zwróć nazwę wygenerowanego pliku obrazu
    return plot_filename