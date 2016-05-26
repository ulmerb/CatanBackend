from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import Controller
import Player
import Board
import Location
import Devcards
import Ai
import ASCII.catan_ascii_functions as asc

@csrf_exempt
def djangotest(request):
	# z = json.loads(request.POST['js_resp'])
	# print z['action']
	# return HttpResponse("Hello")
	print request.POST
	# return HttpResponse(
	# json.dumps({
 #  "numPlayers": "2",
 #  "currentPlayer": "1",
 #  "message": "cannot buy devcard",
 #  "robberTileLocation": "04T","players": [
 #  	{
 #  	"hasLongestRoad": True,
 #  	"hasLargestArmy": False,
 #  	"victoryPoints": "1",
 #  	}
 #  ]})
	# )

	return HttpResponse(
		json.dumps(
	{
	  "numPlayers": "2",
	  "currentPlayer": "1",
	  "message": "cannot buy devcard",
	  "robberTileLocation": "04T",
	  "players": [
	    {
	      "hasLongestRoad": True,
	      "hasLargestArmy": False,
	      "victoryPoints": "1",
	      "resources": {
	        "wood": "1",
	        "brick": "2",
	        "grain": "3",
	        "sheep": "0",
	        "ore": "1"
	      },
	      "devCards": {
	        "yearOfPlenty": "1",
	        "roadBuilding": "0",
	        "knight": "0",
	        "monopoly": "0",
	        "victoryPoint": "0"
	      },
	      "ports": [
	        "1"
	      ]
	    },
	    {
	      "hasLongestRoad": False,
	      "hasLargestArmy": True,
	      "victoryPoints": "1",
	      "resources": {
	        "wood": "1",
	        "brick": "0",
	        "grain": "0",
	        "sheep": "0",
	        "ore": "1"
	      },
	      "devCards": {
	        "yearOfPlenty": "0",
	        "roadBuilding": "1",
	        "knight": "0",
	        "monopoly": "1",
	        "victoryPoint": "0"
	      },
	      "ports": [
	        "1"
	      ]
	    }
	   ],
		  "board": {
		    "cities": [
		      "07V",
		      "18V"
		    ],
		    "roads": [
		      "21R",
		      "13R"
		    ],
		    "settlements": [
		      "42V"
		    ]
		  }
	   })
	)

def initialJsonify(board, players):
	data = {}
	data['numPlayers'] = len(players)
	data['currentPlayer'] = 0
	data["robberTileLocation"] = board.tileToAscii[board.robberTile]
	data["players"] = []
	print players
	for p in players:
		# These should all be 0, but for validations sake,
		# I'm filling them in using properties
		pInfo = {"victoryPoints":p.score}
		pInfo['resources'] = p.resources
		pInfo["devCards"] = {}
		for card in p.devCardsHeld:
			if card in pInfo["devCards"]:
				pInfo["devCards"][card] += 1
			else:
				pInfo["devCards"][card] = 1
		# stubs to be updated
		pInfo["hasLongestRoad"] = False
		pInfo["hasLongestArmy"] = False
		for key in p.structures:
			pInfo[key] = p.structures[key]
		data["players"].append(pInfo)

	return json.dumps(data) 
	# return "yayo"

# Intialize game
@csrf_exempt
def initialize(request):
	info = json.loads(request.POST['js_resp'])
	numPlayers = info['numPlayers']
	AI = info['AI']
	board, players = Controller.tileInitialization(numPlayers, AI)
	# convert board, players, newNum into json response
	resp = initialJsonify(board, players)
	return HttpResponse(resp)

@csrf_exempt
def build(request):
	pass

