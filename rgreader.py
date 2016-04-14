###################################################
#                                                 #
# Reading confirmed *and expected* batting orders #
#                                                 #
###################################################


import urllib2
from bs4 import BeautifulSoup
from namemapper import Ascii
from namemapper import TeamAbbrv

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
        self.TeamNames = TeamAbbrv()

    def ReadStarters(self):
        if len(self.players) > 0:
            return self.players
        else:
            allmatchups = self.soup.find_all('div', {'class': 'blk crd lineup'})

            allgames = []
            for matchup in allmatchups:
                away = self.TeamNames.GetDKAbbrv(matchup.find_all('span', {'class': 'shrt'})[0].text)
                home = self.TeamNames.GetDKAbbrv(matchup.find_all('span', {'class': 'shrt'})[1].text)
                info = away+'@'+home
                gameblk = matchup.find_all('div', {'class': 'blk lineup-content drw'})[0]

                try:
                    gamesoup = gameblk.find_all('div', {"class": "blk game"})[0]
                    print len(gamesoup)
                except IndexError:
                    continue

                allgames.append([info, gamesoup])

            #### REMOVES FIRST GAME IN ALL DOUBLE-HEADERS ####
            dupes = []
            for game1 in allgames:
                for game2 in allgames:
                    dupe = 0
                    for item in dupes:
                        if item[0] == game1[0]:
                            dupe = 1
                            break ## if matchup is already in dupes, ignore it.

                    if game1[0] == game2[0] and game1[1] != game2[1] and dupe == 0:
                        dupes.append(game1)
                        break

            for game in dupes:
                allgames.remove(game)

            teams = []
            for game in allgames:
                teams.append([game[0],game[1].find_all('div', {'class' : 'blk away-team'})[0]])
                teams.append([game[0],game[1].find_all('div', {'class' : 'blk home-team'})[0]])

            for teaminfo in teams:
                team = teaminfo[1]
                pitcher = team.find_all('div', {'class' : 'pitcher players'})[0]
                conf = team.find_all('ul', {'class': 'players unconfirmed'})
                if len(conf) > 0:
                    confirm = 0
                else:
                    confirm = 1
                try:
                    self.players.append([0, pitcher.a.text, Ascii(pitcher.find_all('span', {'class' : 'stats'})[0].text.split()[0]), 'SP', teaminfo[0], 1, pitcher.find_all('span', {'class' : 'fpts'})[0].text])
                except IndexError:
                    pass
                except AttributeError:
                    pass
                batters = team.find_all('li', {'class' : 'player'})
                for batter in batters:
                    order = batter.find_all('span', {'class' : 'order'})[0].text
                    try:
                        position = batter.find_all('span', {'class' : 'position'})[0].text.split()[0]
                    except IndexError:
                        continue
                    name = batter.find_all('span', {'class' : 'pname'})[0].text.strip("\n")
                    try:
                        handedness = batter.find_all('span', {'class' : 'stats'})[1].text.split()[0]
                    except IndexError:
                        continue
                    if position == 'SP':
                        continue
                    self.players.append([int(order), name, handedness, position, teaminfo[0], confirm])
            return self.players








