from espn_api.football import League
from dotenv import load_dotenv
import os

load_dotenv()
LEAGUE = os.getenv('LEAGUE_ID')
ESPN_S2 = os.getenv('ESPN_S2')
SWID = os.getenv('SWID')

def getMatchupData(startWeek, endWeek, year):
	matchups = {}
	league = League(league_id=LEAGUE, year=year, espn_s2=ESPN_S2, swid=SWID)	
	for week in range(startWeek,endWeek):
		for matchup in league.scoreboard(week):
			matchups[week].append({	
      		"homeTeam": matchup.home_team.owner,
      		"homeScore": str(matchup.home_score),
      		"awayTeam": matchup.away_team.owner,
      		"awayScore": str(matchup.away_score)
        })
	return matchups