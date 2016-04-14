#################################
#                               #
# Classes to build full lineups #
#                               #
#################################


class Full44:

    def __init__(self, teams, stacks):

        self.teamstacks = []
        self.fullbatters = []

        for team in teams:
            self.teamstacks.append([team[0], []])

        for stack in stacks:
            for team in self.teamstacks:
                if team[0] == stack.player1.team:
                    team[1].append(stack)
                    break

        team1 = 0
        while team1 < len(self.teamstacks) - 1:
            for stack1 in self.teamstacks[team1][1]:
                team2 = team1 + 1
                while team2 < len(self.teamstacks):
                    for stack2 in self.teamstacks[team2][1]:
                        if stack1.stackpos == stack2.pairpos and stack1.salary + \
                                stack2.salary < 38000 and stack1.salary + stack2.salary > 26000:
                            self.fullbatters.append([stack1, stack2])
                    team2 += 1
            team1 += 1

    def ReturnBatters(self):
        return self.fullbatters



class Full53:

    def __init__(self, teams, stacks5, stacks3):

        self.teamstacks = []
        self.fullbatters = []

        for team in teams:
            self.teamstacks.append([team[0], []])

        for stack in stacks:
            for team in self.teamstacks:
                if team[0] == stack.player1.team:
                    team[1].append(stack)
                    break

        team1 = 0
        while team1 < len(self.teamstacks) - 1:
            for stack1 in self.teamstacks[team1][1]:
                team2 = team1 + 1
                while team2 < len(self.teamstacks):
                    for stack2 in self.teamstacks[team2][1]:
                        if stack1.stackpos == stack2.pairpos and stack1.salary + \
                                stack2.salary < 38000 and stack1.salary + stack2.salary > 26000:
                            self.fullbatters.append([stack1, stack2])
                    team2 += 1
            team1 += 1

    def ReturnBatters(self):
        return self.fullbatters


