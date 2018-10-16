class Release:
    def __init__(self, name, date, style, is_video, musician_id):
        self.name = name
        self.date = date
        self.style = style
        self.is_video = is_video
        self.musician_id = musician_id

    def print(self):
        print(f'Release name : {self.name}')
        print(f'Release date : {self.date}')
        print(f'Release style : {self.style}')
        print(f'Release have_video : {self.have_video}')
        print(f'Release musician_id : {self.musician_id}')
