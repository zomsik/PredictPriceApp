from flask import Flask, redirect, render_template, request, flash
from functions.createNewSymbol import downloadNewSymbolData
from functions.fileManipulation import getSymbolList, loadPlotFromFile


server = Flask(__name__, template_folder='../templates', static_folder='../static')

@server.route('/')
def index():
    komunikat = request.args.get('komunikat')
    status = request.args.get('status')
    symbolsPredicted = getSymbolList("symbolsPredicted.json")
    
    if status:
        flash(komunikat, status)
        return render_template('index.html', symbols=symbolsPredicted)
    else:
        return render_template('index.html', symbols=symbolsPredicted)   

@server.route('/add_symbol', methods=['POST'])
def add_symbol():
    symbol = request.form['addSymbol']

    response, status = downloadNewSymbolData(symbol)
    return redirect('/?komunikat=' + response + '&status=' + status)


@server.route('/getPlotData')
def get_plot():
    symbol = request.args.get('symbol')
    divPlot = loadPlotFromFile(symbol)

    return render_template('index.html', divPlot = divPlot)
    