# -*- coding: utf-8 -*-
import Player

class ai:
    
    def __init__(self, board):
        self.AI = Player.player()
        #weights for features
        self.centrality = []
        self.incomeIncrease = 1.0
        self.costInTurns = 1.0
        self.costInRes = 1.0
        self.port = 1.0
        self.vp = 1.0
        self.diceProbs = [0.028,0.056,0.083,0.111,0.139,0.167,0.139,0.111,0.083,0.056,0.028]
        self.income = {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        
    def getBuildLocations(self):
        pass
        
    def updateBuildLocations(self):
        pass
        
    def evaluateLocationCost(self):
        pass
        
    def evaluateLocationBenefit(self, vert):
        tiles = self.board.getVertexToTiles(vert)
        exReturn =  {'wood':0.0, 'sheep':0.0, 'brick': 0.0, 'ore': 0.0, 'grain' : 0.0}
        for tile in tiles:
            tileType = tile.getType()
            if tileType == 'desert':
                continue 
            exReturn[tileType] += self.diceProbs[tile.getNumber() - 2]
        return exReturn
        
        
        
    def decideMove(self):
        pass
               
    def updateIncome(self, vert):
        #anytime we build on a location whether adding a settlment or changing to city
        #our income increases by one settlment of expected value so we can levarge our
        #benefit function
        gain = self.evaluateLocationBenefit(vert)
        for res in gain:
            self.income[res] += gain[res]
        
    def tests(self):
        print self.AI.roadsRemaining
    