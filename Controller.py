
import Player
import Board
import Location
reload(Player)

CONST_DEFAULT_NUM_PLAYERS = 2
CONST_ROBBER = 7

def main():
	board = Board.board()
	print "hello world"
	numPlayers = 0
	#sublime text can't work with stdin, so hardcoded it as a 2 player game while on sublime
	try:
		numPlayers = input('How many players do you want? ')
	except EOFError:
		numPlayers = CONST_DEFAULT_NUM_PLAYERS
		print  ""
	players = []
	for i in range (0, numPlayers):
		players.append(Player.player())
	firstPlacement(numPlayers, players, board)
	playMainGame(numPlayers, players, board)

def playMainGame(numPlayers, players, board):
	turnCounter = 0
	while (True):
		gameEnd = playTurn(turnCounter % numPlayers, players, board)
		#remove the turnCounter>= 10 when full implementation
		if gameEnd or turnCounter >= 10:
			break
		turnCounter += 1

def playTurn(curPlayer, players, board):
	print  "Player " + str(curPlayer) + " turn"
	askPlayerIfDevCard(curPlayer, players, board)
	diceRoll = board.rollDice()
	if diceRoll is CONST_ROBBER:
		handleRobber(curPlayer, players, board)
	else:
		print str(diceRoll) + " was rolled"
		board.assignResources(diceRoll)
	trade(curPlayer, players, board)
	build(curPlayer, players, board)
	return players[curPlayer].hasWon()

def build(curPlayer, players, board):
	print "Player " + str(curPlayer) + " is building"
	while(True):
		try:
			response = raw_input("Do you want to build?")
			if  response == "Yes" or response == "yes" or response == "y":
				toBuild = raw_input("What do you want to build? ")
				if toBuild == "road":
					buildRoad(curPlayer, players, board)
				elif toBuild == "settlement":
					buildSettlement(curPlayer, players, board)
				elif toBuild == "city":
					buildCity(curPlayer, players, board)
				elif toBuild == "devCard":
					buildDevCard(curPlayer, players, board)
			else:
				break
		except EOFError:
			print " Not building, on sublime"
			break

def handleRobber(curPlayer, players, board):
	print "Robber"
	locations = board.getAllTiles()
	print "Choose a location: "
	for l in locations:
		print l
	locationForRobber = 0
	try:
		locationForRobber = raw_input("")
	except EOFError:
		locationForRobber = Location.Tile()
		print  ""
	board.moveRobber(locationForRobber)
	targets = board.playersToStealFrom(locationForRobber)
	print "Choose a player to steal from:"
	for t in targets:
		print t
	target = 0
	try:
		target = raw_input("")
	except EOFError:
		target = 0
		print  ""
	steal(target, curPlayer)

def askPlayerIfDevCard(curPlayer, players, board):
	useCard = 0
	try:
		useCard = raw_input("Do you want to play a dev card?")
		if useCard == "Yes" or useCard == "yes" or useCard == "y":
			if players[curPlayer].canPlayDevCard():
				potentialDevCards = player.getDevCards
				chosenCard = selectDevCard(potentialDevCards)
				useCard(curPlayer, players, board, chosenCard)
			else:
				print "You can't play a dev card"
	except EOFError:
		print "Not doing dev card, sublime"
	return 0

def steal(target, curPlayer):
	stolen = target.getRandomCard()
	curPlayer.addResource(stolen, 1)

def buildRoad(curPlayer, players, board):
	if players[curPlayer].canBuildRoad():
		roadLocations = board.getPotentialRoadLocs(curPlayer, players)
		roadLocation = askPlayerForRoadLocation()
		players[curPlayer].buildRoad()
		board.buildRoad(curPlayer, players, roadLocation)
	else:
		print "You can't build a road"

def buildSettlement(curPlayer, players, board):
	if players[curPlayer].canBuildSettlement():
		settlementLocations = board.getPotentialSettlementLocs(curPlayer, players)
		settlementLocation = askPlayerForSettlementLocation()
		players[curPlayer].buildSettlement()
		board.buildSettlement(curPlayer, players, settlementLocation)
	else:
		print "You can't build a settlement"

def buildCity(curPlayer, players, board):
	if players[curPlayer].canBuildCity():
		cityLocations = board.getPotentialCityLocs(curPlayer, players)
		cityLocation = askPlayerForCityLocation()
		players[curPlayer].buildCity()
		board.buildCity(curPlayer, players, cityLocation)
	else:
		print "You can't build a city"

def buildDevCard(curPlayer, players, board):
	if players[curPlayer].canBuildDevCard():
		players[curPlayer].buildDevCard()
	else:
		print "You can't build a dev card"

def firstPlacement(numPlayers, players, board):
	for i in range (0, numPlayers):
		board.initialPlacement(i, players)
	for i in range(numPlayers, 0, -1):
	 	board.initialPlacement(i-1, players)

def selectDevCard(potentialDevCards):
	return 0

def useCard(curPlayer, chosenCard):
	return 0

def askPlayerForRoadLocation():
	return 0

def askPlayerForSettlementLocation():
	return 0

def askPlayerForCityLocation():
	return 0

def trade(curPlayer, players, board):
	print "Trading phase"

main()