from django.forms import ModelForm
from .models import Event
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    

class TimeInput(forms.TimeInput):
    input_type = 'time'
    


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'title', 'color', 'description', 'start_time', 'end_time', 'author']
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'author': forms.TextInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'