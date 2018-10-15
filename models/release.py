class Release:
    def __init__(self, name, date, style, musician_id):
        self.name = name
        self.date = date
        self.style = style
        self.musician_id = musician_id

    def print(self):
        print(f'Release name : {self.name}')
        print(f'Release date : {self.date}')
        print(f'Release style : {self.style}')
