import json

class Result:
    def __str__(self):
        return json.dumps(self.__dict__)

    def __init__(self, artist, song, rating, kind, url):
        self.artist = artist
        self.song   = song
        self.rating = rating
        self.kind   = kind
        self.url    = url

    def get_tabular(self):
        return [
            self.artist,
            self.song,
            self.rating,
            self.kind
        ]

    def get_url(self):
        return self.url