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
reload(asc)
reload(Location)

CONST_DEFAULT_NUM_PLAYERS = 2

CONST_ROBBER = 7

## Server related functions ##
def tileInitialization(numPlayers, ai):
	board = Board.board()
	devCardsDeck = Devcards.devcards()
	players = []
	for i in range (0, numPlayers):
		players.append(Player.player(i))
	AiNum = -1
	if ai:
		players.append(Ai.ai(len(players)))
		numPlayers +=1
	if not ai or numPlayers > 1:
	   board.createBatchCSV(players)
	   board.batchUpdate()
	return board, players

def rollDice(board, players, curPlayer, AiNum=-1):
	diceRoll = board.rollDice()
	if diceRoll is CONST_ROBBER:
		#print "Robber not handled"
		return diceRoll
	else:
		print str(diceRoll) + " was rolled"
		board.assignResources(diceRoll, players)
		return diceRoll

def serverHandleRobber(curPlayer, players, loc, target, board, AiNum):
	if curPlayer == AiNum:
		target = players[curPlayer].placeRobber(board)
		if target != None and target != curPlayer:
		    steal(players[int(target)], curPlayer,players)
		print "The ai has moved the robber"
	else:
		if loc > 0 and loc < len(board.tiles) - 1:
			newRobberLocation = board.tiles[loc]
			board.moveRobber(newRobberLocation)
			board.createBatchCSV(players)
			board.batchUpdate()
			targets = board.playersToStealFrom(newRobberLocation)
			print len(targets), "Should be 0"
			if len(targets) != 0:
				if int(target) not in targets:
					return "Invalid target"
				else:
					steal(players[int(target)], curPlayer, players)
			else:
				return "No targets"
		else:
			return "Invalid tile"

def serverBuildRoad(curPlayer, players, board, sugLoc):
	if sugLoc in board.asciiToEdge:
		loc = board.asciiToEdge[sugLoc]
		players[curPlayer].buildRoad(loc, board)
		asc.buildRoad(board.currentBoardNumber, sugLoc, str(curPlayer))
	else:
		return "road build failed"

def serverBuildSettlement(curPlayer, players, board, sugLoc):
	if sugLoc in board.asciiToVertex:
		loc = board.asciiToVertex[sugLoc]
		players[curPlayer].buildSettlement(loc, board)
		#test
		board.createBatchCSV(players)
		board.batchUpdate()
		print "my current board:"
		print board.printBoard()
		# if not error:
		board.handlePortConstruction(curPlayer, loc)
		asc.buildSettlement(board.currentBoardNumber, sugLoc, str(curPlayer), str(5 - players[curPlayer].settlementsRemaining))
		# else:
			# return error
	else:
		return "Vertex not on board"

def serverBuildCity(curPlayer, players, board, sugLoc):
	if board.validCityLoc(sugLoc):
		loc = board.asciiToVertex[board.getSettlementFromAscii(sugLoc)]
		players[curPlayer].buildCity(loc, board)
		asc.buildCity(board.currentBoardNumber,sugLoc,str(curPlayer))
	else:
		return "city build failed"


def serverUseCard(curPlayer, players, board, chosenCard, devCardBrick, devCardWood, devCardSheep, devCardOre, devCardGrain, roadLoc1, roadLoc2):
	if chosenCard == "knight":
		print "You played a knight!"
		handleRobber(curPlayer, players, board)
		recalculateLargestArmy(players, board)
		players[curPlayer].playDevCard(chosenCard)
	if chosenCard == "victoryPoint":
		players[curPlayer].incrementScore()
		players[curPlayer].playDevCard(chosenCard)
		print "You got a victory point!"
	if chosenCard == "roadBuild":
		print "You can build two free roads!"
		roadOne = board.asciiToEdge[roadLoc1]
		if players[curPlayer].validSpaceForRoad(roadOne, board):
			roadOne.buildRoad(curPlayer)
			players[curPlayer].structures['roads'].append(roadOne.index)
		else:
			return "Invalid road 1"
		roadTwo = board.asciiToEdge[roadLoc2]
		if players[curPlayer].validSpaceForRoad(roadTwo, board):
			roadTwo.buildRoad(curPlayer)
			players[curPlayer].structures['roads'].append(roadTwo.index)
			players[curPlayer].playDevCard(chosenCard)
		else:
			return "Invalid road 2"
	if chosenCard == "monopoly":
		resource = ""
		if devCardBrick:
			resource = 'brick'
		elif devCardWood:
			resource = 'wood'
		elif devCardOre:
			resource = 'ore'
		elif devCardGrain:
			resource = 'grain'
		elif devCardSheep:
			resource = 'sheep'
		totalStolen = 0
		for player in players:
			numResource = player.numResources(resource)
			player.loseResource(resource, numResource)
			players[curPlayer].addResource(resource, numResource)
		players[curPlayer].playDevCard(chosenCard)
	if chosenCard == "yearOfPlenty":
		numChosen = 0
		
		if devCardBrick:
			players[curPlayer].addResource('brick', 1)
		if devCardWood:
			players[curPlayer].addResource('wood', 1)
		if devCardOre:
			players[curPlayer].addResource('ore', 1)
		if devCardGrain:
			players[curPlayer].addResource('grain', 1)
		if devCardSheep:
			players[curPlayer].addResource('sheep', 1)
		players[curPlayer].playDevCard(chosenCard)

