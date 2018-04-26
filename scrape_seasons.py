#!/usr/bin/env python
# Author: Pradeep Sivakumar
# Task: Publish successful chases in IPL history.
# encoding=utf8

# standard libraries
import urllib2
import re
import json
import datetime
import sys

# 3rd party library
from BeautifulSoup import BeautifulSoup
import pandas as pd
import numpy as np

# Globals
SEASONS = ["http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2007/08;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2009;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2009/10;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2011;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2012;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2013;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2014;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2015;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2016;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2017;trophy=117;type=season",
"http://stats.espncricinfo.com/indian-premier-league-2013/engine/records/team/match_results.html?class=;id=2018;trophy=117;type=season"]
AGGTOPCHASERS = []
AGGTOPFAILURES = []

def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
		'''
		Call in a loop to create terminal progress bar
		@params:
				iteration   - Required  : current iteration (Int)
				total       - Required  : total iterations (Int)
				prefix      - Optional  : prefix string (Str)
				suffix      - Optional  : suffix string (Str)
				decimals    - Optional  : positive number of decimals in percent complete (Int)
				length      - Optional  : character length of bar (Int)
				fill        - Optional  : bar fill character (Str)

		Source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console    
		'''
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print'\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
		sys.stdout.flush()
		# Print New Line on Complete                                                                                                                                                                                                              
		if iteration == total:
				print

def is_season_current(seasonYear):
	''' Returns True if passed season-year is current.
	'''
	now = datetime.datetime.now()
	this_year = now.year

	if str(this_year) == seasonYear:
		return True

	return False

def scrape_and_cache(seasonURL, seasonYear, cachename):
	''' Called only if there is no local data cache, so invoke URL, scrape and 
	cache the data for future use.

	Caching improves performance by 99%.
	> No cache (fetch from URL every time): 11694 ms.
	> With cache (json): 105ms.

	Caching benchmark with pickle, also improves by 99%.
	> No cache (fetch from URL every time): 11451 ms.
	> With cache (json): 110ms. 
	But pickle is not secure and is not human-readable.
	'''
	page = urllib2.urlopen(seasonURL)
	soup = BeautifulSoup(page)

	results = []
	games = soup.findAll("tr","data1")
	for game in games:
		for attribute in game.findAll("td"):
			if attribute.renderContents() == "abandoned" or attribute.renderContents() == "tied" or attribute.renderContents() == "no result":
				results.append("null")
			else:
				for column in attribute.findAll("a","data-link"):
					columndata = column.renderContents()
					results.append(columndata)
	
	json.dump(results, open(cachename,'w'))

def get_alltime_chasing_aggregate():
	'''
	Prepare a dictionary for each season, collecting total successful 
	chases by each team.

	Load a global list of dictionaries, thus collecting data across seasons.
	'''
	total_seasons = len(SEASONS)
	count_seasons = 0
	print_progress_bar(count_seasons, total_seasons, prefix = 'Progress:', suffix = 'Complete', length = 50)

	for seasonURL in SEASONS:
		count_seasons = count_seasons + 1
		# "seasonURL" is the complete URL for a given season
		# "seasonYear" is the 4-digit year in the URL
		seasonYear = seasonURL.split(';id=')[1].split(';')[0]
		if '/' in seasonYear:
			seasonYear = seasonYear[:2] + seasonYear[5:]
		
		# read data from cache, if available, else fetch data over network and cache
		cachename = "data/results" + seasonYear + ".json" 
		try:
			results = json.load(open(cachename,'r'))
		except (OSError, IOError) as e:
			scrape_and_cache(seasonURL, seasonYear, cachename)
			results = json.load(open(cachename,'r'))

		print_progress_bar(count_seasons, total_seasons, prefix = 'Progress:', suffix = 'Complete', length = 50)
		
		successfulchasers = []
		unsuccessfulchasers = []
		
		# "results" list is just one contiguous collection of data, at this point.
		# so, consider each 5-element chunk as one data row and operate upon it.
		for i in xrange(0,len(results)-1,5):
			if results[i+1] == results[i+2]:
				successfulchasers.append(results[i+2])
				# print results[i+2]
			elif results[i+0] == results[i+2]:
				unsuccessfulchasers.append(results[i+1])

		# print "success: " + ",".join(successfulchasers)
		# print "failures: " + ",".join(unsuccessfulchasers)

		topchasers = {}
		topfailures = {}
		for i in set(successfulchasers):
			topchasers[i] = successfulchasers.count(i)

		# print topchasers

		for j in set(unsuccessfulchasers):
			topfailures[j] = unsuccessfulchasers.count(j)

		# print topfailures

		AGGTOPCHASERS.append(topchasers)
		# print AGGTOPCHASERS
		AGGTOPFAILURES.append(topfailures)
		# print AGGTOPFAILURES

def get_all_chasers():	
	'''
	Return: A list containing teams that have chased targets in IPL History.
	'''
	# summary
	# prepare unique teams
	teamcollection = []
	teamwins = []
	teamlosses = []
	for seasonsummary in AGGTOPCHASERS:
		for teamname, wins in seasonsummary.iteritems():
			teamcollection.append(teamname)
			teamwins.append(wins)

	for seasonsummary in AGGTOPFAILURES:
		for teamname, losses in seasonsummary.iteritems():
			teamcollection.append(teamname)
			teamlosses.append(losses)

	teams = list(set(teamcollection))
	# print teams
	return teams

def main():
	# load all time aggregate
	get_alltime_chasing_aggregate()
	# get unique successful chasers
	teams = get_all_chasers()

	summary = {}
	# collect total chasing wins across seasons
	iplTotalSuccessfulChases = 0
	ipl_total_chases = 0
	for team in teams:
		# print team

		team_total_wins = 0
		team_total_losses = 0
		for seasonsummary in AGGTOPCHASERS:
			if team in seasonsummary:
				# print seasonsummary[team]
				team_total_wins = team_total_wins + seasonsummary[team]

		for seasonsummary in AGGTOPFAILURES:
			if team in seasonsummary:
				# print seasonsummary[team]
				team_total_losses = team_total_losses + seasonsummary[team]

		team_total_chases = team_total_wins + team_total_losses
		winpercentage = float(team_total_wins)/float(team_total_chases)

		ipl_total_chases = ipl_total_chases + team_total_chases
		iplTotalSuccessfulChases = iplTotalSuccessfulChases + team_total_wins

		datarow = []
		datarow.append(team_total_wins)
		datarow.append(team_total_losses)
		datarow.append(team_total_chases)
		datarow.append(winpercentage)
		summary[team] = datarow

	print "\nChasing record of IPL Teams: \n"
	
	# load DataFrame
	df = pd.DataFrame(summary)
	df = df.transpose()
	df.columns = ['wins', 'losses', 'total', 'wp']
	
	# format data
	cols_to_format = ['wins', 'losses', 'total']
	df[cols_to_format] = df[cols_to_format].applymap(np.int64)
	df['wp'] = pd.Series(["{0:.2f}%".format(val*100) for val in df['wp']], index = df.index)

	# sort
	df.sort_values(by='wp', ascending=False, inplace=True)
	print df

	print "\nRemoving outliers: \n"
	print df.loc[df['total'] >= 25]

	# total successful chases
	chasePercentage = float(iplTotalSuccessfulChases)/float(ipl_total_chases)
	formattedChasePercentage = "{:.1%}".format(chasePercentage)
	print "\nTotal Successful Chases in IPL history: %s (out of %s total chases), a %s success rate option." % (iplTotalSuccessfulChases,ipl_total_chases,formattedChasePercentage)	

if __name__ == "__main__":
	main()