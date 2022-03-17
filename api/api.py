from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
import os

import plotly.express as px
import pandas as pd
import datetime


# Flask setup
app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

# Firebase setup
load_dotenv()
# replace \\n with \n since heroku config vars adds a \
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "mem-fit",
    "private_key_id": os.getenv("PY_FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("PY_FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": "firebase-adminsdk-m1254@mem-fit.iam.gserviceaccount.com",
    "client_id": "103893414132813680155",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-m1254%40mem-fit.iam.gserviceaccount.com"
}
cred = credentials.Certificate(FIREBASE_CONFIG)
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
    params = request.get_json()
    # convert ms to s, grab current local time (client time)
    local_datetime = datetime.datetime.fromtimestamp(
        params.get('currTime') / 1000.0)
    sleep_type = 'wake' if datetime.time(
        4, 0) < local_datetime.time() < datetime.time(16, 0) else 'sleep'
    # Add UTC time, and sleep type
    # sleep_ref.add({
    #     'datetime': datetime.datetime.now(),
    #     'type': sleep_type
    # })
    print({
        'datetime': datetime.datetime.now(),
        'type': sleep_type
    })

    return jsonify(success=True)


@app.route('/api/charts', methods=['GET', 'POST'])
@cross_origin()
def get_charts():
    ''' Return requested generated charts '''
    params = request.get_json()
    chart_names = params.get('charts')

    return get_requested_charts(chart_names)


@app.route('/api/chartsFromFirebase', methods=['GET', 'POST'])
@cross_origin()
def charts_from_firebase():
    ''' Return requested chart json strings from Firestore '''
    charts = {}
    params = request.get_json()
    chart_names = params.get('charts')

    # charts collection has one document for each chart (doc name is the chart)
    # each chart document has just one field: chart_json
    charts_ref = db.collection('charts')
    for chart_name in chart_names:
        print(charts_ref.document(chart_name).get().to_dict())
        chart_json = charts_ref.document(chart_name).get().get('chartJSON')
        charts[chart_name] = chart_json

    return charts


def get_requested_charts(chart_names):
    ''' Generate and return the requested charts '''
    charts = {}
    for chart_name in chart_names:
        if chart_name == 'sleep':
            # charts[chart_name] = get_sleep_chart()
            # debug, return simple scatter plot json
            charts[chart_name] = px.scatter(
                x=[1, 2, 3, 4], y=[2, 3, 1, 4]).to_json()

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
    fig = px.line(sleep_df, x='Date', y='Hours', markers=True)
    fig.update_traces(line=dict(width=3), marker=dict(size=10))

    # add horizontal line at average sleep
    avg_sleep = sleep_df['Hours'].mean()
    fig.add_hline(y=avg_sleep, line_color='green',
                  line_dash='dash', annotation_text=f'Average: {round(avg_sleep, 2)}', annotation_position='top left')

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
