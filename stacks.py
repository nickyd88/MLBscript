#############################################
#                                           #
# Class to hold partial lineup (stack) info #
#                                           #
#############################################


class BatterStack5:

    def __init__(self, player1, player2, player3, player4, player5, value):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        self.stackpos = value
        self.pairpos = 111113 - self.stackpos
        self.salary = player1.salary + player2.salary + player3.salary + player4.salary + player5.salary
        self.team = player1.team
        self.opp = player1.opp
        self.list = [self.player1, self.player2, self.player3, self.player4, self.player5]

class BatterStack4:

    def __init__(self, player1, player2, player3, player4, value):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.stackpos = value
        self.pairpos = 111113 - self.stackpos
        self.salary = player1.salary + player2.salary + player3.salary + player4.salary
        self.team = player1.team
        self.opp = player1.opp
        self.list = [self.player1, self.player2, self.player3, self.player4]

class BatterStack3:

    def __init__(self, player1, player2, player3, value):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.stackpos = value
        self.pairpos = 111113 - self.stackpos
        self.salary = player1.salary + player2.salary + player3.salary
        self.team = player1.team
        self.opp = player1.opp
        self.list = [self.player1, self.player2, self.player3]

class PitcherStack:

    def __init__(self, pitcher1, pitcher2):
        self.pitcher1 = pitcher1
        self.pitcher2 = pitcher2
        self.salary = pitcher1.salary + pitcher2.salary
        self.team1 = pitcher1.team
        self.team2 = pitcher2.team
        self.list = [self.pitcher1, self.pitcher2]