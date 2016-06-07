from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import Controller
import Player
import Board
import Location
import Devcards
import Ai
import ASCII.catan_ascii_functions as asc
import settings
import Devcards


def makeJson(board, players, message, diceRoll=0, curPlayer=0, card=0, canTrade=False, take=None, offer=None, proposer=None, discarding=False):
    data = {}
    data['message'] = message
    data['currentDiceRoll'] = diceRoll
    data['numPlayers'] = len(players)
    data['currentPlayer'] = curPlayer
    data["robberTileLocation"] = board.tileToAscii[board.robberTile]
    data["players"] = []
    data["boardString"] = board.printBoard()
    for p in players:
        if hasattr(p, 'AI'):
            pInfo = {"victoryPoints": p.AI.score}
            pInfo['resources'] = p.AI.resources
            pInfo["devCards"] = {}
            pInfo["index"] = p.AI.playerNumber
            pInfo["devCardsPlayed"] = {}
            pInfo["ports"] = p.AI.structures['ports']
            for card in p.AI.devCardsHeld:
                if card in pInfo["devCards"]:
                    pInfo["devCards"][card] += 1
                else:
                    pInfo["devCards"][card] = 1

            for card in p.AI.devCardsPlayed:
                if card in pInfo["devCardsPlayed"]:
                    pInfo["devCardsPlayed"][card] += 1
                else:
                    pInfo["devCardsPlayed"][card] = 1

            # stubs to be updated
            pInfo["hasLongestRoad"] = False
            pInfo["hasLongestArmy"] = (board.largestArmy == p.AI.playerNumber)
            for key in p.AI.structures:
                pInfo[key] = p.AI.structures[key]
            data["players"].append(pInfo)
        else:
            pInfo = {"victoryPoints": p.score}
            pInfo['resources'] = p.resources
            pInfo["devCards"] = {}
            pInfo["index"] = p.playerNumber
            pInfo["devCardsPlayed"] = {}
            pInfo["ports"] = p.structures['ports']
            for card in p.devCardsHeld:
                if card in pInfo["devCards"]:
                    pInfo["devCards"][card] += 1
                else:
                    pInfo["devCards"][card] = 1

            for card in p.devCardsPlayed:
                if card in pInfo["devCardsPlayed"]:
                    pInfo["devCardsPlayed"][card] += 1
                else:
                    pInfo["devCardsPlayed"][card] = 1

            # stubs to be updated
            pInfo["hasLongestRoad"] = False
            pInfo["hasLongestArmy"] = (board.largestArmy == p.playerNumber)
            for key in p.structures:
                pInfo[key] = p.structures[key]
            data["players"].append(pInfo)
    data['devCardName'] = card
    data['canTrade'] = canTrade
    data['take'] = take
    data['offer'] = offer
    data['proposer'] = proposer
    return json.dumps(data)

# Intialize game


@csrf_exempt
def newGame(request):
    info = json.loads(request.POST['js_resp'])
    numPlayers = info['numPlayers']
    AI = info['AI']
    board, players = Controller.tileInitialization(numPlayers, AI)
    settings.BOARD = board
    settings.PLAYERS = players
    settings.DEVCARDS = Devcards.devcards()
    # convert board, players, newNum into json response
    resp = makeJson(board, players, "Player 0, place your first settlement")
    return HttpResponse(resp)


@csrf_exempt
def build(request):
    pass


