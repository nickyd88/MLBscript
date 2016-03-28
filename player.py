#
# #
# # # A Player Class. Used to create Player objects, initialized with important player attributes:
# #         - Name, Matchup, Position, Salary, PlayerId, etc.
#

from namemapper import Ascii

class Player:

    def __init__(self, position, uname, dkId, salary, gameInfo, team):
        self.position = position
        self.name = Ascii(uname)
        self.uname = uname
        self.dkId = dkId
        self.salary = salary
        self.gameInfo = gameInfo
        self.team = team
        self.IsStarting = 0
        self.IsConfirmed = 0
        self.battingOrder = 'NA'
        self.handedness = 'NA'
        if self.gameInfo.split('@')[0] == self.team:
            self.opp = self.gameInfo.split('@')[1].split()[0]
        else:
            self.opp = self.gameInfo.split('@')[0]

    def Print(self):
        print(self.name, self.position, self.battingOrder, self.team, self.opp, self.salary, self.dkId)




