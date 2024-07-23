from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv 
import luckBot
import espnData
import previewBot

app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/')
def index():
	return render_template("index.html")
    
@app.route('/getMatchupData', methods = ['GET'])
def getLeagueData():
	startWeek = int(request.args.get('startWeek'))
	endWeek = int(request.args.get('endWeek'))
	year = int(request.args.get('year'))
	return jsonify(espnData.getMatchupData(startWeek, endWeek, year))

@app.route('/getDraftData', methods = ['GET'])
def getDraftData():
	year = int(request.args.get('year'))
	return jsonify(espnData.getDraftData(year))

@app.route('/runLuckBot', methods = ['GET'])
def runLuckBot():
	currWeek = int(request.args.get('week'))
	currYear = int(request.args.get('year'))
	response = luckBot.runLuckBot(currWeek, currYear)
	return response.json()

@app.route('/runPreviewBot', methods = ['GET'])
def runPreviewBot():
	currYear = int(request.args.get('year'))
	response = previewBot.runPreviewBot(currYear)
	return response

if __name__ == '__main__':
	app.run()