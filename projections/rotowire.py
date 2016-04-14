

from bs4 import BeautifulSoup
import urllib2
from namemapper import Ascii



#### Importing Projections from RotoWire ####

class ReadRotoWire:

    def __init__(self, url):
        req = urllib2.Request(url)
        connection = urllib2.urlopen(req)
        document = connection.read()
        soup = BeautifulSoup(document, "html.parser")
        connection.close()

        table = soup.find_all('table', {'id': 'playerPoolTable'})[0]
        players = table.find_all('tr')
        players = players[2:]

        self.projections = []
        for player in players:
            name = Ascii(player.find_all('td')[1].a.text)
            proj = float(player.find_all('td', {'class': 'rwo-points basic'})[0].input.get('value'))
            self.projections.append([name, proj])

    def ReturnProjections(self):
        return self.projections
