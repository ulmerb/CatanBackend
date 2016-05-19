from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def djangotest(request):
	z = json.loads(request.POST['js_resp'])
	print z['action']
	return HttpResponse("Hello")
