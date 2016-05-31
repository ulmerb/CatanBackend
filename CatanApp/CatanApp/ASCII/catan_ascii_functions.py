import os
import sys
import fileinput
import json
# import settings
# ^Use import settings when server is not running
# otherwise use from CatanApp import settings
import settings

# IS_RUNNING is True when the django server is running
if settings.IS_RUNNING:
	asciiPath = os.path.join(settings.BASE_DIR, "ASCII/")
else:
	asciiPath = "ASCII/"

def printBoard(currentBoardNum):
 	filein = asciiPath + "catan_example" + str(currentBoardNum) + ".txt"
	f = open(filein,'r')
	filedata = f.read()
	print filedata
	f.close()
	return filedata

def replaceText(old,new,currentBoardNum):
	filein = asciiPath + "catan_example" + str(currentBoardNum) + ".txt"
	fileout = asciiPath + "catan_example" + str(currentBoardNum + 1) + ".txt"
	f = open(filein,'r')
	filedata = f.read()
	f.close()
	# print "old", old, 'new ', new
	newdata = filedata.replace(old,new)
	f = open(fileout,'w')
	f.write(newdata)
	# print newdata
	f.close()

def verify(boardNum):
	filein = asciiPath + "catan_example" + str(boardNum) + ".txt"
	f = open(filein,'r')
	filedata = f.read()
	# roads
	print "Road Search"
	for i in xrange(1,72):
		output =""
		if(i < 10):
			output = "0"+str(i)+"R"
		else:
			output = str(i)+"R"
		if output not in filedata:
			print "NOT FOUND",output
	print "Road Search Done"
	# vertexes
	print "Vertex Search"
	for i in xrange(1,55):
		output =""
		if(i < 10):
			output = "0"+str(i)+"V"
		else:
			output = str(i)+"V"
		if output not in filedata:
			print "NOT FOUND",output
	print "Vertext Search Done"
	# tiles
	print "Tile Search"
	for i in xrange(1,20):
		output =""
		if(i < 10):
			output = "0"+str(i)+"T"
		else:
			output = str(i)+"T"
		if output not in filedata:
			print "NOT FOUND",output
	print "Tile Search Done"

	# ports
	print "Port Search"
	for i in xrange(1,10):
		output = "port"+str(i)
		if output not in filedata:
			print "NOT FOUND",output
	print "Port Search Done"
	f.close()

def batchUpdate(curBoardNum):
	fileData = open(asciiPath + "latest_update.csv",'r')
	lines = [line.rstrip('\n').rstrip('\r') for line in fileData]
	fileData.close()
	for line in lines:
		result = line.split(',')
		old = result[0]
		new = result[1]
		replaceText(old,new,curBoardNum)
		curBoardNum += 1
	printBoard(curBoardNum)
	return curBoardNum

def undo(curBoardNum):
	current = asciiPath + "catan_example" + str(curBoardNum) + ".txt"
	previous = asciiPath + "catan_example" + str(curBoardNum - 1) + ".txt"
	f = open(previous,'r')
	filedata = f.read()
	f.close()
	f = open(current,'w')
	f.write(filedata)
	f.close()

def replace(curBoardNum, old, new):
	replaceText(old,new,curBoardNum)
	curBoardNum += 1
	printBoard(curBoardNum)
	return curBoardNum

def buildRoad(curBoardNum,location,player):
	output = "!R"+player
	replaceText(location,output,curBoardNum)
	curBoardNum += 1
	printBoard(curBoardNum)
	return curBoardNum

def buildSettlement(curBoardNum, location, player, settlementNumber):
	output = settlementNumber+"S"+player
	replaceText(location,output,curBoardNum)
	curBoardNum += 1
	printBoard(curBoardNum)
	return curBoardNum

def buildCity(curBoardNum, location, player):
	output = "!C"+player
	replaceText(location,output,curBoardNum)
	curBoardNum += 1
	printBoard(curBoardNum)
	return curBoardNum


def build(curBoardNum, subCommand, location=None, player=None, settlementNumber=None):
	if(subCommand == "road"):
		return buildRoad(curBoardNum,location,player)
		
	if(subCommand == "settlement"):
		return buildSettlement(curBoardNum,location,player,settlementNumber)
		
	if(subCommand=="city"):
		return buildCity(curBoardNum, location, player)
	
def main():
	currentBoardNum = 1
	currentCommands = ["batch update", "verify","undo","print board","replace","build","formatting","help"]
	while(True):
		print("Enter a Command")
		command = raw_input("> ")


