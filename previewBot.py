from espn_api.football import League
from tabulate import tabulate
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
import os
import requests

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

def sendMessage(preview):
    webhook = DiscordWebhook(url=WEBHOOK, content=f"`{preview}`")
    return webhook.execute()

def getPreview(owner1, owner2):
    overview = requests.get(f"http://localhost:3000/getH2HOverview/{owner1}/{owner2}")
    overview = overview.json()
    data = [
        ["Wins", overview["o1Data"]["wins"], overview["o2Data"]["wins"]],
        ["Points", overview["o1Data"]["points"], overview["o2Data"]["points"]],
        ["Avg", overview["o1Data"]["avgPFSW"], overview["o2Data"]["avgPFSW"]],
        ["High", overview["o1Data"]["hssw"]["score"], overview["o2Data"]["hssw"]["score"]],
        ["Low", overview["o1Data"]["lssw"]["score"], overview["o2Data"]["lssw"]["score"]],
        ["High MOV", overview["o1Data"]["maxMOV"]["val"], overview["o2Data"]["maxMOV"]["val"]],
        ["Low MOV", overview["o1Data"]["minMOV"]["val"], overview["o2Data"]["minMOV"]["val"]]
        ]
    return tabulate(data, headers=['', owner1.split(' ', 1)[0], owner2.split(' ', 1)[0]], tablefmt="rst", stralign="left", floatfmt=".2f")

def runPreviewBot(currYear):
    league = League(league_id=LEAGUE, year=currYear, espn_s2=ESPN_S2, swid=SWID)
    webhook = DiscordWebhook(url=WEBHOOK, content="Upcoming Matchup Previews:")
    webhook.execute()
    previews = []
    for matchup in league.scoreboard():
        sendMessage(getPreview(UserMap[matchup.home_team.owners[0]], UserMap[matchup.away_team.owners[0]]))
    webhook = DiscordWebhook(url=WEBHOOK, content="For more details visit the [WFFL H2H Page](http://www.wallersteinffl.com/#/h2h)")
    webhook.execute()
    return "yay"