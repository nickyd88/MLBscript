######################################
#                                    #
# Classes to build 3, 4 and 5-stacks #
#                                    #
######################################

from copy import copy
from stacks import BatterStack5
from stacks import BatterStack4
from stacks import BatterStack3
from stacks import PitcherStack




class BuildLists:

    def __init__(self, playermap):

        self.batters = []
        self.pitchers = []

        for player in playermap.values():
            if player.position == 'SP' and player.battingOrder == 0:
                self.pitchers.append(player)
                continue
            if player.battingOrder == 0 or player.battingOrder == 'NA':
                continue
            pos = player.position.split('/')
            if len(pos) > 1:
                for item in pos:
                    player.position = item
                    newplayer = copy(player)
                    self.batters.append(newplayer)
            else:
                self.batters.append(player)

        ## Create list of all teams playing:
        self.teams = []
        for player in self.batters:
            dupe = 0
            for team in self.teams:
                if team[0] == player.team:
                    dupe = 1
            if dupe == 0:
                self.teams.append([player.team, []])

        ## Add in batters to their associated team list
        for team in self.teams:
            for batter in self.batters:
                if team[0] == batter.team:
                    team[1].append(batter)
        for team in self.teams:
            sortedbats = sorted(team[1], key=lambda player: player.battingOrder)
            team[1] = sortedbats

        self.teams = sorted(self.teams, key=lambda team: team[0])

    def ReturnBatters(self):
        return self.teams

    def ReturnPitchers(self):
        return self.pitchers

class Stack5:

    def __init__(self, teams): ## Teams is of form [['Team1', [PlayerObj1, PlayerObj2, ...]],['Team2',[PlayerObj1,...]]]

        self.stacks = []

        positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
        pos = {}
        for item in positions:
            pos[item] = 0

        posvalue = {}
        posvalue['C'] = 100000
        posvalue['1B'] = 10000
        posvalue['2B'] = 1000
        posvalue['3B'] = 100
        posvalue['SS'] = 10
        posvalue['OF'] = 1

        for team in teams:
            p1 = 0

            while p1 < len(team[1]) - 4:
                p2 = p1 + 1

                while p2 < len(team[1]) - 3:
                    if team[1][p1].dkId == team[1][p2].dkId:
                        p2 += 1
                        continue
                    p3 = p2 + 1

                    while p3 < len(team[1]) - 2:
                        if team[1][p2].dkId == team[1][p3].dkId:
                            p3 += 1
                            continue
                        p4 = p3 + 1

                        while p4 < len(team[1]) - 1:
                            if team[1][p3].dkId == team[1][p4].dkId:
                                p4 += 1
                                continue
                            p5 = p4 + 1

                            while p5 < len(team[1]):
                                if team[1][p5].dkId == team[1][p4].dkId:
                                    p5 += 1
                                    continue
                                partial = [team[1][p1], team[1][p2], team[1][p3], team[1][p4], team[1][p5]]

                                for item in positions:
                                    pos[item] = 0

                                value = 0
                                for player in partial:
                                    try:
                                        pos[player.position] += 1
                                        value = value + posvalue[player.position]
                                    except IndexError:
                                        pass

                                legal = 1
                                for item in positions:
                                    if pos[item] > 1:
                                        if item == 'OF' and pos[item] > 3:
                                            legal = 0
                                            break
                                        elif item == 'OF':
                                            pass
                                        else:
                                            legal = 0
                                            break

                                if legal == 0:
                                    p5 += 1
                                    continue

                                self.stacks.append(BatterStack5(team[1][p1], team[1][p2], team[1][p3], team[1][p4], team[1][p5], value))

                                p5 += 1
                            p4 += 1
                        p3 += 1
                    p2 += 1
                p1 += 1

    def ReturnStacks5(self):
        return self.stacks

