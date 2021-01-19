from pprint import PrettyPrinter

import firebase_admin
from firebase_admin import credentials, firestore


credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()
print = PrettyPrinter(indent=4).pprint

def get_user(user_id):
    return db.collection('users').document(user_id).get()


def get_users():
    return db.collection('users').get()


def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()


def create_todo(user_id, description):
    todo_collection_ref = db.collection('users').document(user_id).collection('todos')
    todo_collection_ref.document().set({'description': description, 'done': False})


def delete_todo(user_id, todo_id):
    _get_todo_ref(user_id, todo_id).delete()


def edit_todo(user_id, todo_id, done):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': not done})


def _get_todo_ref(user_id, todo_id):
    return db.collection('users').document(user_id).collection('todos').document(todo_id)
