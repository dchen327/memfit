from flask import Flask, request
from flask_cors import CORS, cross_origin
import plotly.express as px

import pandas as pd
import datetime

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)


@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')


@app.route('/api/logSleep', methods=['GET', 'POST'])
@cross_origin()
def log_sleep():
    ''' Log sleep time to firestore db '''
    pass
