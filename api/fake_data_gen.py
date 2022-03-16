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
        day = today_date - timedelta(days=day)
        # sleep between 10pm and 2am
        earliest_sleep = datetime.combine(day, time(22, 0))
        latest_sleep = datetime.combine(
            day + timedelta(day=1), time(2, 0))
        sleep_time = fake.date_time_between(
            earliest=earliest_sleep, latest=latest_sleep)
        # sleep between 6-10 hours
        wake_time = sleep_time + \
            timedelta(minutes=random.randint(6 * 60, 10 * 60))
        sleep_ref.add({'datetime': sleep_time})
        sleep_ref.add({'datetime': wake_time})


add_sleep()
