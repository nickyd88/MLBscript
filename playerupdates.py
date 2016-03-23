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