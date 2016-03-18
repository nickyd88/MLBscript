#                      #
#  Consolidating Code  #
#  Main Python Script  #
#                      #
#                      #
#                      #

import csv
from csvimport import DKSalaryImport
from baseballpress import BaseballPressReader
from rotolineupreader import RotoWireNBAReader
from rotoprojreader import RotowireProjReader
from namemapper import NameToDK






#### Importing DK Salary File as Player Objects ####
filename = 'DKSalaries.csv'
playerlist = DKSalaryImport(filename).PlayerList()

print "\n"
playerlist.values()[0].Print()
playerlist['Kelly Oubre Jr.'].Print()
print "\n"


#### Importing Baseballpress.com Starting Lineup, Batting order and handedness information ####
bpress = 'http://www.baseballpress.com/lineups'
bpreader = BaseballPressReader(bpress)
lineups = bpreader.ReadStartingLineups()

print "\n", lineups, "\n"


#### Importing Rotowire NBA Starter projections, along with gametime decision status and starting 5 confirmation status ####
rotonba = 'http://www.rotowire.com/basketball/nba_lineups.htm'
rotonbareader = RotoWireNBAReader(rotonba)
starters = rotonbareader.ReturnStarters()

print starters, "\n"
status = 'GTD'
for player in starters:
    if player[2] == status:
        print player[0], "is a GTD"
print "\n"


#### Importing Rotowire NBA player projections ####
rotoproj = 'http://www.rotowire.com/daily/nba/optimizer.htm?site=DraftKings&sport=NBA&projections='
rotoprojreader = RotowireProjReader(rotoproj)
rotoprojections = rotoprojreader.ReturnProjections()
rotoprojsorted = sorted(rotoprojections, key=lambda player: player[1], reverse= True)

print "Top 5 Rotowire Projected Players:"
i = 0
while i < 5:
    print rotoprojsorted[i][1], rotoprojsorted[i][0]
    i += 1
print "\n"


#### Understanding how Name Mapping and Hashsets work ####
with open('MissingNames.csv', 'wb') as nameFile:
    nameFileWriter = csv.writer(nameFile)
    dictionary = NameToDK()

    for player in starters:
        if dictionary.GetDKFromName(player[0]) == 0:
            nameFileWriter.writerow([player[0]])

    for player in rotoprojections:
        if dictionary.GetDKFromName(player[0]) == 0:
            nameFileWriter.writerow([player[0]])


#### Taking opponent info out from "matchup" field ####
for playeritem in playerlist.values():
    if playeritem.gameInfo.split('@')[0] == playeritem.team:
        playeritem.opp = playeritem.gameInfo.split('@')[1].split()[0]
    else:
        playeritem.opp = playeritem.gameInfo.split('@')[0]


#### Updating projected points field from RotowireProj ####
for item in rotoprojections:
    try:
        playerlist[dictionary.GetDKFromName(item[0])].projFP = float(item[1])
    except KeyError:
        pass
playerlist['Kelly Oubre Jr.'].Print()


#### Updating projected points field from RotowireProj ####
for item in starters:
    try:
        playerlist[dictionary.GetDKFromName(item[0])].starting = 1
        playerlist[dictionary.GetDKFromName(item[0])].confirmed = item[1]
        playerlist[dictionary.GetDKFromName(item[0])].status = item[2]
    except KeyError:
        pass
playerlist['Paul George'].Print()


#### Building Lineups from Player Objects ####

# NBA Lineup: PG, SG, SF, PF, C, G, F, Util (8 positions)

allstarters = []
for player in playerlist.values():
    if player.starting == 1:
        allstarters.append(player)

startinglist = sorted(allstarters, key= lambda player: player.salary, reverse= True)


print "\nGenerating Lineups...\n\n"

lineupnum = 0
mill = 1
minstarters = 8
clearplayers = 8
maxp1 = 5000
maxsalary = 50000
minsalary = 48000
legallineups = []
p1 = 0
while p1 < len(startinglist)-7: # - 7 because we need at least 7 other players to build the full 8 person lineup
    curplayer = 1
    if startinglist[p1].salary < minsalary/8:
        print "Checked all reasonable lineups"
        break
    partial1 = [startinglist[p1]]
    p2 = p1 + 1
    while p2 < len(startinglist) - 6:
        if curplayer > maxp1:
            break
        partial2 = []
        partial2.extend(partial1)
        partial2.append(startinglist[p2])
        p3 = p2 + 1
        while p3 < len(startinglist) - 5:
            if curplayer > maxp1:
                break
            partial3 = []
            partial3.extend(partial2)
            partial3.append(startinglist[p3])
            p4 = p3 + 1
            while p4 < len(startinglist) - 4:
                if curplayer > maxp1:
                    break
                partial4 = []
                partial4.extend(partial3)
                partial4.append(startinglist[p4])
                p5 = p4 + 1
                while p5 < len(startinglist) - 3:
                    if curplayer > maxp1:
                        break
                    partial5 = []
                    partial5.extend(partial4)
                    partial5.append(startinglist[p5])
                    p6 = p5 + 1
                    while p6 < len(startinglist) - 2:
                        if curplayer > maxp1:
                            break
                        partial6 = []
                        partial6.extend(partial5)
                        partial6.append(startinglist[p5])
                        p7 = p6 + 1
                        while p7 < len(startinglist) - 1:
                            if curplayer > maxp1:
                                break
                            partial7 = []
                            partial7.extend(partial6)
                            partial7.append(startinglist[p7])
                            p8 = p7 + 1
                            while p8 < len(startinglist):
                                if curplayer > maxp1:
                                    break
                                partial8 = []
                                partial8.extend(partial7)
                                partial8.append(startinglist[p8])
                                clear = 0
                                starter = 0
                                salary = 0
                                pg = 0
                                sg = 0
                                sf = 0
                                pf = 0
                                c = 0
                                g = 0
                                f = 0
                                for player in partial8:
                                    lineupnum += 1
                                    if lineupnum == 1000000:
                                        lineupnum = 0
                                        print "Checked",mill,"million lineups"
                                        mill += 1
                                    starter = starter + player.starting
                                    salary = salary + player.salary
                                    if player.status == 'Clear':
                                        clear += 1
                                    if player.position == 'PG':
                                        pg += 1
                                        g += 1
                                    if player.position == 'SG':
                                        sg += 1
                                        g += 1
                                    if player.position == 'SF':
                                        sf += 1
                                        f += 1
                                    if player.position == 'PF':
                                        pf += 1
                                        f += 1
                                    if player.position == 'C':
                                        c += 1
                                if pg >= 1 and sg >= 1 and sf >= 1 and pf >= 1 and c >= 1 and g >= 3 and f >= 3 and\
                                                salary <= maxsalary and clear == clearplayers and starter == minstarters\
                                                and salary >= minsalary:
                                    legallineups.append(partial8)
                                    curplayer += 1
                                p8 += 1
                            p7 += 1
                        p6 += 1
                    p5 += 1
                p4 += 1
            p3 += 1
        p2 += 1
    p1 += 1

print "\nTotal Legal Lineups Created:",len(legallineups),"\nBest Legal Lineup:"














