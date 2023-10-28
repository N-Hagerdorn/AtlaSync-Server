from flask import Flask, request
from database import Database as db
from qrCodeGenerator import QRCodeGenerator as qrcg
import netifaces as ni

app = Flask(__name__)

ip_address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/room', methods=['GET'])
def room():
    # Get room
    room_id = request.args.get('room')
    print(f'User {request.remote_addr} requests Room {room_id}')
    # Get floor from room.floor_id
    # Get floor map
    # Get building
    # Get organization
    return room_id


@app.route('/floor')
def floor():
    return None

db.connect('atlas','atlas')
app.run(host=ip_address, port=5000, debug=True, threaded=False)
