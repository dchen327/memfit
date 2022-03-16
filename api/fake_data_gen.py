'''
Generate fake data and store in Firestore
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from faker import Faker
from pathlib import Path

import datetime


fake = Faker()

cred_path = Path('./api/firebase_key.json')
# list files in directory
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {'projectId': 'mem-fit'})

db = firebase_admin.firestore.client()

sleep_ref = db.collection('sleep')


def add_sleep():
    ''' Add randomized sleep times '''
    today_date = datetime.date.today()
    print(today_date)
    # for day in range(10):


add_sleep()
