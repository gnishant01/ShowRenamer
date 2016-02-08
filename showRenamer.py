#-------------------------------------------------------------------------------
# Name:        ShowRenamer
# Purpose:     To rename every episode of a TV series, fetching the title of the episode from IMDb
# Author:      Gaurav Nishant
#-------------------------------------------------------------------------------

#!/usr/bin/python

import urllib, urllib2, os, re
from bs4 import BeautifulSoup

prefix = "http://www.imdb.com/"

# Class for HTML page
class Page:
	pageUrl = ''
	def __init__(self, url):
		self.pageUrl = url
	# this member function returns the soup object from the url
	def getHtml(self):
		completeUrl = prefix + self.pageUrl
		source = urllib2.urlopen(completeUrl)
		return BeautifulSoup(source, 'html.parser')

# function to take tv series name as parameter & return the url of the TV series landing page
def findSeriesHomeFromName(seriesName):
	url = prefix + "find/"
	data = {}
	data['q'] = seriesName.lower()
	data['ref_'] = 'nv_sr_fn'
	data['s'] = 'all'
	url_values = urllib.urlencode(data)
	url = url + '?' + url_values
	data = urllib2.urlopen(url)
	x = BeautifulSoup(data, 'html.parser')
	resultDiv = str(x.find_all("td", { "class" : "result_text" })[0].find('a').get('href'))
	return resultDiv


# function to fetch the names from IMDb and store in the list seasonWiseEpisodes
def fetchNamesFromIMDb():
	for seasonNumber in range(0, numOfSeasons):
		print '----- Fetching season', (seasonNumber + 1), 'episode names -----'
		seasonPage = Page(allSeasonsList[seasonNumber].get('href'))
		seasonHtml = seasonPage.getHtml()
		episodeListDiv = seasonHtml.find_all("div", {"class" : "info"})
		currentSeasonEpisode = []
		for episodeNumber in range(0, len(episodeListDiv)):
			episodeTitle = episodeListDiv[episodeNumber].strong.get_text()
			episodeName = seriesName
			if seasonNumber < 9:
				episodeName = episodeName + ' ' + 'S0' + str(seasonNumber + 1)
			else:
				episodeName = episodeName + ' ' + 'S' + str(seasonNumber + 1)			
			if episodeNumber < 9:
				episodeName = episodeName + 'E0' + str(episodeNumber + 1)
			else:			
				episodeName = episodeName + 'E' + str(episodeNumber + 1)
			episodeName = episodeName + ' - ' + episodeTitle

			# removing the '/' & '?' characters from filename 
			episodeName = episodeName.replace('/', '-')
			episodeName = episodeName.replace('?', '!')
			currentSeasonEpisode.append(episodeName)
		print '----- Season', (seasonNumber + 1), 'episode names fetched -----'
		seasonWiseEpisodes.append(currentSeasonEpisode)


# get episode name stored in the seasonWiseEpisodes list
def getEpisodeName(seasonNumber, episodeNumber):
	return seasonWiseEpisodes[seasonNumber - 1][episodeNumber - 1]

seriesName = raw_input('Give the series name: ')
path = raw_input('Give the series path in your PC: ')

homePage = Page(findSeriesHomeFromName(seriesName))
homeHtml = homePage.getHtml()

seriesName = homeHtml.find("div", {"class" : "title_wrapper"}).get_text().split('\n')[1].strip()
allSeasonsDiv = str(homeHtml.find_all("div", { "class" : "seasons-and-year-nav" })[0])

seasonsListDivHtml = BeautifulSoup(allSeasonsDiv, 'html.parser')
allSeasonsList = seasonsListDivHtml.find_all('a')
numOfSeasons = int(allSeasonsList[0].get_text())

# reverse the seasonList list
for seasonNumber in range(0, int(numOfSeasons / 2)):
	tempSeason = allSeasonsList[seasonNumber]
	allSeasonsList[seasonNumber] = allSeasonsList[numOfSeasons - seasonNumber - 1]
	allSeasonsList[numOfSeasons - seasonNumber - 1] = tempSeason

seasonWiseEpisodes = []
fetchNamesFromIMDb()

os.chdir(path)
count = 0
for subdir, dirs, files in os.walk(path, topdown = False):
	for i in dirs:
		dir = os.path.join(path, i)
		p = re.compile(".*[sS]\D*(\d+).*")
		x = p.match(i)
		if x:
			seasonNum = int(x.group(1))
			newDir = os.path.join(path, 'Season ' + str(seasonNum))
			os.rename(dir, newDir)

	os.chdir(subdir)
	for file in files:
		if re.match(".*s\D*\d+\D*e\D*\d+.*\..*", file, re.I):
			p = re.compile(".*[sS]\D*(\d+)\D*[eE]\D*(\d+).*(\..*)")
			x = p.match(file)
			seasonNum = int(x.group(1))
			episodeNum = int(x.group(2))
			extension = x.group(3)
			try:
				os.rename(file, getEpisodeName(seasonNum, episodeNum) + extension)
				count = count + 1
			except Exception:
				print 'Unable to rename file ' + file
print 'Total ' + str(count) + ' files renamed'