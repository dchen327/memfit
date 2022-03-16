'''
Generate fake data and store in Firestore
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from faker import Faker
from pathlib import Path


fake = Faker()

cred_path = Path('./firebase_key.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {'projectId': 'mem-fit'})

db = firebase_admin.firestore.client()

sleep_ref = db.collection('sleep')