# 		jsondata = simplejson.dumps(data, indent=4, skipkeys=True, sort_keys=True)
# 		fd = open(filename, 'w')
# 		fd.write(jsondata)
# 		fd.close()
		if(command == "JSON Output"):
			filein = "catan_example" + str(currentBoardNum) + ".txt"
			with open(filein) as f:
				content = f.readlines()
				jsondata = json.dumps(content)
				fd = open("jsonOutput.json",'w')
				fd.write(jsondata)
				fd.close()
				print "downloaded to jsonOutput.json, all lines seperated into an array"
				f.close()

		if(command == "batch update"):
			subCommand = raw_input("What is the name and location of the update file?")
			foundFile = False
			fileData = 0
			while foundFile == False:
				try:
					fileData = open(subCommand,'r')
					foundFile = True
				except IOError:
					subCommand =raw_input("Incorrect file name try again\n>")
			lines = [line.rstrip('\n') for line in fileData]
			fileData.close()
			print lines
			for line in lines:
				result = line.split(',')
				old = result[0]
				new = result[1]
				print old, new
				replaceText(old,new,currentBoardNum)
			currentBoardNum += 1
			printBoard(currentBoardNum)


		if(command=="verify"):
			filein ="catan_example" + str(currentBoardNum) + ".txt"
			f = open(filein,'r')
			filedata = f.read()
			# roads
			print "Road Search"
			for i in xrange(1,72):
				output =""
				if(i < 10):
					output = "0"+str(i)+"R"
				else:
					output = str(i)+"R"
				if output not in filedata:
					print "NOT FOUND",output
			print "Road Search Done"
			# vertexes
			print "Vertex Search"
			for i in xrange(1,55):
				output =""
				if(i < 10):
					output = "0"+str(i)+"V"
				else:
					output = str(i)+"V"
				if output not in filedata:
					print "NOT FOUND",output
			print "Vertext Search Done"
			# tiles
			print "Tile Search"
			for i in xrange(1,20):
				output =""
				if(i < 10):
					output = "0"+str(i)+"T"
				else:
					output = str(i)+"T"
				if output not in filedata:
					print "NOT FOUND",output
			print "Tile Search Done"

			# ports
			print "Port Search"
			for i in xrange(1,10):
				output = "port"+str(i)
				if output not in filedata:
					print "NOT FOUND",output
			print "Port Search Done"
			f.close()


		if(command=="undo"):
			current = "catan_example" + str(currentBoardNum) + ".txt"
			previous = "catan_example" + str(currentBoardNum - 1) + ".txt"
			f = open(previous,'r')
			filedata = f.read()
			f.close()
			f = open(current,'w')
			f.write(filedata)
			f.close()

		if(command=="print board"):
	 		filein = "catan_example" + str(currentBoardNum) + ".txt"
			f = open(filein,'r')
			filedata = f.read()
			print filedata
			f.close()

		if(command=="replace"):
			old =  raw_input("What are you replacing (use full numbering)? ")
			new = raw_input("Replace with this (use full numbering): ")
			replaceText(old,new,currentBoardNum);
			currentBoardNum += 1
			printBoard(currentBoardNum)

		if(command=="build"):
			subCommand = raw_input("What do you want to build? ('road','settlement','city')")
			if(subCommand == "road"):
				location = raw_input("What location (use full numbering '03R')?")
				player = raw_input("Which player are you? (1-4)")
				output = "!R"+player
				replaceText(location,output,currentBoardNum)
				currentBoardNum += 1

			if(subCommand == "settlement"):
				location = raw_input("What location (use full numbering ie '02V')?")
				player = raw_input("Which player are you? (1-4)")
				settlementNumber = raw_input("Which Settlement is this? (1-5)")
				output = settlementNumber+"S"+player
				replaceText(location,output,currentBoardNum)
				currentBoardNum += 1

			if(subCommand=="city"):
				location = raw_input("What location (use full numbering ie '1S1')?")
				player = raw_input("Which player are you? (1-4)")
				output = "!C"+player
				replaceText(location,output,currentBoardNum)
				currentBoardNum += 1
			printBoard(currentBoardNum)

		if(command =="help"):
			print "Current Commands are"
			for l in currentCommands:
				print "- ",l

		if(command =="formatting"):
	 		filein = "BoardFormatting.txt"
			f = open(filein,'r')
			filedata = f.read()
			print filedata
			f.close()
# main()


	


