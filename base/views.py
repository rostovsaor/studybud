from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse

rooms = [
    {'id': 1, 'name': 'Lets learn python'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend Developers'},
]

def home(request):
    context = {'rooms':rooms}
    # return HttpResponse('Home page')
    return render(request, 'base/home.html', context)

def room(request):
    # return HttpResponse('ROOM')
    return render(request, 'base/room.html')

