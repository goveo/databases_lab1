class Release:
    def __init__(self, name, date):
        self.name = name
        self.date = date

    def print(self):
        print(f'Release name : {self.name}')
        print(f'Release date : {self.date}')