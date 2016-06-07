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


def makeJson(board, players, message, diceRoll=0, curPlayer=0, card=0, canTrade=False, take=None, offer=None):
    data = {}
    data['message'] = message
    data['currentDiceRoll'] = diceRoll
    data['numPlayers'] = len(players)
    data['currentPlayer'] = curPlayer
    data["robberTileLocation"] = board.tileToAscii[board.robberTile]
    data["players"] = []
    data["boardString"] = board.printBoard()
    for p in players:
        pInfo = {"victoryPoints": p.score}
        pInfo['resources'] = p.resources
        pInfo["devCards"] = {}
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
    print info['currentPlayer']
    newCurPlayer = int(info['currentPlayer'] + 1) % len(settings.PLAYERS)
    dRoll = Controller.rollDice(
        settings.BOARD, settings.PLAYERS, newCurPlayer, -1)
    if dRoll == 7:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "Robber!", dRoll, newCurPlayer)
    else:
        resp = makeJson(
            settings.BOARD, settings.PLAYERS, "not robber", dRoll, newCurPlayer)
    return HttpResponse(resp)


@csrf_exempt
def placeRobber(request):
    info = json.loads(request.POST['js_resp'])
    loc = int(info['tilePosition'])
    target = int(info['playerToStealFrom'])
    curPlayer = int(info['currentPlayer'])
    print "old board number", settings.BOARD.currentBoardNumber
    error = Controller.serverHandleRobber(
        curPlayer, settings.PLAYERS, loc, target, settings.BOARD, -1)
    print "new board number", settings.BOARD.currentBoardNumber
    # print settings.BOARD.printBoard()
    if error:
        resp = makeJson(settings.BOARD, settings.PLAYERS, error, 7, curPlayer)
    else:
        resp = makeJson(settings.BOARD, settings.PLAYERS,
                        "Player " + str(curPlayer) + "'s turn", 7, curPlayer)
    return HttpResponse(resp)


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
    tilePosition = info['tilePosition']
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
def playerTrade(request):
    info = json.loads(request.POST['js_resp'])
    curPlayer = info['curPlayer']
    offer = info['offer']
    take = info['take']
    userToTradeWith = info['userToTradeWithArr'][0]
    canTrade, message = settings.PLAYERS[curPlayer].checkTrade(offer, player)
    if canTrade:
        resp = makeJson(settings.BOARD, settings.PLAYERS, "Player " +
                        str(curPlayer) + " has proposed a trade", 0, userToTradeWith, 0, canTrade, take)
    else:
        resp = makeJson(settings.BOARD, settings.PLAYERS,
                        message, 0, curPlayer, 0, canTrade, take, offer)
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
