from enum import Enum


class Status(Enum):
    SOLO = "Solo artist"
    BAND = "Band"
    ENSEMBLE = "Ensemble"
    ORCHESTRA = "Orchestra"

    @staticmethod
    def get_all():
        return [e.value for e in Status]


class Musician:
    def __init__(self, name, status, members):
        self.name = name
        self.members = members
        self.status = status

    def print(self):
        print(f'Name : {self.name}')
        print(f'Status: {"self.status.value"}')
        print('Members : ')
        for member in self.members:
            print(member)
