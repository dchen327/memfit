from flask import Flask, request
from flask_cors import CORS, cross_origin
import plotly.express as px

import pandas as pd
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Flask setup
app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

# Firebase setup
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'mem-fit',
})

db = firestore.client()
sleep_col = db.collection('sleep')


@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')


@app.route('/api/logSleep')
@cross_origin()
def log_sleep():
    ''' Log sleep time to firestore db '''
    sleep_col.add({'datetime': datetime.datetime.now()})
