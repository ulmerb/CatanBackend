from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def djangotest(request):
<<<<<<< Updated upstream
	print request.POST
=======
	print request
	print "nothing"
>>>>>>> Stashed changes
	return HttpResponse("somestring")
