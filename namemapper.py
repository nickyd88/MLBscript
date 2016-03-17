import csv


class NameToDK:
    def __init__(self):
        self.idSet = {}
        with open('DKnameMapper.csv', 'rb') as idConversions:
            idReader = csv.reader(idConversions, delimiter=',')
            for idRow in idReader:
                self.idSet[idRow[0]] = idRow[1]

    def GetDKFromName(self, nameString):
        try:
            id = self.idSet[nameString]
            return id
        except KeyError:
            return 0