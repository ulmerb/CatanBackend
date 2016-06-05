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
import settings
import Devcards

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

	# return HttpResponse(
	# 	json.dumps(
	# {
	#   "numPlayers": "2",
	#   "currentPlayer": "1",
	#   "message": "cannot buy devcard",
	#   "robberTileLocation": "04T",
	#   "players": [
	#     {
	#       "hasLongestRoad": True,
	#       "hasLargestArmy": False,
	#       "victoryPoints": "1",
	#       "resources": {
	#         "wood": "1",
	#         "brick": "2",
	#         "grain": "3",
	#         "sheep": "0",
	#         "ore": "1"
	#       },
	#       "devCards": {
	#         "yearOfPlenty": "1",
	#         "roadBuilding": "0",
	#         "knight": "0",
	#         "monopoly": "0",
	#         "victoryPoint": "0"
	#       },
	#       "ports": [
	#         "1"
	#       ]
	#     },
	#     {
	#       "hasLongestRoad": False,
	#       "hasLargestArmy": True,
	#       "victoryPoints": "1",
	#       "resources": {
	#         "wood": "1",
	#         "brick": "0",
	#         "grain": "0",
	#         "sheep": "0",
	#         "ore": "1"
	#       },
	#       "devCards": {
	#         "yearOfPlenty": "0",
	#         "roadBuilding": "1",
	#         "knight": "0",
	#         "monopoly": "1",
	#         "victoryPoint": "0"
	#       },
	#       "ports": [
	#         "1"
	#       ]
	#     }
	#    ],
	# 	  "board": {
	# 	    "cities": [
	# 	      "07V",
	# 	      "18V"
	# 	    ],
	# 	    "roads": [
	# 	      "21R",
	# 	      "13R"
	# 	    ],
	# 	    "settlements": [
	# 	      "42V"
	# 	    ]
	# 	  }
	#    })
	# )



	#used for testing (from the new gameState2):
	return HttpResponse(
		json.dumps(
	{
	  "numPlayers": "2",
	  "currentPlayer": "1",
	  "message": "cannot buy devcard",
	  "robberTileLocation": "04T",
	  "currentDiceRoll":"4",
	  "boardText": "the actual ascii board",
	  "players": [
	    {
	      "hasLongestRoad": True,
	      "hasLargestArmy": False,
	      "victoryPoints": "1",
	      "knightsPlayed": "1",
      	  "lengthOfLongestRoad": "2",
      	  "victoryPointCardsPlayed": "1",
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
	      ],
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
	    },
	    {
	      "hasLongestRoad": False,
	      "hasLargestArmy": True,
	      "victoryPoints": "1",
	      "knightsPlayed": "3",
      	  "lengthOfLongestRoad": "1",
          "victoryPointCardsPlayed": "0",
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
	        "2"
	      ],
	      "cities": [
		      "09V",
		      "20V"
		    ],
		    "roads": [
		      "22R",
		      "14R"
		    ],
		    "settlements": [
		      "44V"
		    ]
	    }
	]
	   })
	)

def makeJson(board, players, message, diceRoll=0, curPlayer=0, card=0):
	data = {}
	data['message'] = message
	data['currentDiceRoll'] = diceRoll
	data['numPlayers'] = len(players)
	data['currentPlayer'] = curPlayer
	data["robberTileLocation"] = board.tileToAscii[board.robberTile]
	data["players"] = []
	data["boardString"] = board.printBoard()
	for p in players:
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
	data['devCardName'] = card
	return json.dumps(data)

# Intialize game
@csrf_exempt
def newGame(request):
	info = json.loads(request.POST['js_resp'])
	numPlayers = info['numPlayers']
	AI = info['AI']
	board, players = Controller.tileInitialization(numPlayers, AI)
	settings.BOARD = board
	settings.PLAYERS = players
	settings.DEVCARDS = Devcards.devcards()
	# convert board, players, newNum into json response
	resp = makeJson(board, players, "Player 0, place your first settlement")
	return HttpResponse(resp)

