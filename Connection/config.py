import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def init():
    cred = credentials.Certificate("Connection\cribbage-a0a16-firebase-adminsdk-ncvs7-7944f69046.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://cribbage-a0a16-default-rtdb.firebaseio.com'
    })

    ref = db.reference("game")

    return ref