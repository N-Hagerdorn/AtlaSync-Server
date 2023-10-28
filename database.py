import mariadb
import sys
from db_model import *


class Database:

    cur = None


    @classmethod
    def connect(cls, username, password):

        try:
            conn = mariadb.connect(
                user=username,
                password=password,
                host='127.0.0.1',
                port=3306,
                database='atlas'
            )
        except mariadb.Error as e:
            print(f'Error connecting to MariaDB platform: {e}')
            sys.exit(1)

        cls.cur = conn.cursor()

    @classmethod
    def addRoom(cls):
        return None

    @classmethod
    def addFloor(cls):
        return None

    @classmethod
    def addBuilding(cls):
        return None

    @classmethod
    def addOrganization(cls):
        return None

    @classmethod
    def getOrganizationByID(cls, organization_id):
        query = 'SELECT * FROM Organization WHERE id = ?'
        data = (organization_id,)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is None:
            return None
        organization_id, organization_name = record
        return Organization(organization_id, organization_name)

    @classmethod
    def getBuildingByID(cls, building_id):
        query = 'SELECT * FROM Building WHERE id = ?'
        data = (building_id,)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is None:
            return None
        building_id, building_name, org_id = record
        return Building(building_id, building_name, org_id)

    @classmethod
    def getFloorByID(cls, floor_id):
        query = 'SELECT * FROM Floor WHERE id = ?'
        data = (floor_id,)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is None:
            return None
        floor_id, story, building_id = record
        return Floor(floor_id, story, building_id)

    @classmethod
    def getRoomByID(cls, room_id):
        query = 'SELECT * FROM Room WHERE id = ?'
        print(query)
        data = (room_id,)
        print(data)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is None:
            return None
        room_id, room_name, floor_id, x_loc, y_loc = record
        return Room(room_id, room_name, floor_id, (x_loc, y_loc))

    @classmethod
    def getLocation(cls, room_id):
        if cls.cur is None:
            return None

        room = cls.getRoomByID(room_id)

        floor = cls.getFloorByID(room.owner_id)

        building = cls.getBuildingByID(floor.owner_id)

        organization = cls.getOrganizationByID(building.owner_id)

        return f'Room {room.name} is located on floor {floor.namet} of the {building.name} at {organization.name}'