## NON SERVER RELATED FUNCTIONS BELOW
def main():
	
	numPlayers = -1
	#test Ben
	#sublime text can't work with stdin, so hardcoded it as a 2 player game while on sublime
	while(True):
		try:
			response = raw_input('How many players do you want? ')
			numPlayers = int(response)
		except ValueError:
			print "Please enter a number"
			continue
		if (numPlayers >= 0 and numPlayers <= 4):
			break
		else:
			print "Please enter a number betweeen 0 and 4"
	players = []
	for i in range (0, numPlayers):
		players.append(Player.player(i))
	AiNum = -1
	try:
            response = raw_input("Add an Ai player?")
            if response == "Yes" or response == "yes" or response == "y":
                AiNum = len(players)			
                players.append(Ai.ai(AiNum))
                numPlayers +=1
	except EOFError:
		print " Not building, on sublime"
        if AiNum != -1 and numPlayers == 1:
	   numRuns = input('How many runs? ')
	else:
	   numRuns = 1
	if numRuns > 1:
	        stats = []
           	for x in xrange(numRuns):
           	    numPlayers = 1
           	    players = []
           	    AiNum = len(players)			
                    players.append(Ai.ai(AiNum))
                    board = Board.board()
               	    devCardsDeck = Devcards.devcards()
                    #board.createBatchCSV(players)
                    #board.batchUpdate()
                    #print board.printBoard()
                    firstPlacement(numPlayers, players, board, AiNum)
                    stats.append(playMainGame(numPlayers, players, board, devCardsDeck, AiNum))
                print stats
                print "average turns (excluding robber) = ", sum(stats)/float(numRuns)
        else:
            board = Board.board()
            devCardsDeck = Devcards.devcards()
            board.createBatchCSV(players)
            board.batchUpdate()
            print board.printBoard()
            firstPlacement(numPlayers, players, board, AiNum)
            playMainGame(numPlayers, players, board, devCardsDeck, AiNum)

def playMainGame(numPlayers, players, board, devCardsDeck, AiNum = -1):
	turnCounter = 1
	robberCounter = 0
	while (True):
	        #print turnCounter
	        curPlayer = turnCounter % numPlayers
	        isAi = False
	        if (curPlayer == AiNum):
	            isAi = True
	        if (isAi):
	            diceRoll = board.rollDice()
	            #print "dice", diceRoll
	            if diceRoll is CONST_ROBBER:
		        handleRobber(curPlayer, players, board, AiNum)
		        robberCounter += 1
		    else:
		        board.assignResources(diceRoll, players)
	            gameEndVP = players[AiNum].decideMove(players, board, False)
	            #print gameEndVP
	            if gameEndVP >= 10:
	                print "the Ai has won in", turnCounter, "turns with", robberCounter, "wasted robber turns"
	                gameEnd = True
	                return turnCounter - robberCounter
	            else:
	                gameEnd = False
	        else:
		  gameEnd = playTurn(curPlayer, players, board, devCardsDeck, AiNum)
		#remove the turnCounter>= 10 when full implementation
		if gameEnd or turnCounter >= 1000:
			break
		turnCounter += 1

def playTurn(curPlayer, players, board, devCardsDeck, AiNum = -1):
	board.createBatchCSV(players)
	board.batchUpdate()
	print board.printBoard()
	print  "Player " + str(curPlayer) + " turn"
	askPlayerIfDevCard(curPlayer, players, board)
	diceRoll = board.rollDice()
	if diceRoll is CONST_ROBBER:
		print "7 is rolled, robber!"
		handleResourceLossFromRobber(players, board)
		handleRobber(curPlayer, players, board, AiNum)
	else:
		print str(diceRoll) + " was rolled"
		board.assignResources(diceRoll, players)
	for player in players:
		print player
	trade(curPlayer, players, board, AiNum)
	build(curPlayer, players, board, devCardsDeck)
	return players[curPlayer].hasWon()

