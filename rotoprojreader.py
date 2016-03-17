#                            #
#                            #
# SCRAPING FOR SPECIFIC DATA #
#                            #
#                            #

import urllib2
from bs4 import BeautifulSoup
import unicodedata

class RotowireProjReader:

    def __init__(self, url):
        req = urllib2.Request(url)
        connection = urllib2.urlopen(req) # or (req, timeout= 5) #timeout in seconds
        document = connection.read()
        self.soup = BeautifulSoup(document, "html.parser")
        self.projections = []

    def ReturnProjections(self):
        if len(self.projections) == 0:
            table = self.soup.find_all("tbody")[1]
            for row in table.find_all('tr'):
                    name = row.find_all("td")[1].a.text
                    asciiname = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
                    projfp = float(row.find_all("td")[9].text)
                    self.projections.append([asciiname, projfp])
            return self.projections
        else:
            return self.projections




