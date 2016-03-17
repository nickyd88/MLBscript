#
# #
# # # A Player Class. Used to create Player objects, initialized with important player attributes:
# #         - Name, Matchup, Position, Salary, PlayerId, etc.
#

class Player:

    def __init__(self, position, name, dkId, salary, gameInfo, team, opp, projFP, status, starting, confirmed):
        self.position = position
        self.name = name
        self.dkId = dkId
        self.salary = salary
        self.gameInfo = gameInfo
        self.team = team
        self.opp = opp
        self.projFP = projFP
        self.status = status
        self.starting = starting
        self.confirmed = confirmed

    def Print(self):
        print(self.name, self.position, self.team, self.salary, self.dkId, self.gameInfo, self.opp, self.projFP, self.status, self.starting, self.confirmed)