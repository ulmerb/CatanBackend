import Player
import Board
import Location
import Devcards
import Ai
import sys
import ASCII.catan_ascii_functions as asc
reload(Player)
reload(Board)
reload(Ai)

CONST_DEFAULT_NUM_PLAYERS = 2

CONST_ROBBER = 7

def main():
	board = Board.board()
	devCardsDeck = Devcards.devcards()
	numPlayers = 0
	#test Ben
	#sublime text can't work with stdin, so hardcoded it as a 2 player game while on sublime
	try:
		numPlayers = input('How many players do you want? ')
	except EOFError:
		numPlayers = CONST_DEFAULT_NUM_PLAYERS
		print  ""
	players = []
	for i in range (0, numPlayers):
		players.append(Player.player(i))
	# players[0].addResource("wood",10)
	# players[0].addResource("ore",10)
	# players[0].addResource("grain",10)
	# players[0].addResource("sheep",10)
	# players[0].buildDevCard(devCardsDeck)
	# print players[0].devCardsHeld
	# print devCardsDeck.getNumDevCards()
	AiNum = -1
	try:
            response = raw_input("Add an Ai player?")
            if response == "Yes" or response == "yes" or response == "y":
                AiNum = len(players)			
                players.append(Ai.ai(AiNum))
                numPlayers +=1
	except EOFError:
		print " Not building, on sublime"
	board.createBatchCSV(players)
	board.batchUpdate()
	board.printBoard()
	firstPlacement(numPlayers, players, board, AiNum)
	playMainGame(numPlayers, players, board, AiNum)

def playMainGame(numPlayers, players, board, AiNum = -1):
	turnCounter = 0
	while (True):
	        curPlayer = turnCounter % numPlayers
	        isAi = False
	        if (curPlayer == AiNum):
	            isAi = True
	        if (isAi):
	            diceRoll = board.rollDice()
	            if diceRoll is CONST_ROBBER:
		        handleRobber(curPlayer, players, board, AiNum)
		    else:
		        board.assignResources(diceRoll, players)
	            gameEnd = players[AiNum].decideMove(players, board, False)
	        else:
		  gameEnd = playTurn(curPlayer, players, board, AiNum)
		#remove the turnCounter>= 10 when full implementation
		if gameEnd or turnCounter >= 20:
			break
		turnCounter += 1

def playTurn(curPlayer, players, board, AiNum = -1):
	board.createBatchCSV(players)
	board.batchUpdate()
	print  "Player " + str(curPlayer) + " turn"
	askPlayerIfDevCard(curPlayer, players, board)
	diceRoll = board.rollDice()
	if diceRoll is CONST_ROBBER:
		#print "Robber not handled"
		handleRobber(curPlayer, players, board, AiNum)
	else:
		print str(diceRoll) + " was rolled"
		board.assignResources(diceRoll, players)
	for player in players:
		print player
	trade(curPlayer, players, AiNum)
	build(curPlayer, players, board)
	return players[curPlayer].hasWon()

def build(curPlayer, players, board):
	print "Player " + str(curPlayer) + " is building"
	while(True):		
		try:
			response = raw_input("Do you want to build?")
			if response == "Yes" or response == "yes" or response == "y":
				toBuild = raw_input("What do you want to build? ")
				if toBuild == "road":
					buildRoad(curPlayer, players, board)
				elif toBuild == "settlement":
					buildSettlement(curPlayer, players, board)
				elif toBuild == "city":
					buildCity(curPlayer, players, board)
				elif toBuild == "devCard":
					buildDevCard(curPlayer, players, board)
				break
			else:
				break
		except EOFError:
			print " Not building, on sublime"
			break

