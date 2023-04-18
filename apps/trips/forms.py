from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.db.models import Q

from .models import *


class CreateTripForm(forms.ModelForm):
    
    class Meta:
        model = Trip
        fields=['vehicle','driver','starting_location','destination','note']
        
        widgets = { 
            # 'owner':TextInput(attrs={'disabled':True}),
            'vehicle': forms.Select(attrs={}),
            'driver': forms.Select(attrs={}),
            'starting_location': forms.TextInput(attrs={'cols':'4'}),
            'destination': forms.TextInput(attrs={'cols':'4'}),
            'note':forms.Textarea(attrs={'rows':'4'}),
        }
        
        labels = {
            'vehicle': ('Available Cars'),
            'driver': ('Available Drivers'),
            

        }
        
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all vehicles that have only closed trips
        self.fields['vehicle'].queryset = Vehicle.objects.filter(~Q(trip__status='Open') | Q(trip__isnull=True)).distinct()
        # Get all drivers that have only closed trips
        self.fields['driver'].queryset = Driver.objects.filter(~Q(trip__status='Open') | Q(trip__isnull=True)).distinct()

