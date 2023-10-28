class Organization:

    def __init__(self, organization_id, name):
        self.name = name
        self.uid = organization_id


class Building:

    def __init__(self, building_id, name, organization_id):
        self.name = name
        self.uid = building_id
        self.owner = organization_id


class Floor:

    def __init__(self, floor_id, story, building_id):
        self.name = story
        self.uid = floor_id
        self.owner = building_id


class Room:

    def __init__(self, room_id, name, floor_id, location):
        self.name = name
        self.uid = room_id
        self.owner = floor_id
        self.location = location