class Stack4:

    def __init__(self, teams): ## Teams is of form [['Team1', [PlayerObj1, PlayerObj2, ...]],['Team2',[PlayerObj1,...]]]

        self.stacks = []

        positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
        pos = {}
        for item in positions:
            pos[item] = 0

        posvalue = {}
        posvalue['C'] = 100000
        posvalue['1B'] = 10000
        posvalue['2B'] = 1000
        posvalue['3B'] = 100
        posvalue['SS'] = 10
        posvalue['OF'] = 1

        for team in teams:
            p1 = 0

            while p1 < len(team[1]) - 3:
                p2 = p1 + 1

                if team[1][p1].dkId == team[1][p2].dkId or team[1][p2].battingOrder - team[1][p1].battingOrder > 2:
                    p2 += 1
                    continue
                while p2 < len(team[1]) - 2:
                    p3 = p2 + 1

                    while p3 < len(team[1]) - 1:
                        if team[1][p2].dkId == team[1][p3].dkId or team[1][p3].battingOrder - team[1][p2].battingOrder > 2:
                            p3 += 1
                            continue
                        p4 = p3 + 1

                        while p4 < len(team[1]):
                            if team[1][p4].dkId == team[1][p3].dkId or team[1][p4].battingOrder - team[1][p3].battingOrder > 2:
                                p4 += 1
                                continue
                            partial = [team[1][p1], team[1][p2], team[1][p3], team[1][p4]]

                            for item in positions:
                                pos[item] = 0

                            value = 0
                            for player in partial:
                                try:
                                    pos[player.position] += 1
                                    value = value + posvalue[player.position]
                                except IndexError:
                                    pass

                            legal = 1
                            for item in positions:
                                if pos[item] > 1:
                                    if item == 'OF' and pos[item] > 3:
                                        legal = 0
                                        break
                                    elif item == 'OF':
                                        pass
                                    else:
                                        legal = 0
                                        break

                            if legal == 0:
                                p4 += 1
                                continue

                            self.stacks.append(BatterStack4(team[1][p1], team[1][p2], team[1][p3], team[1][p4], value))

                            p4 += 1
                        p3 += 1
                    p2 += 1
                p1 += 1

    def ReturnStacks4(self):
        return self.stacks

class Stack3:

    def __init__(self, teams): ## Teams is of form [['Team1', [PlayerObj1, PlayerObj2, ...]],['Team2',[PlayerObj1,...]]]

        self.stacks = []

        positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
        pos = {}
        for item in positions:
            pos[item] = 0

        posvalue = {}
        posvalue['C'] = 100000
        posvalue['1B'] = 10000
        posvalue['2B'] = 1000
        posvalue['3B'] = 100
        posvalue['SS'] = 10
        posvalue['OF'] = 1

        for team in teams:
            p1 = 0

            while p1 < len(team[1]) - 2:
                p2 = p1 + 1

                while p2 < len(team[1]) - 1:
                    if team[1][p1].dkId == team[1][p2].dkId:
                        p2 += 1
                        continue
                    p3 = p2 + 1

                    while p3 < len(team[1]):
                        if team[1][p2].dkId == team[1][p3].dkId:
                            p3 += 1
                            continue
                        partial = [team[1][p1], team[1][p2], team[1][p3]]

                        for item in positions:
                            pos[item] = 0

                        value = 0
                        for player in partial:
                            try:
                                pos[player.position] += 1
                                value = value + posvalue[player.position]
                            except IndexError:
                                pass

                        legal = 1
                        for item in positions:
                            if pos[item] > 1:
                                if item == 'OF' and pos[item] > 3:
                                    legal = 0
                                    break
                                elif item == 'OF':
                                    pass
                                else:
                                    legal = 0
                                    break

                        if legal == 0:
                            p3 += 1
                            continue

                        self.stacks.append(BatterStack3(team[1][p1], team[1][p2], team[1][p3], value))

                        p3 += 1
                    p2 += 1
                p1 += 1

    def ReturnStacks3(self):
        return self.stacks