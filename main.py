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













