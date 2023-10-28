import mariadb
import sys




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
    def getLocation(cls, room_id):
        if cls.cur is None:
            return None
        print('step 1')
        statement = 'SELECT * FROM Room WHERE id = ?'
        print('step 2')
        data = (room_id,)
        print('step 3')
        cls.cur.execute(statement, data)
        print('step 4')
        row = cls.cur.fetchone()
        print('step 5')
        records = []
        print('step 6')
        while row is not None:
            print('step 7')
            records.append(f'Successfully retrieved location x={row[3]}, {row[4]} for room {row[1]}')
        print('step 8')
        return records