@csrf_exempt
def endOfTurn(request):
    info = json.loads(request.POST['js_resp'])
    newCurPlayer = int(info['currentPlayer'] + 1) % len(settings.PLAYERS)
    dRoll = Controller.rollDice(
        settings.BOARD, settings.PLAYERS, newCurPlayer)
    if isAI(newCurPlayer):
        if dRoll == 7:
            settings.PLAYERS[newCurPlayer].placeRobber(settings.BOARD)
            newCurPlayer = int(
                newCurPlayer + 1) % len(settings.PLAYERS)  # should be 0
            dRoll = Controller.rollDice(
                settings.BOARD, settings.PLAYERS, newCurPlayer)
            settings.BOARD.createBatchCSV(settings.PLAYERS)
            settings.BOARD.batchUpdate()
            return HttpResponse(makeJson(settings.BOARD, settings.PLAYERS, "Ai placed robber, " + "Player " + str(newCurPlayer) + " turn", dRoll, newCurPlayer))
        else:
            settings.PLAYERS[newCurPlayer].decideMove(
                settings.PLAYERS, settings.BOARD, True)
            newCurPlayer = int(
                newCurPlayer + 1) % len(settings.PLAYERS)  # should be 0
            dRoll = Controller.rollDice(
                settings.BOARD, settings.PLAYERS, newCurPlayer)
            settings.BOARD.createBatchCSV(settings.PLAYERS)
            settings.BOARD.batchUpdate()
            print "LATEST BOARD"
            print settings.BOARD.printBoard()
            return HttpResponse(makeJson(settings.BOARD, settings.PLAYERS, "Ai moved, " + "Player " + str(newCurPlayer) + " turn", dRoll, newCurPlayer))
    else:
        if dRoll == 7:
            resp = makeJson(
                settings.BOARD, settings.PLAYERS, "Robber!", dRoll, newCurPlayer)
        else:
            resp = makeJson(
                settings.BOARD, settings.PLAYERS, "Player " + str(newCurPlayer) + " turn", dRoll, newCurPlayer)
    return HttpResponse(resp)


@csrf_exempt
def placeRobber(request):
    info = json.loads(request.POST['js_resp'])
    loc = int(info['tilePosition'])
    target = int(info['playerToStealFrom'])
    curPlayer = int(info['currentPlayer'])
    print "old board number", settings.BOARD.currentBoardNumber
    if isAI(target):
        settings.PLAYERS[target].handleDiscard()
        return HttpResponse(makeJson(settings.BOARD, settings.PLAYERS, "Ai has discarded, " + "Player " + str(curPlayer) + "'s turn", 7, curPlayer))

    error = Controller.serverHandleRobber(
        curPlayer, settings.PLAYERS, loc, target, settings.BOARD, len(settings.PLAYERS) - 1)
    print "new board number", settings.BOARD.currentBoardNumber
    # print settings.BOARD.printBoard()
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 7, curPlayer)
    else:
        resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " + str(target) +
                        ": choose half of your cards to discard", 7, target, 0, False, None, None, None, True)
    return HttpResponse(resp)


@csrf_exempt
def playerHandleDiscard(request):
    pass


@csrf_exempt
def buildRoad(request):
    info = json.loads(request.POST['js_resp'])
    suggestedLocation = info['suggestedLocation']
    curPlayer = info['curPlayer']
    error = Controller.serverBuildRoad(
        curPlayer, settings.PLAYERS, settings.BOARD, suggestedLocation)
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "road build successfull", 0, curPlayer)

    return HttpResponse(resp)


@csrf_exempt
def buildSettlement(request):
    info = json.loads(request.POST['js_resp'])
    suggestedLocation = info['suggestedLocation']
    curPlayer = info['curPlayer']
    error = Controller.serverBuildSettlement(
        curPlayer, settings.PLAYERS, settings.BOARD, suggestedLocation)
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "settlement build successfull", 0, curPlayer)

    return HttpResponse(resp)


@csrf_exempt
def buildCity(request):
    info = json.loads(request.POST['js_resp'])
    suggestedLocation = info['suggestedLocation']
    curPlayer = info['curPlayer']
    error = Controller.serverBuildCity(
        curPlayer, settings.PLAYERS, settings.BOARD, suggestedLocation)
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "city build successfull", 0, curPlayer)

    return HttpResponse(resp)


@csrf_exempt
def buyCard(request):
    info = json.loads(request.POST['js_resp'])
    curPlayer = info['curPlayer']
    error, card = settings.PLAYERS[curPlayer].buildDevCard(settings.DEVCARDS)
    if error:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, error, 0, curPlayer, card)
    else:
        resp = makeJson(settings.BOARD, settings.PLAYERS,
                        "succesfully bought devcard", 0, curPlayer, card)

    return HttpResponse(resp)


