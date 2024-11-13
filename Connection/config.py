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

"""def init():
    try:
        # Check if an app with the name "my_app" is already initialized
        app = firebase_admin.get_app("my_app")
    except ValueError:
        # If not, initialize it
        cred = credentials.Certificate("Connection\cribbage-a0a16-firebase-adminsdk-ncvs7-7944f69046.json")
        app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cribbage-a0a16-default-rtdb.firebaseio.com'
        }, name="my_app")
    
    # Get a reference to the "game" node in the database
    ref = db.reference("game", app=app)
    
    return ref"""
