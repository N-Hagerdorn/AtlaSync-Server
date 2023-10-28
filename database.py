import mariadb
import sys
import socket
import fcntl
import struct


class Database:

    cur = None

    @staticmethod
    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


    @classmethod
    def connect(cls, username, password):

        try:
            ip_address = Database.get_ip_address('wlan0')
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
    def getLocation(cls, room_id):
        if cls.cur is None:
            return None
        statement = 'SELECT * FROM Room WHERE id = ?'
        data = room_id
        cls.cur.execute(statement, data)
        row = cls.cur.fetchone()
        while row is not None:
            print(f'Successfully retrieved location x={row[3]}, {row[4]}')
        return 0
