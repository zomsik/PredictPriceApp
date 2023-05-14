from flask import Flask, jsonify, redirect, render_template, request
from functions.createNewSymbol import downloadNewSymbolData
import os
from functions.fileManipulation import getSymbolList, loadData
import plotly.graph_objs as go

server = Flask(__name__, template_folder='../templates', static_folder='../static')


@server.route('/')
def index():
    komunikat = request.args.get('komunikat')
    symbolsPredicted = getSymbolList("symbolsPredicted.json")

    return render_template('index.html', symbols=symbolsPredicted, komunikat=komunikat)



@server.route('/add_symbol', methods=['POST'])
def add_symbol():
    symbol = request.form['addSymbol']

    response = downloadNewSymbolData(symbol)
    return redirect('/?komunikat='+response)

'''@server.route('/generate_plot')
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
    return plot_filename'''

@server.route('/update-data')
def update_data():
    symbol = request.args.get('symbol')

    data = loadData(symbol+"plotData.json")
    
    layout = go.Layout(
        title='Przykładowy wykres Plotly',
        xaxis=dict(title='Oś X'),
        yaxis=dict(title='Oś Y')
    )
    
    response = {'data': data, 'layout': layout}
    return jsonify(response)