def handleRobber(curPlayer, players, board, AiNum = -1):
	print "Robber"
	locations = board.getAllTiles()
	print "Choose a location: "
	location_dict = {}
	for l in locations:
		goalTag = board.tileToAscii[l]
		location_dict[goalTag] = l
		print goalTag
        if (curPlayer == AiNum):
            target = players[curPlayer].placeRobber(board)
            if target != None and target != curPlayer:
                steal(players[int(target)], curPlayer,players)
            print "The ai has moved the robber"
	    return
	locationForRobber = 0
	try:
		while True:
			locationForRobber = raw_input("Enter a location (e.g. 12T)")
			if locationForRobber not in location_dict:
				print "Not a valid location. Try again"
			else:
				break
	except EOFError:
		locationForRobber = Location.Tile()
		print  ""
	newRobberLocation = location_dict[locationForRobber]
	board.moveRobber(newRobberLocation)
	targets = board.playersToStealFrom(newRobberLocation)
	print "Choose a player to steal from:"
	for t in targets:
		print t
	target = 0
	if len(targets) != 0:
		try:
			while True:
				target = raw_input("")
				if int(target) not in targets:
					print "Not a valid selection, try again"
				else:
					break
		except EOFError:
			target = 0
			print  ""
		steal(players[int(target)], curPlayer,players)
	else:
		print "There are no settlements bordering that tile, stealing phase skipped"

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

def steal(target, curPlayer,players):
	stolen = target.loseRandomCard()
	if stolen != None:
	   players[curPlayer].addResource(stolen, 1)

def buildRoad(curPlayer, players, board):
	roadLocation = askPlayerForRoadLocation(board)
	players[curPlayer].buildRoad(roadLocation, board)

def buildSettlement(curPlayer, players, board):
	settlementLocation = askPlayerForSettlementLocation(board)
	players[curPlayer].buildSettlement(settlementLocation, board)

def buildCity(curPlayer, players, board):
	cityLocation = askPlayerForCityLocation(curPlayer, players, board)
	players[curPlayer].buildCity(cityLocation, board)

def buildDevCard(curPlayer, players, board):
	if players[curPlayer].canBuildDevCard():
		players[curPlayer].buildDevCard(devCardsDeck)
	else:
		print "You can't build a dev card"

def firstPlacement(numPlayers, players, board, AiNum = -1):
	for i in range (0, numPlayers):
		if (i == AiNum):
			print i
			players[AiNum].decideMove(players, board, True)
			board.createBatchCSV(players)
			board.batchUpdate()
			continue
		board.printBoard()	            
		initialPlacement(i, players, board)
		board.createBatchCSV(players)
		board.batchUpdate()
	print numPlayers
	for i in range(numPlayers -1, -1, -1):
		print i
		if (i == AiNum):
			players[AiNum].decideMove(players, board, True)
			board.createBatchCSV(players)
			board.batchUpdate()
			continue
		board.printBoard()
	 	initialPlacement(i, players, board)
	 	board.createBatchCSV(players)
		board.batchUpdate()
	for player in players:
          	    player.addResource('wood', 2)
          	    player.addResource('brick', 2)
          	    player.addResource('grain', 2)
          	    player.addResource('sheep', 2)
	board.createBatchCSV(players)
	board.batchUpdate()

def initialPlacement(curPlayer, players, board):
	print curPlayer, " is placing their initial settlement and road"
	settlementLoc = None
	asciiVertexLoc = None
	roadLoc = None
	try:
		while (True):
			asciiVertexLoc = raw_input("Enter the ascii for the location you want to build your settlement: ")
			if asciiVertexLoc not in board.asciiToVertex:
				print "error, invalid ascii"
			elif board.asciiToVertex[asciiVertexLoc].getOwner() != None:
				print "error, already has an owner"
			else:
				vertex = board.asciiToVertex[asciiVertexLoc]
				available = True
				for neighbor in board.getVertexToVertices(vertex):
					if neighbor.getOwner() != None:
						available = False
				if available:
					settlementLoc = board.asciiToVertex[asciiVertexLoc]
					break
				else:
					print "error, you must build at least two away from a built city"
	except EOFError:
		print "On sublime, not building"
	try:
		while (True):
			asciiRoadLoc = raw_input("Enter the ascii for the location you want to build your road: ")
			if asciiRoadLoc not in board.asciiToEdge:
				print "error, invalid ascii"
			else:
				roadLoc = board.asciiToEdge[asciiRoadLoc]
				if roadLoc not in board.getVertexToEdges(settlementLoc) or roadLoc.getOwner() is not None:
					print "Error, that road location is not a neighbor of your settlement location, ", asciiVertexLoc, " or is already owned"
				else:
					break
	except EOFError:
		print "On sublime, not building"
	players[curPlayer].buildSettlement(settlementLoc, board)
	players[curPlayer].buildRoad(roadLoc, board)


def selectDevCard(potentialDevCards):
	return 0

