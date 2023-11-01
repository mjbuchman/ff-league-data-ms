# from espn_api.football import League
# from tabulate import tabulate
# from dotenv import load_dotenv
# from discord_webhook import DiscordWebhook
# import os

# load_dotenv()
# LEAGUE = os.getenv('LEAGUE_ID')
# ESPN_S2 = os.getenv('ESPN_S2')
# SWID = os.getenv('SWID')
# WEBHOOK = os.getenv('WEBHOOK')

# def sendMessage(currWeek, data):
# 	message = f"Here's the Luckiness Factor through Week {currWeek-1}:\n`" + data + "`"
# 	webhook = DiscordWebhook(url=WEBHOOK, content=message)
# 	return webhook.execute()

# def getPreview(owner1, owner2): 
    
# def runPreviewBot(currYear):
# 	league = League(league_id=LEAGUE, year=currYear, espn_s2=ESPN_S2, swid=SWID)
#     for matchup in league.scoreboard():
#         sendMessage(getPreview(matchup.home_team.owner, matchup.away_team.owner)) 

# 	return sendMessage(currWeek, data)