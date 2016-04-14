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
from stackbuilders import Stack5
from stackbuilders import Stack4
from stackbuilders import Stack3
from stacks import PitcherStack
from copy import copy
from time import time
from stackbuilders import BuildLists
from projections.rotowire import ReadRotoWire
import csv
from player import Lineup53

print "\n\n"

#### Importing DK Salary File as Dictionary of Player Objects Keyed on ASCII Name ####
playermap = DKSalaryImport('DKSalaries.csv').PlayerList()

#### Importing Baseballpress.com Starting Lineup, Batting order and handedness information ####
lineups = BaseballPressReader('http://www.baseballpress.com/lineups').ReadStartingLineups()

#### Can also import this informaiton from RotoGrinders. ## https://rotogrinders.com/lineups/mlb?date=2015-04-07&site=draftkings // https://rotogrinders.com/lineups/mlb?date=2016-04-03&site=draftkings
# TODO: Add 'projected lineup' variable to reader.
#rglineups = RGReader('https://rotogrinders.com/lineups/mlb?site=draftkings').ReadStarters()
#print rglineups


######### Where match exists, update player batting order and handedness #######
## BPress update must be in format [batting-order, ascii-name, handedness, position]
updater = PlayerUpdate(playermap)
#playermap = updater.UpdateRG(rglineups)
playermap = updater.UpdateBaseballPress(lineups)

###### Write unmatched names from scraped sources to MissingNames.csv ########
scrapednames = []
for item in lineups:
    scrapednames.append(item[1])
WriteMissingNames(scrapednames).WriteNames()

projections = []
roto = ReadRotoWire('http://www.rotowire.com/daily/mlb/optimizer.htm?site=DraftKings')
projections = roto.ReturnProjections()

playermap = updater.RotoProj(projections)


### Importing Player Projections: ###
# NumberFire http://www.numberfire.com/mlb/fantasy/fantasy-baseball-projections
# FantasyPros http://www.fantasypros.com/mlb/
# SwishAnalytics https://www.swishanalytics.com/optimus/mlb/dfs-pitcher-projections
# RotoWire http://www.rotowire.com/daily/mlb/optimizer.htm?site=DraftKings ## HAS DATA FOR APRIL4 ALREADY!
# RotoGrinders https://rotogrinders.com/offers/mlb?site=draftkings
# BaseballMonster #### HAS PAYWALL - NEED TO LOG IN TO VIEW

######################
## BUILDING LINEUPS ##
######################

#for player in playermap.values():
#    if player.team == 'Hou' or player.team == 'NYY' or player.team == 'Min' or player.team == 'Bal' or player.team == 'Cle' or player.team == 'Bos':
#        player.battingOrder = 'NA'


time1 = time()

lineuplists = BuildLists(playermap)

teams = lineuplists.ReturnBatters()
pitchers = lineuplists.ReturnPitchers()

print 'Team: eligible batters'
for team in teams:
    print '%s: %d' % (team[0], len(team[1]))


## WHAT DO WE HAVE: LIST OF TEAMS AND ASSOCIATED PLAYER OBJECTS

## We can now use this to create 4-stacks of players (or 5- or 3-...):

stacks5 = Stack5(teams).ReturnStacks5()
#stacks = Stack4(teams).ReturnStacks4()
stacks3 = Stack3(teams).ReturnStacks3()
stacks = []

print "\nCreated %d position legal 4-batter stacks, %d 5-batter stacks, and %d 3-batter stacks!\n" % (len(stacks), len(stacks5), len(stacks3))

teamstacks5 = []
for team in teams:
    teamstacks5.append([team[0], []])

for stack in stacks5:
    for team in teamstacks5:
        if team[0] == stack.player1.team:
            team[1].append(stack)
            break

teamstacks3 = []
for team in teams:
    teamstacks3.append([team[0], []])

for stack in stacks3:
    for team in teamstacks3:
        if team[0] == stack.player1.team:
            team[1].append(stack)
            break



fullbatters = []

team1 = 0
while team1 < len(teamstacks5) - 1:
    for stack1 in teamstacks5[team1][1]:
        team2 = team1 + 1
        while team2 < len(teamstacks3):
            for stack2 in teamstacks3[team2][1]:
                if stack1.stackpos == stack2.pairpos and stack1.salary + \
                        stack2.salary < 38000 and stack1.salary + stack2.salary > 26000:
                    fullbatters.append([stack1, stack2])
            team2 += 1
    team1 += 1

print "\nFound %d total possible legal 8-batter combinations\n" % (len(fullbatters))

pitcherstacks = []

p1 = 0
while p1 < len(pitchers) - 1:
    p2 = p1 + 1

    while p2 < len(pitchers):
        if pitchers[p2].team == pitchers[p1].opp:
            p2 += 1
            continue
        pitcherstacks.append(PitcherStack(pitchers[p1], pitchers[p2]))
        p2 += 1
    p1 += 1

print "\nBuilt %d total 2-pitcher stacks\n" % (len(pitcherstacks))

fulllineups = []

for bats in fullbatters:
    for arms in pitcherstacks:
        if arms.team1 == bats[0].opp or arms.team1 == bats[1].opp \
            or arms.team2 == bats[0].opp or arms.team2 == bats[1].opp \
            or arms.salary + bats[0].salary + bats[1].salary > 50000 \
            or arms.salary + bats[0].salary + bats[1].salary < 45000:
            continue
        fulllineups.append(Lineup53(arms, bats[0], bats[1]))

print "\nBuilt %d total legal full lineups! Entire process took %.2f seconds.\n" % (len(fulllineups), time()-time1)

print "aggregated lineups"

sortedfinal = sorted(fulllineups, key=lambda lineup: lineup[2], reverse=True)

print "sorted lineups"

usedteams = []

finallineups = None

with open('lineups.csv', 'wb') as nameFile:
    nameFilewriter = csv.writer(nameFile)
    total = 0
    for lineup in sortedfinal:
        legal = 1
        for stack in usedteams:
            if lineup[0]+lineup[1] == stack:
                legal = 0
                break
        if legal == 1:
            nameFilewriter.writerow(lineup)
            usedteams.append(lineup[0]+lineup[1])
            total += 1







