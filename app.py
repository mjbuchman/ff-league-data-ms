from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv 
import luckBot
import espnData

app = Flask(__name__)
CORS(app)
load_dotenv()
    
@app.route('/getMatchupData', methods = ['GET'])
def getLeagueData():
	startWeek = int(request.args.get('startWeek'))
	endWeek = int(request.args.get('endWeek'))
	year = int(request.args.get('year'))
	return jsonify(espnData.getMatchupData(startWeek, endWeek, year))

@app.route('/runLuckBot', methods = ['GET'])
def runLuckBot():
	currWeek = int(request.args.get('week'))
	currYear = int(request.args.get('year'))
	response = luckBot.runLuckBot(currWeek, currYear)
	return jsonify({"status": response.status})

if __name__ == '__main__':
	app.run()