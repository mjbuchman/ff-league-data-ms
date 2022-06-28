from espn_api.football import League
from dotenv import load_dotenv
import os

load_dotenv()
LEAGUE = os.getenv('LEAGUE_ID')
ESPN_S2 = os.getenv('ESPN_S2')
SWID = os.getenv('SWID')

def getMatchupData(startWeek, endWeek, year):
	matchups = []
	fullWeek = []
	league = League(league_id=LEAGUE, year=year, espn_s2=ESPN_S2, swid=SWID)	
	for week in range(startWeek,endWeek+1):
		for matchup in league.scoreboard(week):
			fullWeek.append({	
      		"week": week,
      		"year": year,
      		"homeTeam": matchup.home_team.owner,
      		"homeScore": str(matchup.home_score),
      		"awayTeam": matchup.away_team.owner,
      		"awayScore": str(matchup.away_score)
        })
		matchups.append(fullWeek)
		fullWeek = []
	return matchups

def getDraftData(year):
	draft = []
	league = League(league_id=LEAGUE, year=year, espn_s2=ESPN_S2, swid=SWID)
	for pick in league.draft:
		player = league.player_info(playerId = pick.playerId)
		gp = 0
		for key in player.stats:
			if(player.stats[key]["breakdown"]):
				gp += 1
		avgPts = round(player.total_points/gp, 2) if gp > 0 else 0
		draftPick = {"year": year, "round": pick.round_num, "pick": pick.round_pick, "name": player.name, "team": player.proTeam, "position": player.position, "owner": pick.team.owner, "prk": player.posRank, "gp": gp, "fptsg": avgPts, "fpts": player.total_points}
		draft.append(draftPick)
	return draft