#########################################
#                                       #
# Updating Player Objects with web data #
#                                       #
#########################################

from namemapper import NameToDK


class PlayerUpdate:

    def __init__(self, playermap):
        self.playermap = playermap
        self.dict = NameToDK()

#### bpress must be list of len=4 lists of players [batting-order, ascii-name, handedness, position]
    def UpdateBaseballPress(self, bpress):
        for item in bpress:
            try:
                self.playermap[self.dict.GetDKFromName(item[1])].battingOrder = item[0]
                self.playermap[self.dict.GetDKFromName(item[1])].handedness = item[2]
            except KeyError:
                continue
        return self.playermap

#### bpress must be list of len=4 lists of players [batting-order, ascii-name, handedness, position, gameinfo, isConfirmed]
    def UpdateRG(self, rglineups):
        for item in rglineups:
            try:
                if item[4] == self.playermap[self.dict.GetDKFromName(item[1])].gameInfo.split(' ')[0]:
                    self.playermap[self.dict.GetDKFromName(item[1])].battingOrder = item[0]
                    self.playermap[self.dict.GetDKFromName(item[1])].handedness = item[2]
                    self.playermap[self.dict.GetDKFromName(item[1])].isConfirmed = item[5]
                else:
                    print item[4], self.playermap[self.dict.GetDKFromName(item[1])].gameInfo.split(' ')[0]
            except KeyError:
                continue
        return self.playermap


    def RotoProj(self, projections):
        for item in projections:
            try:
                self.playermap[self.dict.GetDKFromName(item[0])].projFP = item[1]
            except KeyError:
                continue
        return self.playermap