# getResourceCost(buildType,roadsAway)
# Varible one, build type, "road", "settlement", "city", "devCard"
# Variable two, number of roads away
# 
def getResourceCost(buildType,roadsAway):
	cost =  {'wood':0, 'sheep':0, 'brick': 0, 'ore': 0, 'grain' : 0}
	if(buildType == "road"):
		cost['brick'] += 1
		cost['wood'] += 1
	elif (buildType == "settlement"):
		cost['sheep'] += 1
		cost['brick'] += 1
		cost['wood'] += 1
		cost['grain'] += 1
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

def getVictoryPoints():
	return self.AI.getScore();

def getCostInTurns(buildType,roadsAway,incomeMap):
	resCost = getResourceCost(buildType,roadsAway)
	turnCost = 0.0 
	for key in resCost.keys():
		curIncome = incomeMap[key]
		curCost = resCost[key]
		if (curIncome == 0):
			return -1 #sentinel
		else:
			val = curCost / curIncome
			if (val > turnCost):
				turnCost = val
	return turnCost



