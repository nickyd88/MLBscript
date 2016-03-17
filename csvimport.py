#                           #
#                           #
#  READING FROM A .CSV FILE #
#                           #
#                           #

## Turn .csv import file into a class

import csv
import player

class DKSalaryImport:

    def __init__(self, filename):
        with open(filename, 'rb') as dksalaries:
            dksalariesreader = csv.reader(dksalaries, delimiter=',')
            startrow = 7
            currentrow = 0
            self.players = {}
            for row in dksalariesreader:
                if currentrow > startrow:
                    playerobject = player.Player(row[9], row[11], int(row[12]), int(row[13]), row[14], row[15], 'NoOpp', 0, 'NoStatus', 0, 0)
                    self.players[playerobject.name] = playerobject
                currentrow += 1

    def PlayerList(self):
        return self.players


