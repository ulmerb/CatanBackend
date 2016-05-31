# -*- coding: utf-8 -*-
# Feature discussion
# Weighting of resources
#   Ovearll Best
#   Availability
#   What's in your hand
#   What's in your income

# Vertex Cost Location
#   Turns away
#   Resources used


# Vertex Reward Valuation
#   Centraility
#   Income increase
#   Resource Weighting (from above)
#   Ports
#   Variability (not in alpha)
#   Vertex Cost (from above)
#   Current VP (when at 9VP, cost is all that matters)
#   Total Turns remaaining in the game (not in 1-player)


 




import math
import Player

class ai:
    
    def __init__(self, i):
        self.AI = Player.player(i)
        #weights for features
        self.weights =  {'incomeIncrease' : 1000, 'centrality' : 1.0, 'costInTurns' : -1.0, 'costInRes' : -1.0, 'port' : 1.0, 'vp' : 1.0}
        self.diceProbs = [0.0, 0.0, 0.028,0.056,0.083,0.111,0.139,0.167,0.139,0.111,0.083,0.056,0.028]
        self.income = {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
   
    # getResourceCost(buildType,roadsAway)
    # Varible one, build type, "road", "settlement", "city", "devCard"
    # Variable two, number of roads away
    # 
    def getResourceCost(self, buildType,roadsAway):
   	cost =  {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
   	if(buildType == "road"):
  		cost['brick'] += 1
  		cost['wood'] += 1
   	elif (buildType == "settlement"):
  		cost['sheep'] += 1
  		cost['brick'] += 1
  		cost['wood'] += 1
  		cost['grain'] += 1
  		cost['brick'] += roadsAway
  		cost['wood'] += roadsAway
   	elif (buildType == "city"):
  		cost['grain'] += 2
  		cost['ore'] += 3
   	elif (buildType == "devCard"):
  		cost['sheep'] += 1
  		cost['grain'] += 1
  		cost['ore'] += 1
   	else:
  		print "invalid getResourceCost() call",buildType,roadsAway
   	
   	return cost
    
    def getVictoryPoints(self):
   	return self.AI.getScore();

    def findNeed(self, cost, income):
        if len(cost) == 0:
            return None
        maxNeed = (0, 0)
        need = cost.keys()[0]
        for r in cost:
            if cost[r] <= 0:
                continue
            if income[r] == 0:
                temp = (float('inf'), cost[r])
            else:
                temp = (cost[r]/income[r], cost[r])
            if temp[0] > maxNeed[0] or ((temp[0] == maxNeed[0]) and(temp[1] > maxNeed[1])):
                need = r
                maxNeed = temp
        return need

    def getCostInTurns(self, buildType,roadsAway,incomeMap):
   	resCost = self.getResourceCost(buildType,roadsAway)
   	modResCost = {}
   	turnCost = 0.0 
   	ownedResources = self.AI.resources.copy()
   	stockpile = ownedResources.copy()
   	for r in stockpile:
   	    stockpile[r] = 0
   	baseTurns = 0
   	baseTurnSet = False
   	for res in resCost:
   	    dif = 0
   	    temp = resCost[res] - ownedResources[res]

   	    if temp > dif:
   	        dif = temp
   	    else:
   	        stockpile[res] = -temp
   	    if temp <= 0:
   	        baseTurnSet = True
   	    if dif != 0:
   	        modResCost[res] = dif
        if not baseTurnSet:
            baseTurnSet = float('inf')
            for r in modResCost:
                turns = int(math.ceil(modResCost[r] / incomeMap[r]))
                if turns < baseTurnSet:
                    baseTurnSet = turns
   	#delete fields from needs increment while needs not empty
   	#when we hit overflow give to largest gap
   	#encode ports knowledge
   	turnCost = baseTurns
   	for r in incomeMap:
   	    stockpile[r] += incomeMap[r] * baseTurns	
   	while(len(modResCost) > 0):
   	    for r in stockpile:
   	        if r in modResCost:
   	            if stockpile[r] >= 1:
   	                if modResCost[r] <= stockpile[r]:
   	                    stockpile[r] -= modResCost[r]
   	                    modResCost.pop(r)
   	                    if len(modResCost) == 0:
   	                        return turnCost
   	                else:
   	                    modResCost[r] -= int(stockpile[r])
   	                    stockpile[r] -= int(stockpile[r])
   	        elif stockpile[r] >= 4:
   	            while(stockpile[r] >= 4):
           	            exchange = self.findNeed(modResCost, incomeMap)
           	            if exchange == None:
           	                return turnCost
           	            stockpile[r] -= 4
           	            modResCost[exchange] -= 1
           	            if modResCost[exchange] == 0:
           	                modResCost.pop(exchange)
           	                if len(modResCost) == 0:
   	                            return turnCost
   	    if len(modResCost) == 0:
   	        break
   	    if turnCost > 100:
   	        break
   	    turnCost +=1
   	    for r in stockpile:
   	        stockpile[r] += incomeMap[r]
   	return turnCost
   	        
    def evaluateLocationBenefit(self, vert, board):
        tiles = board.getVertexToTiles(vert)
        # print len(tiles)
        exReturn =  {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        for tile in tiles:
            tileType = tile.getType()
            if tileType == 'desert':
                continue 
            exReturn[tileType] += self.diceProbs[tile.getNumber()]
        return exReturn
    
    #still doesnt handle other players roads that block paths
    def findPlayableLocations(self, vert, x, board):
        #print vert, x, board, "find plays 1"
        trash = set()
        cur = [vert]
        #we use sets to keep the spots unique in case of longer distances
        cur = set(cur)
        #this dictates how many steps away we look (ie, x = 2 means we look for all spots 2 away)
        for i in xrange(x):
            temp = set()
            for v in cur:
                #this board function should return all of a vertex's neighbors
                for n in board.getVertexToVertices(v):
                    #we dont want to back track hence the trash list
                    if n not in trash:
                        #if we're one road away from the spots we're looking we don't
                        #need to consider neighbors of an owned vetex
                        if i == x-2 and n.getOwner() != None:
                            continue
                        temp.add(n)
            trash = trash.union(cur)
            cur = temp
        #this check is still needeed despite above neighbor check, should be more efficient to have both as is
        cur = list(cur)
        trash = []
        for v in cur:
            if v.getOwner() != None:
                #cur.remove(v)
                trash.append(v)
                #print "v", v.getIndex(), "removed 1", v.getOwner()
                continue
            for n in board.getVertexToVertices(v):
                if n.getOwner() != None:
                    #cur.remove(v)
                    trash.append(v)
                    #print "v", v.getIndex(), "removed 2", n.getOwner()
                    break
            #print "v", v.getIndex(), "passed"
        for v in trash:
            cur.remove(v)
        #for v in cur:
            #print "V", v.index
        return cur            
    def evaluateTrade(self, gain, lose):
        print "gain",gain,"lose",lose
        currentResources  = self.AI.resources
        print "currentResources",currentResources
        available = False
        difference = {key: currentResources[key] - lose.get(key, 0) for key in currentResources.keys()}
        print difference
        
        gainTotal = sum(gain.values())
        loseTotal = sum(lose.values())


        print "gainTotal", gainTotal, "loseTotal",loseTotal
        print "The AI is too naive to trade right now"
        return False
    def findShortestPath(self, start, end, expected, board):
        print start, end
        startVert = board.vertices[start]
        seen = []
        paths = []
        for r in board.getVertexToEdges(startVert):
            if r.getOwner() != None and r.getOwner() != self.AI.playerNumber:
                    continue
            seen.append(r.index)
            paths.append([r.index])
        print seen, paths
        curLen = 1
        while(True):
            curLen += 1
            if curLen > expected:
                print "warning curLen has surpassed expected path length"
            temp = []
            for p in paths:
                tip = board.edges[p[-1]]
                for n in board.getEdgeToEdges(tip):
                    if n.getOwner() != None and n.getOwner() != self.AI.playerNumber:
                        continue
                    new = p[:]
                    new.append(n.index)
                    temp.append(new)
                    #p.append(n.index)
                    if curLen >= expected:
                        vertSet = board.getEdgeToVertices(n)
                        for v in vertSet:
                            if v.index == end:
                                print new, curLen
                                return new
            paths = temp
                

            if curLen > 6:
                break
        print paths
    def makeExchange(self, cost, board, locObj, players, typeS):
        print cost, "cccc"
        print self.AI.resources, "<< res"
        for r in self.AI.resources:
            if r not in cost:
                cost[r] = 0
        modCost = cost.copy()
        for r in modCost:
            modCost[r] -= self.AI.resources[r]
        print modCost, "mccc"
        while(not self.AI.canBuildCity(locObj)):
            print cost, modCost
            exchange = self.findNeed(modCost, self.income)
            print exchange
            sortRes = []
            for r in self.AI.resources:
                sortRes.append((self.AI.resources[r] - cost[r], self.income[r], r))
            sortRes.sort(key=lambda tup: tup[1], reverse=True)
            sortRes.sort(key=lambda tup: tup[0], reverse=True)
            print sortRes
            if sortRes[0][0] < 4:
                print "something went wrong, it doesnt appear the " + typeS + " can be built"
                return False
            r = sortRes[0][2]
            print "exchange", r , "for", exchange
            self.AI.resources[r] -= 4
            self.AI.resources[exchange] += 1
            modCost[exchange] -= 1
            '''
            if typeS == 'city' and self.AI.canBuildCity(locObj):
                print "exchanges done"
                return True
            '''
            if not self.needsExchange(cost):
                print "exchanges done"
                return True
    def needsExchange(self, cost):
        for r in cost:
            if cost[r] > self.AI.resources[r]:
                return True
        return False
    def execute(self, players, board, bestOption, bestOptionKey, options):
        #currently all options passed in though unused, may need to eval other options when
        #exchanges come into play
        #more advanced step
        #self.AI.resources =  {'wood':40, 'sheep':0, 'brick': 0, 'ore': 10, 'grain' : 10}

        print "the ai is executing option", bestOptionKey, bestOption
        if bestOption['backtrace'][0] == 'settlement':
            settleLoc = int(bestOptionKey[:2])
            path = self.findShortestPath(bestOption['backtrace'][1], settleLoc, bestOption['backtrace'][2], board)
            roadsAway = bestOption['backtrace'][2]
            for r in path:
                if r in self.AI.structures['roads']:
                    roadsAway -= 1
            cost = self.getResourceCost('settlement', roadsAway)
            settleObj = board.vertices[settleLoc]
            if not self.needsExchange(cost):
                for i in xrange(len(path)):
                    roadInd = path[i]
                    if roadInd in self.AI.structures['roads']:
                        continue
                    locObj = board.edges[roadInd]
                    self.AI.buildRoad(locObj, board)
                self.AI.buildSettlement(settleObj, board)
                self.updateIncome(settleObj, board)

                board.createBatchCSV(players)
		board.batchUpdate()
	        print "the AI has built a settlement"
	    else:
                if self.makeExchange(cost, board, settleObj, players, 'settlement'):
                    for i in xrange(len(path)):
                        roadInd = path[i]
                        if roadInd in self.AI.structures['roads']:
                            continue
                        locObj = board.edges[roadInd]
                        self.AI.buildRoad(locObj, board)
                    self.AI.buildSettlement(settleObj, board)
                    self.updateIncome(settleObj, board)
                    board.createBatchCSV(players)
		    board.batchUpdate()
                    print "the AI has built a settlement after some resource reallocation"

        elif bestOption['backtrace'][0] == 'city':
            print "time to upgrade our chosen loc"
            cost = self.getResourceCost('city', 0)
            print cost
            print self.AI.resources
            locObj = board.vertices[bestOption['backtrace'][1]]
            if self.AI.canBuildCity(locObj):
                self.AI.buildCity(locObj, board)
                self.updateIncome(locObj, board)
                board.createBatchCSV(players)
		board.batchUpdate()
                print "the AI has built a city"
            else:
                print "exchanges needed"
                #the following needs to be decomped later
                cost = self.getResourceCost('city', 0)
                if self.makeExchange(cost, board, locObj, players, 'city'):
                    self.AI.buildCity(locObj, board)
                    self.updateIncome(locObj, board)
                    board.createBatchCSV(players)
                    board.batchUpdate()
                    print "the AI has built a city after some resource reallocation"
        elif bestOption['backtrace'][0] == 'dev':
            print "getting tactical with a dev card"
        else:
            print "something strange has happened, an wild option appears, the ai will reevaluate"
        
            
        
    def decideMove(self, players, board, firstTurn):

# Look at spots available to build on (settlement locations)
# What does it take to get there (how many turns?) expected value
# This is a cost
# Cost vs reward for each spot
# Learned by getting to 10
# Manually change a ratio parameter
# Additional value for ports
# Centrality value
# Longest road length
# At 7+ points different math
# ignore robber at first
# Add ability to automatically branch the game
# ignore trading at first
# Start at each settlement, search for spots 2 away, if not enough, 
# search further, etc. UNTIL we find N+ (start with N=5)
      #don't ignore the update income if something is built
      #self.AI.resources =  {'wood':10, 'sheep':10, 'brick': 10, 'ore': 10, 'grain' : 10}
      if firstTurn:
          locs = list(board.getPotentialSettlementLocs(self.AI.playerNumber, players, True))
          maxIncome = 0
          bestloc = 0
          for i in xrange(len(locs)):
            benefit = self.evaluateLocationBenefit(locs[i], board)
            gain = 0.0
            for r in benefit:
                gain += benefit[r]
            # print "*******"
            # print locs[i].index
            # print benefit
            # print "******"
            if gain > maxIncome:
                bestloc = i
                maxIncome = gain
          self.AI.buildSettlement(locs[bestloc], board)
          self.updateIncome(locs[bestloc], board)
          builtSettlementSpot = locs[bestloc].getIndex()
          roadOptions = board.vertexToEdgeMap[builtSettlementSpot]
          print builtSettlementSpot, "roadOptions", roadOptions
          print "currently just choosing the first road on the list" # Currentliy just building at the first option
          roadChoice = board.edges[roadOptions[0]]
          self.AI.buildRoad(roadChoice, board) 
      else:
        curDistanceAway = 2
        devCardCost = sum(self.getResourceCost('devCard', 0).values())
        options = {"devCard": {'costInRes' : devCardCost, 'backtrace' : ['dev']},"pass": {'backtrace' : ['pass']} }
        curSettlements = self.AI.structures['settlements'][:]
        curSettlements += self.AI.structures['cities']
        if self.AI.settlementsRemaining > 0:
            while(True):
                for settlement in curSettlements:
                    s = board.vertices[settlement]
                    playableLocations = self.findPlayableLocations(s,curDistanceAway,board)
                    for playableS in playableLocations:
                        #ideally object to ascii
                        benefit = self.evaluateLocationBenefit(playableS, board)
                        turnCost = self.getCostInTurns('settlement', curDistanceAway, self.income)
                        resCost = sum(self.getResourceCost('settlement', curDistanceAway).values())
                        asciiRepresentation = str(board.vertexToAscii[playableS])
                        options[asciiRepresentation] = {'incomeIncrease': sum(benefit.values()), 'costInTurns' : turnCost, 'costInRes' : resCost, 'backtrace' : ['settlement', settlement, curDistanceAway]}
                if (len(options) >= 7 or curDistanceAway >= 5):
                    break
                curDistanceAway += 1
        print self.AI.structures['settlements']
        if self.AI.citiesRemaining > 0:      
            for settle in self.AI.structures['settlements']:
                s = board.vertices[settle]
                benefit = self.evaluateLocationBenefit(s, board)
                turnCost = self.getCostInTurns('city', 0, self.income)
                resCost = sum(self.getResourceCost('city', 0).values())
                asciiRepresentation = str(board.vertexSettlementAscii(s))
                options[asciiRepresentation] = {'incomeIncrease': sum(benefit.values()), 'costInTurns' : turnCost, 'costInRes' : resCost, 'backtrace' : ['city', settle]}
          #need to add more options and expand the curDistanceAway
        print options
        bestOptionKey = self.evaluateOptions(options)
        print bestOptionKey
        bestOption = options[bestOptionKey[0]]
        if bestOptionKey[0] == 'pass':
            "The wise Ai has contemplated all its options and decided to pass"
            return
        if bestOption['costInTurns'] == 0:
            self.execute(players, board, bestOption, bestOptionKey[0], options)
        else:
            print "The Ai will pass for now, its planning something!"
        vp = self.getVictoryPoints()
        if vp == 10:
            print self.AI.structures['settlements'], "Settlements"
            print self.AI.structures['cities'], "cities"
        return vp
    def evaluateOptions(self, options):
        bestOption = ""
        bestScore = -float('inf')
        for opt in options:
            score = 0.0
            for field in options[opt]:
                    if field not in self.weights:
                        continue
                    score += options[opt][field] * self.weights[field]
            if score > bestScore:
                bestOption = opt
                bestScore = score
        return bestOption, bestScore
    def placeRobber(self, board):
        newRobberLocation = board.asciiToTile['01T']
        board.moveRobber(newRobberLocation)
        targets = list(board.playersToStealFrom(newRobberLocation))
        if len(targets) > 0:
            return targets[0]
        else:
            return None

    def updateIncome(self, vert, board):
        #anytime we build on a location whether adding a settlment or changing to city
        #our income increases by one settlment of expected value so we can levarge our
        #benefit function
        gain = self.evaluateLocationBenefit(vert, board)
        for res in gain:
            self.income[res] += gain[res]
    def addResource(self, res, amount):
        self.AI.addResource(res, amount)
        
    def loseResource(self, res, amount, verbose = False):
        self.AI.loseResource(res, amount)
        
    def loseRandomCard(self):
        self.AI.loseRandomCard()   
             
    def tests(self):
        print self.AI.roadsRemaining
    