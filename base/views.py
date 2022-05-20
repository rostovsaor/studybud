from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse

def home(request):
    # return HttpResponse('Home page')
    return render(request, 'home.html')

def room(request):
    # return HttpResponse('ROOM')
    return render(request, 'room.html')

