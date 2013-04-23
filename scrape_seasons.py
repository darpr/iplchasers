#!/usr/bin/env python
# Author: Pradeep Sivakumar
# Task: Publish successful chases in IPL history.

import urllib2
from BeautifulSoup import BeautifulSoup
import re

SEASONS = ["http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2007/08;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2009;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2009/10;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2011;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2012;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2013;trophy=117;type=season"]
AGGTOPCHASERS = []

'''
Prepare a dictionary for each season, collecting total successful 
chases by each team.

Load a global list of dictionaries, thus collecting data across seasons.
'''
def getAllTimeChasingAggregate():
	for season in SEASONS:
		print "Processing Season: %s" % (season.split(';id=')[1].split(';')[0])
		
		page = urllib2.urlopen(season)
		soup = BeautifulSoup(page)

		results = []
		games = soup.findAll("tr","data1")
		for game in games:
			for attribute in game.findAll("td"):
				if attribute.renderContents() == "abandoned" or attribute.renderContents() == "tied":
					results.append("null")
				else:
					for team in attribute.findAll("a","data-link"):
						teamname = team.renderContents()
						results.append(teamname)
		
		successfulchasers = []
		for i in xrange(0,len(results)-1,5):
			if results[i+1] == results[i+2]:
				successfulchasers.append(results[i+2])
				# print results[i+2]

		# print successfulchasers

		topchasers = {}
		for i in set(successfulchasers):
			topchasers[i] = successfulchasers.count(i)

		# print topchasers
		AGGTOPCHASERS.append(topchasers)
		# print AGGTOPCHASERS

'''
Return: A list containing teams that have been successful chasing 
targets in IPL History.
'''
def getSuccessfulChasers():	
	# summary
	# prepare unique teams
	teamcollection = []
	teamwins = []
	for seasonsummary in AGGTOPCHASERS:
		for teamname, wins in seasonsummary.iteritems():
			teamcollection.append(teamname)
			teamwins.append(wins)

	successfulteams = list(set(teamcollection))
	# print successfulteams
	return successfulteams

def main():
	# load all time aggregate
	getAllTimeChasingAggregate()
	# get unique successful chasers
	teams = getSuccessfulChasers()

	summary = {}
	# collect total chasing wins across seasons
	for team in teams:
		# print team

		countwins = 0
		for seasonsummary in AGGTOPCHASERS:
			if team in seasonsummary:
				# print seasonsummary[team]
				countwins = countwins + seasonsummary[team]

		summary[team] = countwins

	print "\nTotal successful chases across seasons, grouped by teams: %s" % (summary)

	# total successful chases
	allsuccessfulchases = 0
	for team, totalchases in summary.iteritems():
		allsuccessfulchases = allsuccessfulchases + totalchases

	print "\nTotal Successful Chases in IPL history: %s" % (allsuccessfulchases)


if __name__ == "__main__":
	main()