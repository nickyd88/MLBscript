

#import urllib2
#opener = urllib2.build_opener()
#opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
#url = "https://rotogrinders.com/projected-stats/mlb?site=draftkings"
#response = opener.open(url)
#page = response.read()
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(page)



import urllib2
from bs4 import BeautifulSoup


url = 'https://rotogrinders.com/projected-stats/mlb?site=draftkings'
req = urllib2.Request(url)
req.add_header('User-Agent', 'Google Chrome')
connection = urllib2.urlopen(req)
document = connection.read()
soup = BeautifulSoup(document, "html.parser")
connection.close()


print soup




















