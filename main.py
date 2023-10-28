from flask import Flask, request
from database import Database as db

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/room', methods=['GET'])
def room():
    # Get room
    room_id = request.args.get('room')
    print(room_id)
    # Get floor from room.floor_id
    # Get floor map
    # Get building
    # Get organization
    return room_id


@app.route('/floor')
def floor():
    return None

db.connect('atlas','atlas')
app.run(host='192.168.0.5', port=5000, debug=True, threaded=False)
