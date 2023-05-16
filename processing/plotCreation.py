import plotly.graph_objs as go
from functions.fileManipulation import loadData
from datetime import datetime
import plotly.offline as py
import pandas as pd

def createPlot(symbol):
    now = datetime.now()
    dateNow = now.strftime("%d/%m/%Y %H:%M:%S")
    
    data = loadData(symbol+"_plotData.json")
    data = pd.DataFrame.from_dict(data, orient='index')
    data['Date'] = data.index
    
    layout = go.Layout(
        title='Wykres z '+ dateNow +' dla cen akcji '+symbol,
        xaxis=dict(title='Dzień'),
        yaxis=dict(title='Cena zamknięcia')
    )
    
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Actual'], name='Actual'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Future'], name='Future'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Predicted'], name='Predicted'))
        

    py.plot(fig, filename='templates/' + symbol + '.html')