@csrf_exempt
def build(request):
	pass

@csrf_exempt
def endOfTurn(request):
	info = json.loads(request.POST['js_resp'])
	print info['currentPlayer']
	newCurPlayer = int(info['currentPlayer'] + 1) % len(settings.PLAYERS)
	dRoll = Controller.rollDice(settings.BOARD, settings.PLAYERS, newCurPlayer, -1)
	if dRoll == 7:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "Robber!", dRoll, newCurPlayer)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "not robber", dRoll, newCurPlayer)
	return HttpResponse(resp)

@csrf_exempt
def placeRobber(request):
	info = json.loads(request.POST['js_resp'])
	loc = int(info['tilePosition'])
	target = int(info['playerToStealFrom'])
	curPlayer = int(info['currentPlayer'])
	print "old board number", settings.BOARD.currentBoardNumber
	error = Controller.serverHandleRobber(curPlayer, settings.PLAYERS, loc, target, settings.BOARD, -1)
	print "new board number", settings.BOARD.currentBoardNumber
	# print settings.BOARD.printBoard()
	if error:
		resp = makeJson(settings.BOARD, settings.PLAYERS, error, 7, curPlayer)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " + str(curPlayer) + "'s turn", 7, curPlayer)
	return HttpResponse(resp)


@csrf_exempt
def buildRoad(request):
	info = json.loads(request.POST['js_resp'])
	suggestedLocation = info['suggestedLocation']
	curPlayer = info['curPlayer']
	error = Controller.serverBuildRoad(curPlayer, settings.PLAYERS, settings.BOARD, suggestedLocation)
	if error:
		resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "road build successfull", 0, curPlayer)

	return HttpResponse(resp)
@csrf_exempt
def buildSettlement(request):
	info = json.loads(request.POST['js_resp'])
	suggestedLocation = info['suggestedLocation']
	curPlayer = info['curPlayer']
	error = Controller.serverBuildSettlement(curPlayer, settings.PLAYERS, settings.BOARD, suggestedLocation)
	if error:
		resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "settlement build successfull", 0, curPlayer)

	return HttpResponse(resp)

@csrf_exempt
def buildCity(request):
	info = json.loads(request.POST['js_resp'])
	suggestedLocation = info['suggestedLocation']
	curPlayer = info['curPlayer']
	error = Controller.serverBuildCity(curPlayer, settings.PLAYERS, settings.BOARD, suggestedLocation)
	if error:
		resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "city build successfull", 0, curPlayer)

	return HttpResponse(resp)

@csrf_exempt
def buyCard(request):
	info = json.loads(request.POST['js_resp'])
	curPlayer = info['curPlayer']
	error, card = settings.PLAYERS[curPlayer].buildDevCard(settings.DEVCARDS)
	if error:
		resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer, card)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "succesfully bought devcard", 0, curPlayer, card)
	
	return HttpResponse(resp)

@csrf_exempt
def playCard(request):
	info = json.loads(request.POST['js_resp'])
	cardType = info['devCardType']
	curPlayer = info['curPlayer']
	devCardBrick = info['devCardBrick']
	devCardWood = info['devCardWood']
	devCardSheep = info['devCardSheep']
	devCardOre = info['devCardOre']
	devCardGrain = info['devCardGrain']
	roadLoc1 = info['roadLoc1']
	roadLoc2 = info['roadLoc2']
	error = Controller.serverUseCard(curPlayer, settings.PLAYERS, settings.BOARD, cardType,
		devCardBrick, devCardWood, devCardSheep, devCardOre, devCardGrain, roadLoc1, roadLoc2)
	if error:
		resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
	else:
		resp = makeJson(settings.BOARD, settings.PLAYERS, "Devcard played", 0, curPlayer)

	return HttpResponse(resp)
