class Listener:
    def __init__(self, name, services):
        self.name = name
        self.services = services

    def print(self):
        print(f'Listener name : {self.name}')
        print('Listener services : ')
        for service in self.services:
            print(service)