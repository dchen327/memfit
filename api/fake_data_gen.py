'''
Generate fake data and store in Firestore
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
    for day in range(10):
        # sleep between 10pm and 2am
        earliest_sleep = datetime.combine(today_date, time(22, 0))
        latest_sleep = datetime.combine(today_date, time(2, 0))


add_sleep()
