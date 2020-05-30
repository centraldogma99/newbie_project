from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'title', 'description', 'color', 'start_time', 'end_time', 'author']