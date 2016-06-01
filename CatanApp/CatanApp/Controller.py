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
		newRobberLocation = board.asciiToTile[loc]
		board.moveRobber(newRobberLocation)
		targets = board.playersToStealFrom(newRobberLocation)
		if len(targets) != 0:
			if int(target) not in targets:
				return "Invalid target"
			else:
				steal(players[int(target)], curPlayer, players)



## NON SERVER RELATED FUNCTIONS BELOW
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
	playMainGame(numPlayers, players, board, devCardsDeck, AiNum)

def playMainGame(numPlayers, players, board, devCardsDeck, AiNum = -1):
	turnCounter = 1
	robberCounter = 0
	while (True):
	        print turnCounter
	        curPlayer = turnCounter % numPlayers
	        isAi = False
	        if (curPlayer == AiNum):
	            isAi = True
	        if (isAi):
	            diceRoll = board.rollDice()
	            print "dice", diceRoll
	            if diceRoll is CONST_ROBBER:
		        handleRobber(curPlayer, players, board, AiNum)
		        robberCounter += 1
		    else:
		        board.assignResources(diceRoll, players)
	            gameEndVP = players[AiNum].decideMove(players, board, False)
	            print gameEndVP
	            if gameEndVP >= 10:
	                print "the Ai has won in", turnCounter, "turns with", robberCounter, "wasted robber turns"
	                gameEnd = True
	            else:
	                gameEnd = False
	        else:
		  gameEnd = playTurn(curPlayer, players, board, devCardsDeck, AiNum)
		#remove the turnCounter>= 10 when full implementation
		if gameEnd or turnCounter >= 100:
			break
		turnCounter += 1

def playTurn(curPlayer, players, board, devCardsDeck, AiNum = -1):
	board.createBatchCSV(players)
	board.batchUpdate()
	print  "Player " + str(curPlayer) + " turn"
	askPlayerIfDevCard(curPlayer, players, board)
	diceRoll = board.rollDice()
	if diceRoll is CONST_ROBBER:
		#print "Robber not handled"
		handleResourceLossFromRobber(players, board)
		handleRobber(curPlayer, players, board, AiNum)
	else:
		print str(diceRoll) + " was rolled"
		board.assignResources(diceRoll, players)
	for player in players:
		print player
	trade(curPlayer, players, AiNum)
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

def buildSettlement(curPlayer, players, board):
	settlementLocation = askPlayerForSettlementLocation(board)
	players[curPlayer].buildSettlement(settlementLocation, board)

def buildCity(curPlayer, players, board):
	cityLocation = askPlayerForCityLocation(curPlayer, players, board)
	players[curPlayer].buildCity(cityLocation, board)

def buildDevCard(curPlayer, players, board, devCardsDeck):
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

def useCard(curPlayer, players, board, chosenCard):
	players[curPlayer].playDevCard(chosenCard)
	if chosenCard == "knight":
		print "You played a knight!"
		handleRobber(curPlayer, players, board)
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
main()