def build(curPlayer, players, board, devCardsDeck):
	print "Player " + str(curPlayer) + " is in building phase"
	building = True
	while(building):
		response = raw_input("Do you want to build?")
		if response == "Yes" or response == "yes" or response == "y":
			toBuild = raw_input("What do you want to build? ")
			if toBuild == "road":
				buildRoad(curPlayer, players, board)
			elif toBuild == "settlement":
				buildSettlement(curPlayer, players, board)
			elif toBuild == "city":
				buildCity(curPlayer, players, board)
			elif toBuild == "devCard" or toBuild == "devcard":
				buildDevCard(curPlayer, players, board, devCardsDeck)
			board.createBatchCSV(players)
			board.batchUpdate()
			print players[curPlayer]
		else:
			building = False

def handleDiscard(player, playerNum, resources):
	print "You have ", player.resources
	toDiscard = resources / 2
	print "Player ", playerNum, " has too many resources. ", playerNum, " must discard ", toDiscard
	try:
		while True:
			numWood = int(raw_input("How much wood do you want to discard? "))
			if numWood > player.resources['wood']:
				print "You can't discard that much, you only have ",  player.resources['wood'], " wood"
				continue
			else:
				print "You will discard ", numWood, " of your ", player.resources['wood'], " wood"
			numBrick = int(raw_input("How much brick do you want to discard? "))
			if numBrick > player.resources['brick']:
				print "You can't discard that much, you only have ",  player.resources['brick'], " brick"
				continue
			else:
				print "You will discard ", numBrick, " of your ", player.resources['brick'], " brick"
			numOre = int(raw_input("How much ore do you want to discard? "))
			if numOre > player.resources['ore']:
				print "You can't discard that much, you only have ",  player.resources['ore'], " ore"
				continue
			else:
				print "You will discard ", numOre, " of your ", player.resources['ore'], " ore"				
			numSheep = int(raw_input("How muuch sheep do you want to discard? "))
			if numSheep > player.resources['sheep']:
				print "You can't discard that much, you only have ",  player.resources['sheep'], " sheep"
				continue
			else:
				print "You will discard ", numSheep, " of your ", player.resources['sheep'], " sheep"
			numWheat = int(raw_input("How much wheat do you want to discard? "))
			if numWheat > player.resources['grain']:
				print "You can't discard that much, you only have ",  player.resources['grain'], " wheat"
			else:
				print "You will discard ", numWheat, " of your ", player.resources['grain'], " wheat"
			totalResources = numWood+numBrick+numOre+numSheep+numWheat
			if totalResources != toDiscard:
				print "You selected ", totalResources, " resources, you need to discard ", toDiscard, " resources"
				continue
			else:
				player.loseResource('wood',numWood)
				player.loseResource('brick',numBrick)
				player.loseResource('ore',numOre)
				player.loseResource('sheep',numSheep)
				player.loseResource('grain',numWheat)
				break
	except EOFError:
		print "Sublime error"
	except ValueError:
		print "Please enter a number"
		handleDiscard(player, playerNum, resources)

def handleResourceLossFromRobber(players, board):
	for playerNum in range(len(players)):
		player = players[playerNum]
		resources = player.totalResources()
		if resources > 7:
			handleDiscard(player, playerNum, resources)

def handleRobber(curPlayer, players, board, AiNum = -1):
	if curPlayer != AiNum: print "Robber"
	locations = board.getAllTiles()
	if curPlayer != AiNum: print "Choose a location: "
	location_dict = {}
	for l in locations:
		goalTag = board.tileToAscii[l]
		location_dict[goalTag] = l
		if curPlayer != AiNum: print goalTag
        if (curPlayer == AiNum):
            target = players[curPlayer].placeRobber(board)
            if target != None and target != curPlayer:
                steal(players[int(target)], curPlayer,players)
            if curPlayer != AiNum: print "The ai has moved the robber"
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
	if not players[curPlayer].canPlayDevCard():
		print "You don't have any dev cards, this step is skippped"
		return 0
	selection = 0
	try:
		selection = raw_input("Do you want to play a dev card?")
		if selection == "Yes" or selection == "yes" or selection == "y":
			if players[curPlayer].canPlayDevCard():
				potentialDevCards = players[curPlayer].getDevCards()
				chosenCard = selectDevCard(potentialDevCards)
				if chosenCard == False:
					return 0
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
	checkLongestRoad(board, players)

