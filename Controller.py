
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
		#print "Robber not handled"
		handleRobber(curPlayer, players, board)
	else:
		print str(diceRoll) + " was rolled"
		board.assignResources(diceRoll, players)
	for player in players:
		print player
	trade(curPlayer, players)
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

def handleRobber(curPlayer, players, board):
	print "Robber"
	locations = board.getAllTiles()
	print "Choose a location: "
	location_dict = {}
	for l in locations:
		goalTag = board.tileToAscii(l.x,l.y)
		location_dict[goalTag] = l
		print goalTag
	locationForRobber = 0
	try:
		locationForRobber = raw_input("Enter a location (e.g. 12T)")
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
	try:
		target = raw_input("")
	except EOFError:
		target = 0
		print  ""
	steal(players[int(target)], curPlayer,players)

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
	players[curPlayer].addResource(stolen, 1)

def buildRoad(curPlayer, players, board):
	roadLocation = askPlayerForRoadLocation()
	players[curPlayer].buildRoad(roadLocation, board)
	board.buildRoad(curPlayer, players, roadLocation)

def buildSettlement(curPlayer, players, board):
	settlementLocation = askPlayerForSettlementLocation(board)
	players[curPlayer].buildSettlement(settlementLocation, board)
	board.buildSettlement(curPlayer, players, settlementLocation)

def buildCity(curPlayer, players, board):
	cityLocation = askPlayerForCityLocation()
	players[curPlayer].buildCity(cityLocation)
	board.buildCity(curPlayer, players, cityLocation)

def buildDevCard(curPlayer, players, board):
	if players[curPlayer].canBuildDevCard():
		players[curPlayer].buildDevCard(devCardsDeck)
	else:
		print "You can't build a dev card"

def firstPlacement(numPlayers, players, board):
	for i in range (0, numPlayers):
		board.initialPlacement(i, players)
	for i in range(numPlayers, 0, -1):
	 	board.initialPlacement(i-1, players)
 	for player in players:
		player.resources['wood'] += 2
		player.resources['brick'] += 2
		player.resources['grain'] += 2
		player.resources['sheep'] += 2
	board.createBatchCSV(players)
	board.batchUpdate()



def selectDevCard(potentialDevCards):
	return 0

def useCard(curPlayer, chosenCard):
	return 0

# convert some string or index into location object
def askPlayerForRoadLocation():
	return 0

def askPlayerForSettlementLocation(board):
	while True:
		asciiLoc = raw_input('Enter the location where you want to build: ')
		if asciiLoc in board.asciiToVertex:
			return board.asciiToVertex[asciiLoc]
		else:
			print 'That location does not exist'

def askPlayerForCityLocation():
	return 0

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
            return True
        else:
            print "Player " + str(curPlayer) + " has changed their mind."
    else:
        print "Player " + str(partner) + "has rejected the trade."
    return False
def trade(curPlayer, players):
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
                if partner != -1:
                    tradeLogicHelper(curPlayer, partner, players, offer, recieve)
                else:
                    for i in xrange(len(players)):
                        if i == curPlayer:
                            continue
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