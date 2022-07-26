# from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.
# from django.http import HttpResponse

# rooms = [
#   {'id': 1, 'name': 'Lets learn python'},
#   {'id': 2, 'name': 'Design with me'},
#   {'id': 3, 'name': 'Frontend Developers'},
# ]

def home(request):
  rooms = Room.objects.all()
  context = {'rooms': rooms}
  return render(request, 'base/home.html', context)

def room(request, pk):
  room = Room.objects.get(id=pk)
  context = {'room': room}
  return render(request, 'base/room.html', context)

def createRoom(request):
  form = RoomForm()
  if request.method == 'POST':
    print(request.POST) #See Documentation about this
    # Since we are useing a model form, it automatically gets all the data and organizes it
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save() #this saves the model instance in the database
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/room_form.html', context)