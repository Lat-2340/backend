from django.http import HttpResponse

def indexView(request):
  return HttpResponse('Welcome to lostandfound index.')


