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

def sendMessage(currWeek, data):
	message = f"Here's the Luckiness Factor through Week {currWeek-1}:\n`" + data + "`"
	webhook = DiscordWebhook(url=WEBHOOK, content=message)
	return webhook.execute()
 
def runLuckBot(currWeek, currYear):
	league = League(league_id=LEAGUE, year=currYear, espn_s2=ESPN_S2, swid=SWID)

	actualWins = {}
	expectedWins = {}
	for team in league.teams:
		actualWins[team.owner] = 0
		expectedWins[team.owner] = 0
		
	scores = {}
	for x in range(1,currWeek):
		for matchup in league.scoreboard(x):
			scores[matchup.home_team.owner] = matchup.home_score
			scores[matchup.away_team.owner] = matchup.away_score
			if (matchup.home_score > matchup.away_score): actualWins[matchup.home_team.owner] += 1
			elif (matchup.home_score < matchup.away_score): actualWins[matchup.away_team.owner] += 1
			else:
				actualWins[matchup.home_team.owner] += .5
				actualWins[matchup.away_team.owner] += .5
    
		sortedScores = dict(sorted(scores.items(), key = lambda x: x[1]))
		
		keysList = list(sortedScores)
		for y in range(len(sortedScores)):
			expectedWins[keysList[y]] = expectedWins[keysList[y]] + y
		
		scores = {}

	output = []
	for team in league.teams:
		output.append([
    	team.owner.split(' ', 1)[0],
     	actualWins[team.owner],
      expectedWins[team.owner]/9,
      actualWins[team.owner] - expectedWins[team.owner]/9
    ])

	sortedOutput = sorted(output, key=lambda x: x[3], reverse=True)
	data = tabulate(sortedOutput, headers=['Team', 'Act.', 'Exp.', 'Luck'], tablefmt="rst", stralign="left", floatfmt=".3f")
	return sendMessage(currWeek, data)