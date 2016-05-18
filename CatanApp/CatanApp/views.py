from django.http import HttpResponse

def djangotest(request):
	return HttpResponse("Hello this is a test")