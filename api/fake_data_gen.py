'''
Generate fake data and store in Firestore
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import random
from faker import Faker
from pathlib import Path
from dotenv import load_dotenv
import os
import datetime

import plotly.express as px
import pandas as pd


fake = Faker()

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

db = firebase_admin.firestore.client()

sleep_ref = db.collection('sleep')


def delete_collection(col_ref):
    ''' Delete all data in sleep collection '''
    docs = col_ref.stream()
    for doc in docs:
        doc.reference.delete()


def add_sleep(num_days):
    ''' Add randomized sleep times '''
    delete_collection(sleep_ref)

    today_date = datetime.date.today()
    for day_num in range(1, num_days):
        day = today_date - datetime.timedelta(days=day_num)
        # sleep between 10PM and 2AM
        earliest_sleep = datetime.datetime.combine(
            day, datetime.time(22, 0))
        latest_sleep = datetime.datetime.combine(
            day + datetime.timedelta(days=1), datetime.time(2, 0))
        sleep_time = fake.date_time_between(
            start_date=earliest_sleep, end_date=latest_sleep).astimezone()

        # sleep between 5-10 hours
        wake_time = sleep_time + \
            datetime.timedelta(minutes=random.randint(5 * 60, 10 * 60))

        sleep_ref.add({'datetime': sleep_time, 'type': 'sleep'})
        sleep_ref.add({'datetime': wake_time, 'type': 'wake'})


def plot_sleep():
    ''' Plot sleep data in a line chart of length of sleep '''
    sleep_data = get_sleep_data()
    hours_dict = {'Date': [], 'Hours': []}
    for i in range(len(sleep_data) - 1):
        if sleep_data[i][1] == 'sleep' and sleep_data[i+1][1] == 'wake':
            # date is wake date minus 1 day
            sleep_date = sleep_data[i+1][0].date() - datetime.timedelta(days=1)
            sleep_time, wake_time = sleep_data[i][0], sleep_data[i+1][0]
            print(sleep_time, wake_time)
            sleep_hours = wake_time - sleep_time
            hours_dict['Date'].append(sleep_date)
            hours_dict['Hours'].append(round(sleep_hours.seconds / 3600, 2))
    sleep_df = pd.DataFrame(hours_dict)
    fig = px.line(sleep_df, x='Date', y='Hours',
                  markers=True)
    fig.update_traces(line=dict(width=3), marker=dict(size=10))

    fig.show()

# def plot_sleep():
#     ''' Plot sleep data in a line chart of length of sleep '''
#     sleep_data = get_sleep_data()
#     hours_dict = {'Date': [], 'Hours': []}
#     for sleep_date in sleep_data:
#         try:
#             next_day = sleep_date + timedelta(days=1)
#             sleep_time = sleep_data[sleep_date]['sleep']
#             wake_time = sleep_data[next_day]['wake']
#             sleep_hours = wake_time - sleep_time
#             hours_dict['Date'].append(sleep_date)
#             hours_dict['Hours'].append(round(sleep_hours.seconds / 3600, 2))
#         except KeyError:  # missing data, or it's the current day
#             pass

#     sleep_df = pd.DataFrame(hours_dict)
#     fig = px.line(sleep_df, x='Date', y='Hours', markers=True)
#     fig.update_traces(line=dict(width=3), marker=dict(size=10))

#     # add horizontal line at average sleep
#     avg_sleep = sleep_df['Hours'].mean()
#     fig.add_hline(y=avg_sleep, line_color='green',
#                   line_dash='dash', annotation_text=f'Average: {round(avg_sleep, 2)}', annotation_position='top left')

#     fig.show()


def get_sleep_data():
    ''' Get sleep data from Firestore, sort and organize by sleep/wake '''
    sort_date_query = sleep_ref.order_by('datetime')
    sleep_docs = sort_date_query.stream()
    # list of tuples of (datetime, sleep/wake)
    return [
        (sleep_doc.get('datetime').astimezone(), sleep_doc.get('type'))
        for sleep_doc in sleep_docs
    ]


# plot_sleep()
add_sleep(50)
