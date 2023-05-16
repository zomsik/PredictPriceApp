from flask import Flask, redirect, render_template, request, url_for
from functions.createNewSymbol import downloadNewSymbolData
from functions.fileManipulation import getSymbolList


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


@server.route('/getPlotData')
def update_data():
    symbol = request.args.get('symbol')
    #return redirect(url_for('index'))
    return render_template(symbol+'.html')
    #return render_template(url_for('static', filename='plots/' + symbol + '.html'))
