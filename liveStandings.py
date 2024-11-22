from espn_api.football import League
from dotenv import load_dotenv
import os

load_dotenv()
LEAGUE = os.getenv('LEAGUE_ID')
ESPN_S2 = os.getenv('ESPN_S2')
SWID = os.getenv('SWID')

base_standings = {
    "Grant Dakovich": {
        "wins": 6,
        "pf": 1531.38
    },
    "Michael Buchman": {
        "wins": 6,
        "pf": 1446.18
    },
    "Brenden Zarrinnam": {
        "wins": 5,
        "pf": 1483.06
    },
    "Ryan Rasmussen": {
        "wins": 5,
        "pf": 1317.9
    },
    "Jonathan Setzke": {
        "wins": 5,
        "pf": 1547.24
    },
    "James Earley": {
        "wins": 5,
        "pf": 1327.92
    },
    "Joe Perry": {
        "wins": 4,
        "pf": 1404.69
    },
    "Tyler Brown": {
        "wins": 7,
        "pf": 1482.82
    },
    "Nick Eufrasio": {
        "wins": 8,
        "pf": 1583.29
    },
    "Connor DeYoung": {
        "wins": 4,
        "pf": 1363.64
    },
}
def calculateStandings():
    standings = base_standings
    result = {}
    league = League(league_id=LEAGUE, year=2024, espn_s2=ESPN_S2, swid=SWID)	
    for matchup in league.box_scores(12):
        homeTeam = matchup.home_team.owners[0]["firstName"] + " " + matchup.home_team.owners[0]["lastName"]
        awayTeam = matchup.away_team.owners[0]["firstName"] + " " + matchup.away_team.owners[0]["lastName"]

        standings[homeTeam]["pf"] += float(matchup.home_score)
        standings[awayTeam]["pf"] += float(matchup.away_score)

        if (float(matchup.home_score) > float(matchup.away_score)):
            standings[homeTeam]["wins"] += 1
        elif (float(matchup.home_score) < float(matchup.away_score)):
            standings[awayTeam]["wins"] += 1

    order = sorted(standings, key=lambda x: (standings[x]['wins'], standings[x]['pf']), reverse=True)
    
    for item in order: 
        result.update({item : standings[item]})
    return result