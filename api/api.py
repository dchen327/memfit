from flask import Flask, request, jsonify
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
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred, {'projectId': 'mem-fit'})

db = firestore.client()
sleep_ref = db.collection('sleep')


@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')


@app.route('/api/logSleep', methods=['POST'])
@cross_origin()
def log_sleep():
    ''' Log sleep time to firestore db '''
    sleep_ref.add({'datetime': datetime.datetime.now()})
    return jsonify(success=True)


@app.route('/api/charts', methods=['GET', 'POST'])
@cross_origin()
def charts():
    ''' Return requested generated charts '''
    params = request.get_json()
    chart_names = params.get('charts')

    return get_requested_charts(chart_names)


def get_requested_charts(chart_names):
    ''' Generate and return the requested charts '''
    charts = {}
    for chart_name in chart_names:
        if chart_name == 'Sleep':
            charts[chart_name] = get_sleep_chart()

    return charts


def get_sleep_chart():
    ''' Plot sleep data in a line chart, return Plotly json '''
    sleep_data = get_sleep_data()
    hours_dict = {'Date': [], 'Hours': []}
    for i in range(len(sleep_data) - 1):
        if sleep_data[i][1] == 'sleep' and sleep_data[i+1][1] == 'wake':
            sleep_date = sleep_data[i+1][0].date()
            sleep_time, wake_time = sleep_data[i][0], sleep_data[i+1][0]
            sleep_hours = wake_time - sleep_time
            hours_dict['Date'].append(sleep_date)
            hours_dict['Hours'].append(round(sleep_hours.seconds / 3600, 2))
    sleep_df = pd.DataFrame(hours_dict)
    fig = px.line(sleep_df, x='Date', y='Hours',
                  markers=True)
    fig.update_traces(line=dict(width=3), marker=dict(size=10))

    return fig.to_json()


def get_sleep_data():
    ''' Get sleep data from Firestore, sort and organize by sleep/wake '''
    sort_date_query = sleep_ref.order_by('datetime')
    sleep_docs = sort_date_query.stream()
    sleep_data = []
    # loop through sorted list of datetimes, label as sleep or wake
    for sleep_doc in sleep_docs:
        sleep_date = sleep_doc.get('datetime')
        # assume wake up is between 4AM and 4PM
        if datetime.time(4, 0) < sleep_date.time() < datetime.time(16, 0):
            sleep_data.append((sleep_date, 'wake'))
        else:
            sleep_data.append((sleep_date, 'sleep'))

    # list of tuples (datetime, 'sleep' OR 'wake')
    return sleep_data
