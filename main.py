from flask import Flask, request
from database import Database as db
from db_model import *
from qrCodeGenerator import QRCodeGenerator as qrcg
import netifaces as ni
import csv

app = Flask(__name__)

with open('Room_data.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file

    for line in csvFile:
        print(line)

ip_address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

# Import XLSX data
@app.route('/load')
def load():

    with open('Room_data.csv', mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file

        for record in csvFile:
            name, building_name, story, _, _, _, x_loc, y_loc = record
            if name == 'Room' or name == '':
                continue
            building = db.getBuilding('name', building_name)
            floor = db.getFloor(building.uid, story)
            room = Room(-1, name, floor.uid, x_loc, y_loc)
            db.addRoom(room)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/room', methods=['GET'])
def room():
    # Get room
    room_id = request.args.get('id')
    print(f'User {request.remote_addr} requests Room {room_id}')
    result = db.getLocation(room_id)
    # Get floor from room.floor_id
    # Get floor map
    # Get building
    # Get organization
    return str(result)


@app.route('/floor')
def floor():
    return None


db.connect('atlas','atlas')
app.run(host=ip_address, port=5000, debug=True, threaded=False)