@csrf_exempt
def playCard(request):
    info = json.loads(request.POST['js_resp'])
    cardType = info['devCardType']
    curPlayer = info['curPlayer']
    devCardBrick = info['devCardBrick']
    devCardWood = info['devCardWood']
    devCardSheep = info['devCardSheep']
    devCardOre = info['devCardOre']
    devCardGrain = info['devCardGrain']
    roadLoc1 = info['roadLoc1']
    roadLoc2 = info['roadLoc2']
    tilePosition = int(info['tilePosition'])
    playerToStealFrom = info['playerToStealFrom']
    error = Controller.serverUseCard(curPlayer, settings.PLAYERS, settings.BOARD, cardType,
                                     devCardBrick, devCardWood, devCardSheep, devCardOre, devCardGrain, roadLoc1, roadLoc2, tilePosition, playerToStealFrom)
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "Devcard played", 0, curPlayer)

    return HttpResponse(resp)


@csrf_exempt
def bankTrade(request):
    info = json.loads(request.POST['js_resp'])
    curPlayer = info['curPlayer']
    give = info['youGiveResource']
    take = info['youWantResource']
    error = settings.PLAYERS[curPlayer].bankTrade(give, take)
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "Successfull transaction", 0, curPlayer)
    return HttpResponse(resp)


@csrf_exempt
def portTrade(request):
    info = json.loads(request.POST['js_resp'])
    curPlayer = info['curPlayer']
    take = info['youWantResource']
    give = info['youGiveResource']
    port = info['tradeType']
    error = settings.PLAYERS[curPlayer].makePortTrade(port, give, take)
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 0, curPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "Successfull port trade", 0, curPlayer)

    return HttpResponse(resp)


def isAI(playerNum):
    return playerNum == len(settings.PLAYERS) - 1


def executeAITrade(curPlayer, ainum, offer, receive, players, board):
    traded = players[ainum].evaluateTrade(offer, receive, players, board)
    if traded:
        for r in offer:
            players[curPlayer].resources[r] -= offer[r]
            players[ainum].AI.resources[r] += offer[r]
            print players[curPlayer]
            print players[ainum].AI
        for r in receive:
            players[curPlayer].resources[r] += receive[r]
            players[ainum].AI.resources[r] -= receive[r]
            print players[curPlayer]
            print players[ainum].AI
        return True
    return False


@csrf_exempt
def playerTrade(request):
    info = json.loads(request.POST['js_resp'])
    curPlayer = info['curPlayer']
    offer = info['offer']
    take = info['take']
    userToTradeWith = info['userToTradeWithArr'][0]
    if isAI(userToTradeWith):
        if executeAITrade(curPlayer, userToTradeWith, offer, take, settings.PLAYERS, settings.BOARD):
            return HttpResponse(makeJson(settings.BOARD, settings.PLAYERS, "AI has accepted trade", 0, curPlayer, 0, True))
        else:
            return HttpResponse(makeJson(settings.BOARD, settings.PLAYERS, "AI has rejected trade", 0, curPlayer, 0, True))

    canTrade, message = settings.PLAYERS[curPlayer].checkTrade(offer)
    if canTrade:
        resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " +
                        str(curPlayer) + " has proposed a trade", 0, userToTradeWith, 0, canTrade, take, offer, curPlayer)
    else:
        resp = makeJson(settings.BOARD, settings.PLAYERS,
                        message, 0, curPlayer, 0, canTrade, take, offer, curPlayer)
    return HttpResponse(resp)


@csrf_exempt
def tradeMaker(request):
    info = json.loads(request.POST['js_resp'])
    proposee = info['curPlayer']
    proposer = info['proposer']
    offer = info['offer']
    take = info['take']
    accepted = info['acceptOrReject']
    canTrade, message = settings.PLAYERS[proposee].checkTrade(take)
    if canTrade:
        if accepted == 'accept':
            print "before trade player 0 resource: ", settings.PLAYERS[proposer].resources, "player 1 resource:", settings.PLAYERS[proposee]
            settings.PLAYERS[proposer].makeTrade(
                offer, take, proposee, settings.PLAYERS)
            print "after trade player 0 resource: ", settings.PLAYERS[proposer].resources, "player 1 resource:", settings.PLAYERS[proposee]

            resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " +
                            str(proposee) + " has accepted your offer", 0, proposer)
        else:
            resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " +
                            str(proposee) + " has rejected your offer", 0, proposer)
    else:
        resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " +
                        str(proposee) + " has rejected your offer", 0, proposer)
    return HttpResponse(resp)
