from espn_api.football import League
from tabulate import tabulate
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
import os

load_dotenv()
LEAGUE = os.getenv('LEAGUE_ID')
ESPN_S2 = os.getenv('ESPN_S2')
SWID = os.getenv('SWID')
WEBHOOK = os.getenv('WEBHOOK')
UserMap = {
	"{AEB27B68-FF30-4525-B27B-68FF3065252B}" : "Connor DeYoung",
	"{9CDAE063-F1E8-4260-B2D9-F457E5214403}" : "Michael Buchman",
	"{EE721424-BE30-499F-A4FA-80556D6673A9}" : "Tyler Brown",
	"{CAE1C5DD-16B2-4B40-A1C5-DD16B29B408B}" : "Joe Perry",
	"{755075D4-4A7D-45E4-BDA3-36711D6B7E6A}" : "Brenden Zarrinnam",
	"{497BB1CE-AAE3-473A-BBB1-CEAAE3573AA9}" : "Nick Eufrasio",
	"{CE187872-D2A1-4B1E-B956-C753D364EA2C}" : "Ryan Rasmussen",
	"{FB25C07D-400B-4EAD-9BDD-098A21B55A92}" : "Grant Dakovich",
	"{69AE30CE-F82D-4957-B3B8-18C2993951D8}" : "James Earley",
	"{C9C2DA15-183C-42F6-B8B4-A6D7D24FC592}" : "Jonathan Setzke"
}

def sendMessage(currWeek, data):
	message = f"Here's the Luckiness Factor through Week {currWeek-1}:\n`" + data + "`"
	webhook = DiscordWebhook(url=WEBHOOK, content=message)
	return webhook.execute()
 
def runLuckBot(currWeek, currYear):
	league = League(league_id=LEAGUE, year=currYear, espn_s2=ESPN_S2, swid=SWID)

	actualWins = {}
	expectedWins = {}
	for team in league.teams:
		currOwner = UserMap[team.owners[0]]
		actualWins[currOwner] = 0
		expectedWins[currOwner] = 0
		
	scores = {}
	for x in range(1,currWeek):
		for matchup in league.scoreboard(x):
			homeTeam = UserMap[matchup.home_team.owners[0]]
			awayTeam = UserMap[matchup.away_team.owners[0]]
			scores[homeTeam] = matchup.home_score
			scores[awayTeam] = matchup.away_score
			if (matchup.home_score > matchup.away_score): actualWins[homeTeam] += 1
			elif (matchup.home_score < matchup.away_score): actualWins[awayTeam] += 1
			else:
				actualWins[homeTeam] += .5
				actualWins[awayTeam] += .5
    
		sortedScores = dict(sorted(scores.items(), key = lambda x: x[1]))
		
		keysList = list(sortedScores)
		for y in range(len(sortedScores)):
			expectedWins[keysList[y]] = expectedWins[keysList[y]] + y
		
		scores = {}

	output = []
	for team in league.teams:
		currOwner = UserMap[team.owners[0]]
		output.append([
    	currOwner.split(' ', 1)[0],
     	actualWins[currOwner],
      expectedWins[currOwner]/9,
      actualWins[currOwner] - expectedWins[currOwner]/9
    ])

	sortedOutput = sorted(output, key=lambda x: x[3], reverse=True)
	data = tabulate(sortedOutput, headers=['Team', 'Act.', 'Exp.', 'Luck'], tablefmt="rst", stralign="left", floatfmt=".3f")
	return sendMessage(currWeek, data)