from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def djangotest(request):
	# z = json.loads(request.POST['js_resp'])
	# print z['action']
	# return HttpResponse("Hello")
	print request.POST
	return HttpResponse(
	json.dumps({
  "numPlayers": "1",
  "currentPlayer": "1",
  "message": "null",
  "robberTileLocation": "null"})
	)

# Intialize unique game
@csrf_exempt
def initializeGame(request):
	pass
