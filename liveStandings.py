import espnData

standings = {
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
    result = {}
    matchups = espnData.getMatchupData(12,12,2024)
    for matchup in matchups[0]:
        standings[matchup["homeTeam"]]["pf"] += float(matchup["homeScore"])
        standings[matchup["awayTeam"]]["pf"] += float(matchup["awayScore"])

        if (float(matchup["homeScore"]) > float(matchup["awayScore"])):
            standings[matchup["homeTeam"]]["wins"] += 1
        elif (float(matchup["homeScore"]) < float(matchup["awayScore"])):
            standings[matchup["awayTeam"]]["wins"] += 1
    order = sorted(standings, key=lambda x: (standings[x]['wins'], standings[x]['pf']), reverse=True)
    
    for item in order: 
        result.update({item : standings[item]})
    return result