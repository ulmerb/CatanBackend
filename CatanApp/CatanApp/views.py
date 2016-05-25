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

# Intialize unique game
@csrf_exempt
def initialize(request):
	info = json.loads(request.POST['js_resp'])
	numPlayers = info['numPlayers']
	AI = info['AI']
	board, players, newNumPlayers = Controller.tileInitialization(numPlayers, AI)
	# convert board, players, newNum into json response
	print board, players, newNumPlayers
	return HttpResponse("initialize in progress")

@csrf_exempt
def build(request):
	pass

