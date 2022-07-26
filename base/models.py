from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.


class Topic(models.Model):
  name = models.CharField(max_length=200)
  def __str__(self):
    return self.name

class Room (models.Model):
  host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) #Relationship, Many to one
  # topic = models.ForeignKey('Topic', on_delete=models.CASCADE) use quotes on Topic to hoist the class
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #Relationship, Many to one
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  # participants = 
  updated = models.DateTimeField(auto_now=True) #whenever something changes
  created = models.DateTimeField(auto_now_add=True) #only once, when object created

  def __str__(self):
    return self.name
  
class Message(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE) #Relationship, many to one
  room = models.ForeignKey(Room, on_delete=models.CASCADE) #Relationship, many to one
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True) #whenever something changes
  created = models.DateTimeField(auto_now_add=True) #only once, when object created

  def __str__(self):
    return self.body[0:50] 