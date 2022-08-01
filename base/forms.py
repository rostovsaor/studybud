from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
  class Meta:
    model = Room
    # fields = ['name', ]
    fields = '__all__' #if we want to include all fields from the model, except some autogenerated or read-only