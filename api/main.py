from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO,emit
import time
import json
from random import randint

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

items = [
    {
        'id': '1',
        'description': 'Item 01',
        'status': 'Not started'
    },
    {
        'id': '2',
        'description': 'Item 02',
        'status': 'Not started'
    },
    {
        'id': '3',
        'description': 'Item 03',
        'status': 'Not started'
    },
    {
        'id': '4',
        'description': 'Item 03',
        'status': 'Not started'
    }
]

status = ['Pass', 'Fail']

def random_status(data):
    time.sleep(2)
    indice = randint(0, 1)
    for item in items:
        if item['id'] == data['id']:
            item['status'] = status[indice]
            break
    emit('items', items, broadcast=True)

@socketio.on('connect')
def connect():
    emit('items', items, broadcast=True)

@socketio.on('edit_item')
def edit_item(data):
    for item in items:
        if item['id'] == data['id']:
            item['status'] = 'Running'
            break
    emit('items', items, broadcast=True)
    random_status(data)


if __name__ == '__main__':
    socketio.run(app, '127.0.0.1', 3001)