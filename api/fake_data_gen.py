'''
Generate fake data and store in Firestore
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import random
from faker import Faker
from pathlib import Path

from datetime import date, time, datetime, timedelta


fake = Faker()

cred_path = Path('./api/firebase_key.json')
# list files in directory
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {'projectId': 'mem-fit'})

db = firebase_admin.firestore.client()

sleep_ref = db.collection('sleep')


def add_sleep():
    ''' Add randomized sleep times '''
    today_date = date.today()
    for day_num in range(10):
        day = today_date - timedelta(days=day_num)
        # sleep between 10PM and 2AM
        earliest_sleep = datetime.combine(day, time(22, 0))
        latest_sleep = datetime.combine(
            day + timedelta(days=1), time(2, 0))
        sleep_time = fake.date_time_between(
            start_date=earliest_sleep, end_date=latest_sleep)
        # sleep between 5-10 hours
        wake_time = sleep_time + \
            timedelta(minutes=random.randint(5 * 60, 10 * 60))
        sleep_ref.add({'datetime': sleep_time})
        sleep_ref.add({'datetime': wake_time})


def plot_sleep():
    ''' Pull sleep data from Firestore, and plot'''
    sort_date_query = sleep_ref.order_by('datetime')
    sleep_docs = sort_date_query.stream()
    sleep_data = []
    # loop through sorted list of datetimes, label as sleep or wake
    for sleep_doc in sleep_docs:
        sleep_date = sleep_doc.get('datetime')
        # assume wake up is between 4AM and 4PM
        if time(4, 0) < sleep_date.time() < time(16, 0):
            sleep_data.append((sleep_date, 'wake'))
        else:
            sleep_data.append((sleep_date, 'sleep'))
    print([i[1] for i in sleep_data])


plot_sleep()