def buildSettlement(curPlayer, players, board):
	settlementLocation = askPlayerForSettlementLocation(board)
	players[curPlayer].buildSettlement(settlementLocation, board)
	board.handlePortConstruction(curPlayer, settlementLocation)

def buildCity(curPlayer, players, board):
	cityLocation = askPlayerForCityLocation(curPlayer, players, board)
	players[curPlayer].buildCity(cityLocation, board)

def buildDevCard(curPlayer, players, board, devCardsDeck):
	if players[curPlayer].canBuildDevCard():
		nameCard = players[curPlayer].buildDevCard(devCardsDeck)
		return nameCard
	else:
		print "You can't build a dev card"

def firstPlacement(numPlayers, players, board, AiNum = -1):
	#print board.printBoard()
	for i in range (0, numPlayers):
		if (i == AiNum):
			#print i
			players[AiNum].decideMove(players, board, True)
			#board.createBatchCSV(players)
			#board.batchUpdate()
			#print board.printBoard()
			continue
		print board.printBoard()    
		initialPlacement(i, players, board)
		board.createBatchCSV(players)
		board.batchUpdate()
	print numPlayers
	for i in range(numPlayers -1, -1, -1):
		if (i == AiNum):
			players[AiNum].decideMove(players, board, True)
			#board.createBatchCSV(players)
			#board.batchUpdate()
			#print board.printBoard()
			continue
		print board.printBoard()
	 	setLoc = initialPlacement(i, players, board)
	 	for tile in board.vertexToTileMap[setLoc.index]:
	 		if board.tiles[tile].type != "desert":
	 			players[i].addResource(board.tiles[tile].type, 1)
	 	#board.createBatchCSV(players)
		#board.batchUpdate()
	#board.createBatchCSV(players)
	#board.batchUpdate()

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
	board.handlePortConstruction(curPlayer, settlementLoc)
	players[curPlayer].buildRoad(roadLoc, board)
	return settlementLoc

def checkLongestRoad(board, players):
	longestRoad = 0
	leadingPlayer = -1
	bestIndex = -1
	curIndex = 0
	for player in players:
		print "examining ", player
		numRoads = player.getRoadLength(board)
		if numRoads > longestRoad:
			longestRoad = numRoads
			leadingPlayer = player
			bestIndex = curIndex
		curIndex += 1
	print "It was found that ", leadingPlayer, " has a road length of ", longestRoad
	if longestRoad >= 5 and longestRoad > board.curLongestRoad:
		if board.longestRoad != -1:
			print board.longestRoad, " lost longestRoad"
			players[board.longestRoad].incrementScore(-2)
		print bestIndex, " gained longestRoad"
		players[bestIndex].incrementScore(2)
		board.longestRoad=bestIndex
		board.curLongestRoad = longestRoad

def selectDevCard(potentialDevCards):
	print "You have: "
	for devCard in potentialDevCards:
		print devCard
	try:
		while (True):
			selection = raw_input("Which dev card to you want to play (enter 'No' if you don't want to play a dev card'? ")
			if selection == 'No' or selection == 'no':
				return False
			if selection not in potentialDevCards:
				print "Not a valid selection, try again"
			else:
				return selection
	except EOFError:
		print "Sublime error"

def recalculateLargestArmy(players, board):
	maxKnights = 0
	leadingPlayer = -1
	bestIndex = -1
	curIndex = 0
	for player in players:
		numKnights = player.getKnightsPlayed()
		if numKnights > maxKnights:
			maxKnights = numKnights
			leadingPlayer = player
			bestIndex = curIndex
		curIndex += 1
	if maxKnights >= 3 and maxKnights > board.curMaxKnights:
		if board.largestArmy != -1:
			players[board.largestArmy].incrementScore(-2)
			print board.largestArmy, " lost largestArmy"
		print bestIndex, " gained largestArmy"
		players[bestIndex].incrementScore(2)
		board.largestArmy=bestIndex
		board.curMaxKnights = maxKnights
		


