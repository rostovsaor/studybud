from django.db import models

# Create your models here.

class Room(models.Model):
  # host =
  # topi =
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  # participants = 
  updated = models.DateTimeField(auto_now=True) #whenever something changes
  created = models.DateTimeField(auto_now_add=True) #only once, when object created

  def __str__(self):
    return self.name
  