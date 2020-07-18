
import urllib.request
import json

class FileSourceLoader:
    def __init__(self):
        self.__providers = {
            'vistazo': 'data_vistazo.json',
            'universo': 'data_universo.json',
            'comercio': 'data_comercio.json',
            'mercurio': 'data_mercurio.json',
            'expreso': 'data_expreso.json',
            'telegrafo': 'data_telegrafo.json'
        }
        
    def load(self, provider):
        with open('./data/' + self.__providers[provider], 'r') as file:
            data = file.read()
        return json.loads(data)

class HttpSourceLoader:
    def __init__(self):
        self.backend = 'http://localhost:9292/news/single'

    def load(self, news_url):
        url = "{}?url={}".format(self.backend, news_url)
        with urllib.request.urlopen(url) as request:
            data = request.read().decode()
        return json.loads(data)