def useCard(curPlayer, players, board, chosenCard):
	players[curPlayer].playDevCard(chosenCard)
	if chosenCard == "knight":
		print "You played a knight!"
		handleRobber(curPlayer, players, board)
		recalculateLargestArmy(players, board)
	if chosenCard == "victoryPoint":
		players[curPlayer].incrementScore()
		print "You got a victory point!"
	if chosenCard == "roadBuild":
		print "You can build two free roads!"
		roadOne = askPlayerForRoadLocation(board)
		while True:
			if players[curPlayer].validSpaceForRoad(roadOne, board):
				break
			else:
				print "Not a valid space. Try again"
				roadOne = askPlayerForRoadLocation(board)
		roadOne.buildRoad(curPlayer)
		players[curPlayer].structures['roads'].append(roadOne.index)
		roadTwo = askPlayerForRoadLocation(board)
		while True:
			if players[curPlayer].validSpaceForRoad(roadTwo, board):
				break
			else:
				print "Not a valid space. Try again"
		roadTwo.buildRoad(curPlayer)
		players[curPlayer].structures['roads'].append(roadTwo.index)
	if chosenCard == "monopoly":
		resource = ""
		try: 
			while (True):
				resource = raw_input("What resource do you want to steal?")
				if resource != "wood" and resource != "sheep" and resource != "brick" and resource != "ore" and resource != "grain":
					print "not a valid resource"
				else:
					break
		except EOFError:
			print "Sublime error"
		totalStolen = 0
		for player in players:
			numResource = player.numResources(resource)
			player.loseResource(resource, numResource)
			players[curPlayer].addResource(resource, numResource)
	if chosenCard == "yearOfPlenty":
		numChosen = 0
		try:
			while True:
				if numChosen == 2:
					break
				resource = raw_input("What resource do you want to get?")
				if resource != "wood" and resource != "sheep" and resource != "brick" and resource != "ore" and resource != "grain":
					print "Not a valid resource"
					continue
				numChose += 1
				players[curPlayer].addResource(resource, 1)
		except EOFError:
			print "Sublime error"


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

def resourceSelector(prompt):
	try:
		resource = ""
		while True:
			resource =  raw_input(prompt)
			if resource != "wood" and resource != "grain" and resource != "brick" and resource != "ore" and resource != "sheep":
				print "Not a valid resource, try again"
			else:
				return resource
	except EOFError:
		return ""


def getAmountFromPlayer():
	try:
		amount =  raw_input("What amount do you want to select? ")
		return int(amount)
		if amount < 0:
			print "Enter a number that's greater than 0"
			return getAmountFromPlayer
	except EOFError:
		return ""
	except ValueError:
		print "Enter an integer"
		return getAmountFromPlayer()

def findTradeModifier(curPlayer, resource, board):
	if curPlayer in board.ports[resource]:
		return 2
	if curPlayer in board.ports["three"]:
		return 3
	return 4

def trade(curPlayer, players, board, AiNum = -2):
        print "Trading phase"
        trading = True
        while(trading):
            response = raw_input("Would you like to propose a trade?")
            if  response == "Yes" or response == "yes" or response == "y":
            	bankResponse = raw_input("Would you like to trade with the bank?")
            	if  bankResponse == "Yes" or response == "yes" or response == "y":
            		toLose = resourceSelector("Which resource do you want to give to the bank? ")
            		numberToLose = getAmountFromPlayer()
            		toGet = resourceSelector("Which resource do you want to receive? ")
            		modifier = findTradeModifier(curPlayer, toLose, board)
            		if numberToLose % modifier != 0:
            			print "Retry and enter a number that is a multiple of ", modifier
            			continue
            		else:
						players[curPlayer].addResource(toGet, numberToLose/modifier)
						players[curPlayer].loseResource(toLose, numberToLose)
						print "You know have ", players[curPlayer].resources
						continue
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
                else: # in this case they didn't provid a number so we can assume they want to offer it to anyone
                	partner = -3
                if (partner == AiNum and AiNum != -2):
					traded = players[AiNum].evaluateTrade(offer, recieve)
					print "trade executed with AI"
					for r in offer:
						players[curPlayer].loseResource(r, offer[r])
						players[AiNum].addResource(r, offer[r])
					for r in recieve:
						players[curPlayer].addResource(r, recieve[r])
						players[AiNum].loseResource(r, recieve[r])
					for player in players:
						print player
                elif partner != -1 and partner != -3:
                    tradeLogicHelper(curPlayer, partner, players, offer, recieve)
                else:
                    for i in xrange(len(players)):
                        if i == curPlayer:
                            continue
                        if i == AiNum:
                            executed = players[AiNum].evaluateTrade(offer, recieve)
                            if (executed):
								print "trade executed with AI"
								for r in offer:
									players[curPlayer].loseResource(r, offer[r])
									players[AiNum].addResource(r, offer[r])
								for r in recieve:
									players[curPlayer].addResource(r, recieve[r])
									players[AiNum].loseResource(r, recieve[r])
								for player in players:
									print player
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

# comment out main when using controller to handle requests
<<<<<<< HEAD
#main()
=======
# main()
>>>>>>> origin/master

