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
import VertexToCentralityDict
import sys

class ai:
    
    def __init__(self, i, verbose = False):
        self.AI = Player.player(i)
        self.vertexToCentralityMap = VertexToCentralityDict.getMap()
        #weights for features
        #change this for not baseline
        #self.weights =  {'incomeIncrease' : 100, 'centrality' : .2, 'costInTurns' : -1.0, 'costInRes' : -2.0, 'port' : 2.0}
        #this is the baseline
        self.weights =  {'incomeIncrease' : 100, 'centrality' : 0.2, 'costInTurns' : -1.0, 'costInRes' : -2.0, 'port' : 20.0}
        self.diceProbs = [0.0, 0.0, 0.028,0.056,0.083,0.111,0.139,0.167,0.139,0.111,0.083,0.056,0.028]
        self.income = {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        self.savedBestOpt = [None, None]
        self.overallScarcity = None
        self.savedPaths = {}
        self.portsMap = {5 : 'three', 6 : 'three', 3 : 'three', 4 : 'three', 28 : 'three', 17 : 'three', 53 : 'three',
        54 : 'three', 39 : 'ore', 40 : 'ore', 8 : 'sheep', 9 : 'sheep', 50 : 'grain', 51 : 'grain', 37 : 'wood', 47: 'wood', 16 : 'brick', 26 : 'brick'}
        self.verbose = verbose
        self.scarceWeightsInc = {'overall' : 0.0, 'soon' : 0.0, 'cur' : 3.0, 'gross' : 0.0} #this should sum to three for baseline
        self.scarceWeightsCost = {'overall' : 0.0, 'soon' : 0.0, 'cur' : 3.0, 'gross' : 0.0} #this should sum to three for baseline
   

    def numResources(self, resource):
      return self.AI.numResources(resource)

    def loseResource(self, resource, numResource):
      self.AI.loseResource(resource, numResource)
    
    def addResource(self, resource, numResource):
      self.AI.addResource(resource, numResource)

    def incrementScore(self, s = 1):
      self.AI.incrementScore(s)

    def getRoadLength(self, board):
      return self.AI.getRoadLength(board)

    def getKnightsPlayed(self):
      return self.AI.getKnightsPlayed()
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
  		if self.verbose: print "invalid getResourceCost() call",buildType,roadsAway
   	
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
   	        exNum = 4
   	        if r in self.AI.structures['ports']:
   	            exNum = 2
   	        elif 'three' in self.AI.structures['ports']:
   	            exNum = 3
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
   	        elif stockpile[r] >= exNum:
   	            while(stockpile[r] >= exNum):
           	            exchange = self.findNeed(modResCost, incomeMap)
           	            if exchange == None:
           	                return turnCost
           	            stockpile[r] -= exNum
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
    def evaluateTrade(self, gain, lose, players, board):
        if self.verbose: 
            print "gain",gain,"lose",lose
        currentResources  = self.AI.resources
        if self.verbose: print "currentResources",currentResources
        available = False
        difference = {key: currentResources[key] - lose.get(key, 0) for key in currentResources.keys()}
        if self.verbose:
            print "difference",difference
        for key in difference: # Check if we don't have the resources to support the trade
          if difference[key] < 0:
            if self.verbose:
                print "dont have enough", key, "to accept trade"
            return False

        scarcity = self.getSoonScarcity(players, board)
        gainTotal = 0
        loseTotal = 0
        for value in gain:
          gainTotal += scarcity[value] * gain[value]
        for value in lose:
          loseTotal += scarcity[value] * lose[value]
        if self.verbose: print "gainTotal", gainTotal, "loseTotal",loseTotal
        if gainTotal > loseTotal: # accept if we are gaining more than we're losing
          return True
        if self.verbose:
            print "The AI doesn't like this trade"
        return False
    def findShortestPath(self, start, end, expected, board):
        if self.verbose: print start, end
        startVert = board.vertices[start]
        seen = []
        paths = []
        for r in board.getVertexToEdges(startVert):
            if r.getOwner() != None and r.getOwner() != self.AI.playerNumber:
                    continue
            seen.append(r.index)
            paths.append([r.index])
        if self.verbose: print seen, paths
        curLen = 1
        while(True):
            curLen += 1
            if curLen > expected:
                if self.verbose: print "warning curLen has surpassed expected path length"
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
                                if self.verbose: print new, curLen
                                return new
            paths = temp
                

            if curLen > 6:
                break
        if self.verbose: print paths
    def makeExchange(self, cost, board, locObj, players, typeS):
        for r in self.AI.resources:
            if r not in cost:
                cost[r] = 0
        modCost = cost.copy()
        for r in modCost:
            modCost[r] -= self.AI.resources[r]
        if self.verbose: print modCost, "mccc"
        while(self.needsExchange(cost)):
            if self.verbose: print cost, modCost
            exchange = self.findNeed(modCost, self.income)
            if self.verbose: print exchange
            sortRes = []
            for r in self.AI.resources:
                if r in self.AI.structures['ports']:
                    sortRes.append((self.AI.resources[r] - cost[r] + 2, self.income[r], r))
                elif 'three' in self.AI.structures['ports']:
                    sortRes.append((self.AI.resources[r] - cost[r] + 1, self.income[r], r))
                else:
                    sortRes.append((self.AI.resources[r] - cost[r], self.income[r], r))
            sortRes.sort(key=lambda tup: tup[1], reverse=True)
            sortRes.sort(key=lambda tup: tup[0], reverse=True)
            if self.verbose: print sortRes
            if sortRes[0][0] < 4:
                if locObj == -1:
                    if self.verbose: print "failed to find reasonable exchange to reduce hand size"
                else:
                    if self.verbose: print "something went wrong, it doesnt appear the " + typeS + " can be built"
                return False
            r = sortRes[0][2]
            exNum = 4
            if r in self.AI.structures['ports']:
                exNum = 2
                if self.verbose: print "Port being used for 2 : 1 exchange"
            elif 'three' in self.AI.structures['ports']:
                exNum = 3
                if self.verbose: print "Port being used for 3: 1 exchange"
            if self.verbose: print "exchange", r , "for", exchange
            self.AI.resources[r] -= exNum
            self.AI.resources[exchange] += 1
            modCost[exchange] -= 1
            if locObj == -1:
                return True
            '''
            if typeS == 'city' and self.AI.canBuildCity(locObj):
                print "exchanges done"
                return True
            '''
            if not self.needsExchange(cost):
                if self.verbose: print "exchanges done"
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
        if self.verbose: print "the ai is executing option", bestOptionKey, bestOption
        if bestOption['backtrace'][0] == 'settlement':
            settleLoc = int(bestOptionKey[:2])
            if bestOptionKey in self.savedPaths:
                path = self.savedPaths[bestOptionKey]
            else:
                path = self.findShortestPath(bestOption['backtrace'][1], settleLoc, bestOption['backtrace'][2], board)
            predRoadsAway = bestOption['backtrace'][2]
            roadsAway = len(path)
            for r in path:
                if r in self.AI.structures['roads']:
                    roadsAway -= 1
            cost = self.getResourceCost('settlement', roadsAway)
            if roadsAway > predRoadsAway:
                newTurnCost = self.getCostInTurns('settlement', roadsAway, self.income)
                if newTurnCost > 0:
                    self.savedPaths[bestOptionKey] = path
                    if self.verbose: print "A planned road for this settlement has been built on, the Ai can no longer complete this option this turn"
                    return False  
            settleObj = board.vertices[settleLoc]
            if not self.needsExchange(cost):
                for i in xrange(len(path)):
                    roadInd = path[i]
                    if roadInd in self.AI.structures['roads']:
                        continue
                    locObj = board.edges[roadInd]
                    self.AI.buildRoad(locObj, board)
                self.AI.buildSettlement(settleObj, board)
                if self.verbose:
                    print settleObj.getCity()
                    print settleObj.getSettlement()
                    print "owner checks settlement"
                self.updateIncome(settleObj, board)
                if self.verbose: 
                    board.createBatchCSV(players)
		    board.batchUpdate()
		    print board.printBoard()
	            print "the AI has built a settlement"
	        return True
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
                    if self.verbose:
                        print settleObj.getCity()
                        print settleObj.getSettlement()
                        print "owner checks settlement"
                    if self.verbose:
                        board.createBatchCSV(players)
		        board.batchUpdate()
		        print board.printBoard()
                        print "the AI has built a settlement after some resource reallocation"
                    return True
        elif bestOption['backtrace'][0] == 'city':
            if self.verbose: print "time to upgrade our chosen loc"
            cost = self.getResourceCost('city', 0)
            if self.verbose: print cost
            if self.verbose: print self.AI.resources
            locObj = board.vertices[bestOption['backtrace'][1]]
            if self.AI.canBuildCity(locObj):
                self.AI.buildCity(locObj, board)
                self.updateIncome(locObj, board)
                if self.verbose:
                    print locObj.getCity()
                    print locObj.getSettlement()
                    print "owner checks city"
                if self.verbose: 
                    board.createBatchCSV(players)
		    board.batchUpdate()
		    print board.printBoard()
                    print "the AI has built a city"
                return True
            else:
                #the following needs to be decomped later
                cost = self.getResourceCost('city', 0)
                if self.makeExchange(cost, board, locObj, players, 'city'):
                    self.AI.buildCity(locObj, board)
                    self.updateIncome(locObj, board)
                    if self.verbose:
                        print locObj.getCity()
                        print locObj.getSettlement()
                        print "owner checks city"
                    if self.verbose: 
                        board.createBatchCSV(players)
                        board.batchUpdate()
                        print board.printBoard()
                        print "the AI has built a city after some resource reallocation"
                    return True
        elif bestOption['backtrace'][0] == 'dev':
            if self.verbose: print "getting tactical with a dev card"
        else:
            if self.verbose: print "something strange has happened, an wild option appears, the ai will reevaluate"
        
        return False   
        
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
      if self.verbose: print "decide move start"
      if firstTurn:
          self.overallScarcity = self.getOverallScarcity(board)
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
          if self.verbose: print builtSettlementSpot, "roadOptions", roadOptions
          if self.verbose: print "currently just choosing the first road on the list" # Currentliy just building at the first option
          roadChoice = board.edges[roadOptions[0]]
          self.AI.buildRoad(roadChoice, board) 
      else:
        #sys.exit()
        curDistanceAway = 2
        devCardCost = sum(self.getResourceCost('devCard', 0).values())
        options = {}
        curSettlements = self.AI.structures['settlements'][:]
        curSettlements += self.AI.structures['cities'][:]
        if self.AI.settlementsRemaining > 0:
            while(True):
                for settlement in curSettlements:
                    s = board.vertices[settlement]
                    playableLocations = self.findPlayableLocations(s,curDistanceAway,board)
                    for playableS in playableLocations:
                        #ideally object to ascii
                        benefit = self.evaluateLocationBenefit(playableS, board)
                        asciiRepresentation = str(board.vertexToAscii[playableS])
                        if asciiRepresentation in self.savedPaths:
                            roadsAway = len(self.savedPaths[asciiRepresentation])
                        else:
                            roadsAway = curDistanceAway
                        turnCost = self.getCostInTurns('settlement', roadsAway, self.income)
                        resCost = self.getResourceCost('settlement', roadsAway)
                        cent = self.getCentrality(board, playableS)
                        options[asciiRepresentation] = {'incomeIncrease': benefit, 'costInTurns' : turnCost, 'costInRes' : resCost, 'centrality' : cent, 'backtrace' : ['settlement', settlement, roadsAway]}
                        if playableS.index in self.portsMap.keys():
                            options[asciiRepresentation]['port'] = self.portsMap[playableS.index]
                if ((len(options) >= 7 and curDistanceAway >= 3) or curDistanceAway >= 5):
                    break
                curDistanceAway += 1
        if self.verbose: 
          print ""
          print "settlements",self.AI.structures['settlements']
          print "cities",self.AI.structures['cities']
          print ""
        if self.AI.citiesRemaining > 0:      
            for settle in self.AI.structures['settlements']:
                s = board.vertices[settle]
                benefit = self.evaluateLocationBenefit(s, board)
                turnCost = self.getCostInTurns('city', 0, self.income)
                resCost = self.getResourceCost('city', 0)
                asciiRepresentation = str(board.vertexSettlementAscii(s))
                #cent = self.getCentrality(board, s)
                options[asciiRepresentation] = {'incomeIncrease': benefit, 'costInTurns' : turnCost, 'costInRes' : resCost, 'backtrace' : ['city', settle, 0]}
          #need to add more options and expand the curDistanceAway
        if self.verbose: print options
        bestOptionKey = self.evaluateOptions(options, players, board)
        if self.verbose: print bestOptionKey
        bestOption = options[bestOptionKey[0]]
        self.savedBestOpt = [bestOptionKey, bestOption]


        if bestOptionKey[0] == 'pass':
            "The wise Ai has contemplated all its options and decided to pass"
            return
        if type(bestOption) == str:
            print "error####################"
            print bestOption
            print bestOptionKey[0]
        if bestOption['costInTurns'] == 0:

                if self.execute(players, board, bestOption, bestOptionKey[0], options) and self.getVictoryPoints() < 10:
                    if self.verbose: print "the Ai is checking for more actions"
                    self.decideMove(players, board, firstTurn)
                    return self.getVictoryPoints()
        else:
            if self.verbose: print "The Ai will pass for now, its planning something!"
        vp = self.getVictoryPoints()
        if vp == 10:
            if self.verbose: print self.AI.structures['settlements'], "Settlements"
            if self.verbose: print self.AI.structures['cities'], "cities"
            #board.createBatchCSV(players)
	    #board.batchUpdate()
	    #print board.printBoard()
            return vp
        #handle over 7 cards in hand

        if sum(self.AI.resources.values()) > 7 and bestOptionKey[0] != 'pass':
            curPath = None
            counter = 0 
            cost = 0
            cost = self.getResourceCost(bestOption['backtrace'][0], bestOption['backtrace'][2])
            while sum(self.AI.resources.values()) >=7:
                counter += 1
                if counter >= 20:
                    break
                changeMade = False
                if bestOption['backtrace'][0] == 'settlement':
                    if self.AI.resources['brick'] >= 1 and self.AI.resources['wood'] >= 1 and self.AI.roadsRemaining > 0 and curPath != []:
                       if curPath == None:
                            curPath = self.findShortestPath(bestOption['backtrace'][1], int(bestOptionKey[0][:2]), bestOption['backtrace'][2], board)
                            self.savedPaths[bestOptionKey[0]] = curPath
                            trash = []
                            for r in curPath:
                                if r in self.AI.structures['roads']:
                                    trash.append(r)
                            for r in trash:
                                curPath.remove(r)
                            if curPath == []:
                                continue
                       roadInd = curPath[0]
                       locObj = board.edges[roadInd]
                       self.AI.buildRoad(locObj, board)
                       cost['brick'] -= 1
                       cost['wood'] -= 1
                       curPath.remove(roadInd)
                       changeMade = True
                       if self.verbose:
                           board.createBatchCSV(players)
		           board.batchUpdate()
		           print board.printBoard()
                           print "the AI has built a road at", roadInd, "to reduce its hand size"
                if not changeMade:
                    if max(self.AI.resources.values()) >= 4 or self.possiblePortEx():
                        if self.makeExchange(cost, board, -1, players, bestOption['backtrace'][0]):
                            changeMade = True
                            if self.verbose: print "the AI has made a bank exchange to reduce its hand size"
                            
                if not changeMade:
                    break
        #end 7 cards in hand handle

        return vp
    def possiblePortEx(self):
        maxi = max(self.AI.resources.values())
        if maxi == 1:
            return False
        if maxi >= 3:
            if 'three' in self.AI.structures['ports']:
                return True
        elif maxi >= 2:
            for r in self.AI.resources:
                if self.AI.resources[r] ==2 and r in self.AI.structures['ports']:
                    return True
        return False
    def evaluateOptions(self, options, players, board):
        overallScarcity = self.overallScarcity
        soonScarcity = self.getSoonScarcity(players, board)
        curNormS = self.getCurrentNormalizedScarcity(players)
        scarceWeightsInc = self.scarceWeightsInc
        scarceWeightsCost = self.scarceWeightsCost
        bestOption = ""
        bestScore = -float('inf')
        for opt in options:
            score = 0.0
            for field in options[opt]:
                    if field not in self.weights:
                        continue
                    elif field == 'incomeIncrease':
                        total = 0.0
                        for r in self.AI.resources:
                            total += scarceWeightsInc['overall']  * options[opt][field][r] * overallScarcity[r]
                            total += scarceWeightsInc['soon']  * options[opt][field][r] * soonScarcity[r]
                            total += scarceWeightsInc['cur']  * options[opt][field][r] * curNormS[r]
                            total += scarceWeightsInc['gross']  * options[opt][field][r]
                        #print total, "inc"
                        score += total * self.weights['incomeIncrease']
                    elif field == 'costInRes':
                        total = 0.0
                        for r in self.AI.resources:
                            total += scarceWeightsCost['overall']  * options[opt][field][r] * overallScarcity[r]
                            total += scarceWeightsCost['soon']  * options[opt][field][r] * soonScarcity[r]
                            total += scarceWeightsCost['cur']  * options[opt][field][r] * curNormS[r]
                            total += scarceWeightsCost['gross']  * options[opt][field][r]
                        #print total, "cost"
                        score += total * self.weights['costInRes']
                    elif field == 'port':
                        if options[opt][field] in self.AI.structures['ports']:
                            continue
                        if options[opt][field] == 'three':
                             sortInc = []
                             for r in self.income:
                                sortInc.append((self.income[r]))
                             sortInc.sort(reverse=True)
                             avg = (sortInc[0] + sortInc[1])/2.0
                             score += avg * self.weights[field] * 2.0/3.0
                        else:
                           score += self.income[options[opt][field]] * self.weights[field]     
                    elif field == 'costInTurns': 
                        vp = self.getVictoryPoints()
                        if vp == 7:
                            score += options[opt][field] * self.weights[field] * 5
                        elif vp >= 8:
                            score += options[opt][field] * self.weights[field] * 50
                        else:
                            score += options[opt][field] * self.weights[field]      
                    else:
                        score += options[opt][field] * self.weights[field]
                    
            if score > bestScore:
                bestOption = opt
                bestScore = score
        return bestOption, bestScore
    def placeRobber(self, board):
        bestTile = board.asciiToTile['01T']
        maxDamage = 0
        for tile in board.getAllTiles():
          badChoice = False
          if tile.robber == True or tile.getType() == "desert": # can't option not to move the robber
            badChoice = True
            continue 
          vertexes = board.getTileToVertices(tile)
          occupiedSpots = 0
          for vertex in vertexes:
            if vertex.getOwner() == self.AI.playerNumber:
              badChoice = True
              break
            if vertex.getOwner() != None:
              if vertex.getSettlement() != self.AI.playerNumber:
                occupiedSpots += 1+self.diceProbs[tile.getNumber()]
              elif vertex.getCity() != self.AI.playerNumber:
                occupiedSpots += 2+self.diceProbs[tile.getNumber()]
              else:
                if self.verbose: print "weirdness in placing robber"
          if badChoice == True: # one of AI settlements is here
            continue
          else:
            if occupiedSpots > maxDamage:
              bestTile = tile
              maxDamage = occupiedSpots
        if self.verbose: print "best selection was", board.tileToAscii[bestTile]
        newRobberLocation = bestTile
        # newRobberLocation = board.asciiToTile['01T']
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
        if self.verbose: print self.AI.roadsRemaining

    def getCentrality(self,board,vertex): # advanced version gives distance to the edge
        returnable = self.vertexToCentralityMap[vertex.getIndex()]
        return returnable
        # OLD VERSION
        # neighborTiles = board.getVertexToTiles(vertex)
        # return len(neighborTiles)
        # USE case  
            # for vertex in board.getAllVertices():
            # print "vertex",vertex
            # self.getCentrality(board,vertex) 
    def getOverallScarcity(self,board):
        scarcity = {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        for tile in board.getAllTiles():
          tileType = tile.getType()
          tileNum = tile.getNumber()
          if tileType == "desert":
            continue
          scarcity[tileType] += self.diceProbs[tileNum]
        scarcity = self.reciprocalAndNormalize(scarcity)
        return scarcity

    def getSoonScarcity(self,players,board):
        scarcity = {'wood':0.01, 'sheep':0.01, 'brick': 0.01, 'ore': 0.01, 'grain' : 0.01}
        ALLsettlements = self.AI.structures['settlements'][:]
        ALLcities = self.AI.structures['cities'][:]

        for player in players:
          if(player == self):
            continue
          ALLsettlements += player.structures['settlements']
          ALLcities += player.structures['cities']


        ALLsettlements = list(set(ALLsettlements))
        ALLcities = list(set(ALLcities))

        for settlement in ALLsettlements:
          vertex = board.vertices[settlement]
          tiles = board.getVertexToTiles(vertex)
          for tile in tiles:
            tileType = tile.getType()
            tileNum = tile.getNumber()
            if tileType == "desert":
              continue
            scarcity[tileType] += self.diceProbs[tileNum]
        for city in ALLcities:
          vertex = board.vertices[city]
          tiles = board.getVertexToTiles(vertex)
          for tile in tiles:
            tileType = tile.getType()
            tileNum = tile.getNumber()
            if tileType == "desert":
              continue
            scarcity[tileType] += self.diceProbs[tileNum]
            scarcity[tileType] += self.diceProbs[tileNum]
        scarcity = self.reciprocalAndNormalize(scarcity)
        return scarcity

    def getCurrentScarcity(self,players):
        scarcity = {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        for player in players:
          if(player == self):
            AIresources = self.AI.resources
            for res in AIresources:
              scarcity[res] += AIresources[res]
            continue
          playerRes = player.resources
          for res in playerRes:
            scarcity[res] += playerRes[res]
        return scarcity

    def getCurrentNormalizedScarcity(self,players):
        scarcity = self.getCurrentScarcity(players)
        scarcity = self.reciprocalAndNormalize(scarcity,True)
        return scarcity

    def reciprocalAndNormalize(self,scarcity,laplace = False):
        done = scarcity
        # inverse
        for res in scarcity:
          if laplace == True:
            scarcity[res] += 1.0
          done[res] = 1.0 / float(scarcity[res])
        # normalize
        factor=1.0/sum(done.itervalues())
        for res in done:
          done[res] = done[res]*factor
        return done


    def handleDiscard(self):
        sortRes = []
        if sum(self.AI.resources.values()) <= 7:
            return
        numLost = sum(self.AI.resources.values())
        numLost /= 2
        if self.verbose: print "The ai must discard", numLost, "resources"
        bestMove = self.savedBestOpt
        if bestMove[0] == None:
            cost = {'wood': 0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
        else:
            cost = self.getResourceCost(bestMove[1]['backtrace'], bestMove[1]['backtrace'][2])
        for r in self.AI.resources:
             sortRes.append([self.AI.resources[r] - cost[r], self.income[r], r])
        sortRes.sort(key=lambda tup: tup[1], reverse=True)
        sortRes.sort(key=lambda tup: tup[0], reverse=True)
        while (numLost > 0):
            excess = sortRes[0][0]
            if excess <= 0:
                if self.resources[sortRes[0][2]] == 0:
                    del sortRes[0]
                else:
                    self.resources[sortRes[0][2]] -=1
                    numLost -= 1
                    sortRes[0][0] -= 1
                    #if self.verbose: 
                    if self.verbose: print "The ai has discared 1", sortRes[0][2]
            else:
                if excess >= numLost:
                    self.AI.resources[sortRes[0][2]] -= numLost
                    if self.verbose: print "The ai has discared", numLost, sortRes[0][2]
                    numLost = 0                  
                    break
                else:
                    self.AI.resources[sortRes[0][2]] -= excess
                    numLost -= excess
                    sortRes[0][0] -= excess
                    if self.verbose: print "The ai has discared", excess, sortRes[0][2]
            sortRes.sort(key=lambda tup: tup[1], reverse=True)
            sortRes.sort(key=lambda tup: tup[0], reverse=True)
