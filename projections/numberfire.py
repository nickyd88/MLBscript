

from bs4 import BeautifulSoup
import urllib2
from namemapper import Ascii



#### Importing Projections from NumberFire ####

url = 'http://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/batters'
req = urllib2.Request(url)
connection = urllib2.urlopen(req)
document = connection.read()
soup = BeautifulSoup(document, "html.parser")
connection.close()


print soup



