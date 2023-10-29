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
@app.route('/load_rooms')
def load_rooms():

    with open('Room_data.csv', mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file

        for record in csvFile:
            name, building_name, story, _, _, _, x_loc, y_loc = record
            if name == 'Room' or name == '' or building_name == 'Building':
                continue
            print(f'Trying to find {building_name} in table Building...')
            building = db.getBuildingByName(building_name)
            print(f'Found {building.name}')
            floor = db.getFloor(building.uid, story)
            room = Room(-1, name, floor.uid, (x_loc, y_loc))
            db.addRoom(room)

    db.commit()
    return 'Load successful...'

@app.route('/load_buildings')
def load_buildings():

    with open('Building_data.csv', mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file

        for record in csvFile:
            name, building_name, story, _, _, _, x_loc, y_loc = record
            if name == 'Room' or name == '':
                continue
            print(f'Trying to find {building_name} in table Building...')
            building = db.getBuildingByName(building_name)
            print(f'Found {building.name}')
            floor = db.getFloor(building.uid, story)
            room = Room(-1, name, floor.uid, (x_loc, y_loc))
            db.addRoom(room)

    db.commit()
    return 'Load successful...'


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
