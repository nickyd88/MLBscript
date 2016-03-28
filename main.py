#                      #
#  Consolidating Code  #
#  Main Python Script  #
#                      #
#                      #
#                      #

from csvimport import DKSalaryImport
from baseballpress import BaseballPressReader
from newnames import WriteMissingNames
from playerupdates import PlayerUpdate
from rgreader import RGReader
from stackbuilder import Stack

print "\n"

#### Importing DK Salary File as Dictionary of Player Objects Keyed on ASCII Name ####
playermap = DKSalaryImport('DKSalaries.csv').PlayerList()

#### Importing Baseballpress.com Starting Lineup, Batting order and handedness information ####
lineups = BaseballPressReader('http://www.baseballpress.com/lineups').ReadStartingLineups()

#### Can also import this informaiton from RotoGrinders.
# TODO: Add 'projected lineup' variable to reader.
rglineups = RGReader('https://rotogrinders.com/lineups/mlb?date=2015-04-07&site=draftkings').ReadStarters()

######### Where match exists, update player batting order and handedness #######
## BPress update must be in format [batting-order, ascii-name, handedness, position]
updater = PlayerUpdate(playermap)
playermap = updater.UpdateBaseballPress(lineups)

###### Write unmatched names from scraped sources to MissingNames.csv ########
scrapednames = []
for item in lineups:
    scrapednames.append(item[1])
WriteMissingNames(scrapednames).WriteNames()
















######################
## BUILDING LINEUPS ##
######################

## Step 1: convert multi-position players into distinct player objects with a single position ##
batters = []
pitchers = []
for player in playermap.values():
    if player.battingOrder == 0 or player.battingOrder == 'NA':
        continue
    pos = player.position.split('/')
    for item in pos:
        player.position = item
        batters.append(player)
for player in playermap.values():
    if player.position == 'SP' and player.battingOrder == 0:
        pitchers.append(player)
playermap = None


print "%d total batters and %d total starting pitchers scraped" % (len(batters), len(pitchers))

## creating list of all teams
teams = []
for player in batters:
    dupe = 0
    for team in teams:
        if team[0] == player.team:
            dupe = 1
            break
    if dupe == 0:
        teams.append([player.team, []])

## Adding players to list associated with each team and ordering batterlist by dkId
for team in teams:
    for batter in batters:
        if team[0] == batter.team:
            team[1].append(batter)
for team in teams:
    sortbat = sorted(team[1], key=lambda player: player.dkId, reverse=True)
    team[1] = sortbat

teams = sorted(teams, key=lambda team: team[0])

### Creating 4-stacks of players (create 4-4 stacks) ###


positions = ['C', '1B', '2B', '3B', 'SS', 'OF']
pos = {}
for item in positions:
    pos[item] = 0

stacks = []
for team in teams:
    p1 = 0

    while p1 < len(team[1]) - 3:
        partial = [team[1][p1]]
        p2 = p1 + 1

        while p2 < len(team[1]) - 2:
            if team[1][p2].dkId == team[1][p1].dkId:
                p2 += 1
                continue
            partial = [team[1][p1], team[1][p2]]
            p3 = p2 + 1

            while p3 < len(team[1]) - 1:
                if team[1][p3].dkId == team[1][p2].dkId:
                    p3 += 1
                    continue
                partial = [team[1][p1], team[1][p2], team[1][p3]]
                p4 = p3 + 1

                while p4 < len(team[1]):
                    if team[1][p4].dkId == team[1][p3].dkId:
                        p4 += 1
                        continue
                    for item in positions:
                        pos[item] = 0
                    partial = [team[1][p1], team[1][p2], team[1][p3], team[1][p4]]
                    stacksize = 0
                    for player in partial:
                        try:
                            pos[player.position] += 1
                            stacksize += 1
                        except IndexError:
                            pass
                    if stacksize < 4:
                        p4 += 1
                        continue
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
                    stacks.append(Stack(partial[0], partial[1], partial[2], partial[3]))
                    p4 += 1
                p3 += 1
            p2 += 1
        p1 += 1


teamstacks = []
for player in batters:
    dupe = 0
    for team in teamstacks:
        if team[0] == player.team:
            dupe = 1
            break
    if dupe == 0:
        teamstacks.append([player.team, []])

teamstacks = sorted(teamstacks, key=lambda team: team[0])

for stack in stacks:
    for team in teamstacks:
        if team[0] == stack.player1.team:
            team[1].append(stack)

stacks = None


## Now that we have all possible stacks of 4 players, we need to turn them into eligible stacks of 8 batters ##
fullbatters = []
n = 0
k = 0

for team1 in teamstacks:
    for stack1 in team1[1]:
        legalteam = 0
        for team2 in teamstacks:
            if team2[0] == team1[0]:
                legalteam = 1
                continue
            if legalteam == 0:
                continue
            for stack2 in team2[1]:
                if stack1.pairpos == stack2.stackpos:
                    n += 1
                    fullbatters.append([stack1.player1, stack1.player2, stack1.player3, stack1.player4, stack2.player1, stack2.player2, stack2.player3, stack2.player4])
                    if n == 1000000:
                        k += 1
                        n = 0
                        print "Found %d million legal 4-4 stack combinations!" % (k)


i = 0
for item in fullbatters:
    salary = 0
    for player in item:
        salary = salary + player.salary
    if salary < 32000:
        i+=1

print "\nBuilt %d legal 8-player batter stacks, %d are under 32k salary" % (len(fullbatters), i)













