# from multiprocessing import context
# from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.

# rooms = [
#   {'id': 1, 'name': 'Lets learn python'},
#   {'id': 2, 'name': 'Design with me'},
#   {'id': 3, 'name': 'Frontend Developers'},
# ]

def loginPage(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    username = request.POST.get('username').lower()
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username) #no real need to instatiate user in this line as this instance only exists here this once
    except:
      messages.error(request, 'Username or password does not exist')
    
    user = authenticate(request, username=username, password=password)

    if user:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or password does not exist.')
    
  context = {'page': page}
  return render(request, 'base/login_register.html', context)


def logoutUser(request):
  logout(request)
  return redirect('home')


def registerPage(request):
  form = UserCreationForm()

  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error occurred during registration')

  context = {'form': form}
  return render(request, 'base/login_register.html', context)


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
  room_messages = room.message_set.all().order_by('-created')
  participants = room.participants.all()

  if request.method == 'POST':
    message = Message.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('room', pk=room.id)

  context = {'room': room, 'room_messages': room_messages, 'participants': participants}
  return render(request, 'base/room.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room) # prefils the form

  if request.user != room.host:
    return HttpResponse('You are not the owner!')

  if request.method == 'POST':
    form = RoomForm(request.POST, instance = room) #specifying which room to update with the data submitted in the request
    if form.is_valid():
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)

  if request.user != room.host:
    return HttpResponse('You are not the owner!')

  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': room})