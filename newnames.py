################################################
## Class to write unmatched names to new file ##
################################################

import csv
from namemapper import NameToDK



## Class init requires list of scraped names where item[0] is the player name
class WriteMissingNames:

    def __init__(self, scrapednames):
        self.scrapednames = scrapednames
        self.map = NameToDK()

###### Write unmatched names from Starting Lineups to Name Matchup File ########
    def WriteNames(self):
        with open('MissingNames.csv', 'wb') as nameFile:
            nameFilewriter = csv.writer(nameFile)
            for player in self.scrapednames:
                if self.map.GetDKFromName(player) == 0:
                    nameFilewriter.writerow([player])

