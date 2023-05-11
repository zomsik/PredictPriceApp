from flask import Flask, render_template
import os

server = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@server.route('/')
def index():
    report_data = {
        'title': 'Raport predykcji cen akcji',
        'content': 'Przykładowa zawartość raportu'
    }
    return render_template('index.html', data=report_data)