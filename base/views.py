# from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.
# from django.http import HttpResponse

# rooms = [
#   {'id': 1, 'name': 'Lets learn python'},
#   {'id': 2, 'name': 'Design with me'},
#   {'id': 3, 'name': 'Frontend Developers'},
# ]

def loginPage(request):

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username) #no real need to instatiate user in this line as it will be overwritten after
    except:
      messages.error(request, 'Username or password does not exist')
    
    user = authenticate(request, username=username, password=password)

    if user:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or password does not exist.')
    
  context = {}
  return render(request, 'base/login_register.html', context)

def logoutUser(request):
  logout(request)
  return redirect('home')

def home(request):
  # q = request.GET.get('q') if request.GET.get('q') != None else ''
  # q = request.GET.get('q') if request.GET.get('q') else ''
  q = request.GET.get('q') or ''

  # The i in icontains below defines contains as case insensitive, remove it for case sensitive. There are others such as startswith etc.
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
  )

  topics = Topic.objects.all()
  room_count = rooms.count() # The count() method is faster than the len() method

  context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
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
      form.save() #this saves the form instance in the database
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room) # prefils the form

  if request.method == 'POST':
    form = RoomForm(request.POST, instance = room) #specifying which room to update with the data submitted in the request
    if form.is_valid():
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': room})