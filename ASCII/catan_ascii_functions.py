
import os
import sys
import fileinput
import json

def printBoard(currentBoardNum):
 	filein = "catan_example" + str(currentBoardNum) + ".txt"
	f = open(filein,'r')
	filedata = f.read()
	print filedata
	f.close()

def replaceText(old,new,currentBoardNum):
	filein = "catan_example" + str(currentBoardNum) + ".txt"
	fileout = "catan_example" + str(currentBoardNum + 1) + ".txt"
	f = open(filein,'r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace(old,new)
	f = open(fileout,'w')
	f.write(newdata)
	# print newdata
	f.close()

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
			for i in xrange(1,54):
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

main()


	