def useCard(curPlayer, chosenCard):
	return 0

# convert some string or index into location object
def askPlayerForRoadLocation(board):
	while True:
		asciiLoc = raw_input('Enter the location where you want to build: ')
		if asciiLoc in board.asciiToEdge:
			return board.asciiToEdge[asciiLoc]
		else:
			print 'That location does not exist'

def askPlayerForSettlementLocation(board):
	while True:
		asciiLoc = raw_input('Enter the location where you want to build: ')
		if asciiLoc in board.asciiToVertex:
			return board.asciiToVertex[asciiLoc]
		else:
			print 'That location does not exist'

def askPlayerForCityLocation(curPlayer, players, board):
	while True:
		asciiLoc = raw_input('Enter the location where you want to build: ')
		if board.validCityLoc(asciiLoc):
			return board.asciiToVertex[board.getSettlementFromAscii(asciiLoc)]
		else:
			print 'That location does not exist'

def tradeHelper(trade, curResources, rec = False):
    for r in trade:
            valid = True
            while(valid):
                maxi = curResources[r]
                if (rec):
                    maxi = float('inf')
                if rec:
                    cur = raw_input(r + "?")
                else:
                    cur = raw_input(r + "? (You have " + str(maxi) + ")")
                if isInt(cur):
                    cur = int(cur)
                    if cur >= 0 and cur <= maxi:
                        trade[r] = cur
                        valid = False
                    else:
                        print "invalid amount try again"
                else:
                    print "invalid input try again"
    return trade

def tradeLogicHelper(curPlayer, partner, players, offer, recieve):
    partnerRes = players[partner].checkResources()
    for r in recieve:
        if recieve[r] > partnerRes[r]:
            print "Player ", partner, " cant make the proposed trade because they dont have enough " + r + "."
            return False
    print "Player " + str(partner) + ", Player " + str(curPlayer) + " has proposed to trade: ", offer, "for: ",  recieve, "do you accept?"
    answer = raw_input("y/n?") 
    if answer == "Yes" or answer == "yes" or answer == "y":
        confirm =  raw_input("Player " + str(curPlayer) + " would you like to confirm this trade?")
        if confirm  == "Yes" or confirm == "yes" or confirm == "y":
            print "Trade confirmed."
            for r in offer:
                players[curPlayer].loseResource(r, offer[r])
                players[partner].addResource(r, offer[r])
            for r in recieve:
                players[curPlayer].addResource(r, recieve[r])
                players[partner].loseResource(r, recieve[r])
            for player in players:
				print player
            return True
        else:
            print "Player " + str(curPlayer) + " has changed their mind."
    else:
        print "Player " + str(partner) + "has rejected the trade."
    return False

def trade(curPlayer, players, AiNum = -2):
        print "Trading phase"
        trading = True
        while(trading):
            response = raw_input("Would you like to propose a trade?")
            if  response == "Yes" or response == "yes" or response == "y":
                curResources = players[curPlayer].checkResources()  
                offer =  {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
                print "What would you like to offer? (Enter an amount for each following resource)"
                offer = tradeHelper(offer, curResources)
                recieve = {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
                print "What would you like in return? (Enter an amount for each following resource)"
                recieve = tradeHelper(recieve, curResources, True)
                partner = -1
                potentialPartner = raw_input("Would like to ask a specific player (if so enter the player number you'd like to trade with)")
                if isInt(potentialPartner):
                    potentialPartner = int(potentialPartner)
                    if potentialPartner < len(players) and potentialPartner != curPlayer:
                        partner = potentialPartner
                        print "Proposing trade to player: ", partner
                    else:
                        print "No partner or invalid partner inserted, proposing trade to all players"
                if (partner == AiNum and AiNum != -2):
                    players[AiNum].evaluateTrade(offer, recieve)
                elif partner != -1:
                    tradeLogicHelper(curPlayer, partner, players, offer, recieve)
                else:
                    for i in xrange(len(players)):
                        if i == curPlayer:
                            continue
                        if i == AiNum:
                            executed = players[AiNum].evaluateTrade(offer, recieve)
                            if (executed):
                                break
                        else:
                            executed = tradeLogicHelper(curPlayer, i, players, offer, recieve)
                            if (executed):
                                break
            else:
                trading = False
	
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


main()