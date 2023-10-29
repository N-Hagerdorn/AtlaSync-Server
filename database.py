import mariadb
import sys
from db_model import *


class Database:

    cur = None
    conn = None

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

        cls.conn = conn
        cls.cur = conn.cursor()

    @classmethod
    def commit(cls):
        cls.conn.commit()

    @classmethod
    def addRoom(cls, room):

        '''
        # First check if there is already a room with the given name
        query = 'SELECT name FROM Room WHERE name = ?'
        data = (room.name,)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is not None:
            return False
        '''
        query = 'INSERT INTO Room (name, floor_id, x_loc, y_loc) VALUES (?, ?, ?, ?)'
        data = (room.name, room.owner_id, room.location[0], room.location[1])
        cls.cur.execute(query, data)

        ''' May not choose to implement this, idk
        query = 'SELECT id FROM Floor WHERE id = ?'
        data = (room.owner_id,)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is None:
            addFloor()
        '''

        return True

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
    def getBuildingByName(cls, name):
        query = 'SELECT * FROM Building WHERE name = ?'
        data = (name,)
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
    def getFloor(cls, building_id, story):
        query = 'SELECT * FROM Floor WHERE building_id = ? AND story = ?'
        data = (building_id, story)
        cls.cur.execute(query, data)
        record = cls.cur.fetchone()
        if record is None:
            return None
        floor_id, story, building_id = record
        return Floor(floor_id, story, building_id)

    @classmethod
    def getRoomByID(cls, room_id):
        query = 'SELECT * FROM Room WHERE id = ?'
        data = (room_id,)
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

        return f'Room {room.name} is located on floor {floor.name} of the {building.name} at {organization.name}'
