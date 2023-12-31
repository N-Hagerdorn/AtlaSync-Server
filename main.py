from flask import Flask, request
from database import Database as db
from db_model import *
from qrCodeGenerator import QRCodeGenerator as qrcg
import netifaces as ni
import csv
from flask import send_file
import base64

app = Flask(__name__)
ip_address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']


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


def make_qr_codes():
    rooms = db.getAllRooms()
    for room_ in rooms:
        qrcg.makeRoomQRCode(room_.uid)

    return 'QR codes created...'


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


@app.route('/floor_map', methods=['GET'])
def floor_map():
    # Get room
    room_id = request.args.get('id')
    print(f'User {request.remote_addr} requests Room {room_id}')

    room = db.getRoomByID(room_id)
    floor = db.getFloorByID(room.owner_id)
    building = db.getBuildingByID(floor.owner_id)
    filename = f'./AtlaSync-Server/floormaps/{building.uid}-{floor.name}.png'

    converted_string = 'Undefined'

    with open(filename, 'rb') as image2string:
        converted_string = base64.b64encode(image2string.read())

    return converted_string


@app.route('/room_info', methods=['GET'])
def room_info():
    # Get room
    room_id = request.args.get('id')
    print(f'User {request.remote_addr} requests Room {room_id}')
    result = db.getLocation(room_id)

    return result


db.connect('atlas','atlas')
app.run(host=ip_address, port=5000, debug=True, threaded=False)
