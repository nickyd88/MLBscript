###################################################
#                                                 #
# Reading confirmed *and expected* batting orders #
#                                                 #
###################################################


import urllib2
from bs4 import BeautifulSoup
from namemapper import Ascii

## Reads Rotogrinders for starting info, and returns list of format [order, name, handedness, position]
## for pitchers, handedness = pitching not batting, and order = 0



class RGReader:

    def __init__(self, urlstring):
        req = urllib2.Request(urlstring)
        connection = urllib2.urlopen(req)
        document = connection.read()
        self.soup = BeautifulSoup(document, "html.parser")
        connection.close()
        self.players = []

    def ReadStarters(self):
        if len(self.players) > 0:
            return self.players
        else:
            allgames = self.soup.find_all('div', {'class' : 'blk game'})

            teams = []
            for game in allgames:
                teams.append(game.find_all('div', {'class' : 'blk away-team'})[0])
                teams.append(game.find_all('div', {'class' : 'blk home-team'})[0])

            for team in teams:
                pitcher = team.find_all('div', {'class' : 'pitcher players'})[0]
                try:
                    self.players.append([0, pitcher.a.text, Ascii(pitcher.find_all('span', {'class' : 'stats'})[0].text.split()[0]), 'SP'])
                except IndexError:
                    pass
                batters = team.find_all('li', {'class' : 'player'})
                for batter in batters:
                    order = batter.find_all('span', {'class' : 'order'})[0].text
                    try:
                        position = batter.find_all('span', {'class' : 'position'})[0].text.split()[0]
                    except IndexError:
                        continue
                    name = batter.find_all('span', {'class' : 'pname'})[0].text.strip("\n")
                    handedness = batter.find_all('span', {'class' : 'stats'})[1].text.split()[0]
                    if position == 'SP':
                        continue
                    self.players.append([int(order), name, handedness, position])
            return self.players

