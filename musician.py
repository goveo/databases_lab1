class Musician:
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def print(self):
        print(f'Name : {self.name}')
        print('Members : ')
        for member in self.members:
            print(member)