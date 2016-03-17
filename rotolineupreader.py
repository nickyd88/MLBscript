#                            #
#                            #
# SCRAPING FOR SPECIFIC DATA #
#                            #
#                            #

import urllib2
from bs4 import BeautifulSoup

class RotoWireNBAReader:

    def __init__(self, url):
        req = urllib2.Request(url)
        connection = urllib2.urlopen(req) # or (req, timeout= 5) #timeout in seconds
        document = connection.read()
        self.soup = BeautifulSoup(document, "html.parser")
        self.starters = []

    def ReturnStarters(self):
        if len(self.starters) == 0:
            matchups = self.soup.find_all('div', {'class' : 'span49'})
            teamstart = 6
            teamend = len(matchups)-1

            row = teamstart
            while row < teamend:
                matchup = matchups[row].find_all('div', {'class' : 'offset1 span15'})
                for game in matchup:
                    team1conf = 0
                    team2conf = 0
                    teamsinfo = game.find_all('div')[0]
                    team1 = teamsinfo.find_all('div')[0].img['src']
                    team2 = teamsinfo.find_all('div')[4].img['src']
                    if team1 == 'http://content.rotowire.com/images/lineup-green.png':
                        team1conf = 1
                    if team2 == 'http://content.rotowire.com/images/lineup-green.png':
                        team2conf = 1
                    teamplayers = game.find_all('div', {'class' : 'dlineups-half'})
                    players1 = teamplayers[0].find_all('div', {'class' : 'dlineups-vplayer'})
                    players2 = teamplayers[1].find_all('div', {'class' : 'dlineups-hplayer'})
                    player = 0
                    while player < 5:
                        try:
                            self.starters.append([players1[player].find_all('div')[1].text, team1conf, players1[player].find_all('div')[2].text])
                        except IndexError:
                            self.starters.append([players1[player].find_all('div')[1].text, team1conf, 'Clear'])
                        try:
                            self.starters.append([players2[player].find_all('div')[1].text, team2conf, players2[player].find_all('div')[2].text])
                        except IndexError:
                            self.starters.append([players2[player].find_all('div')[1].text, team2conf, 'Clear'])
                        player += 1
                row += 1
            return self.starters
        else:
            return self.starters




