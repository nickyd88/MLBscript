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
        self.isConfirmed = 'NA'
        self.projFP = 0
        if self.gameInfo.split('@')[0] == self.team:
            self.opp = self.gameInfo.split('@')[1].split()[0]
        else:
            self.opp = self.gameInfo.split('@')[0]

    def Print(self):
        print(self.name, self.position, self.battingOrder, self.team, self.opp, self.salary, self.dkId)

def Lineup53(pitchers, batters5, batters3):
        pitchers = pitchers.list
        batters = batters5.list
        batters.extend(batters3.list)
        team1 = batters5.list[0].team
        team2 = batters3.list[0].team
        p1 = pitchers[0]
        p2 = pitchers[1]
        of = 0
        for player in batters:
            if player.position == 'C':
                c = player
                continue
            if player.position == '1B':
                b1 = player
                continue
            if player.position == '2B':
                b2 = player
                continue
            if player.position == '3B':
                b3 = player
                continue
            if player.position == 'SS':
                ss = player
                continue
            if of == 0:
                of1 = player
                of += 1
                continue
            if of == 1:
                of2 = player
                of += 1
                continue
            of3 = player
            continue
        projFP = p1.projFP + p2.projFP + c.projFP + b1.projFP + b2.projFP + b3.projFP + ss.projFP + of1.projFP + of2.projFP + of3.projFP
        return [team1, team2, projFP, p1.dkId, p2.dkId, c.dkId, b1.dkId, b2.dkId, b3.dkId, ss.dkId, of1.dkId, of2.dkId, of3.dkId]