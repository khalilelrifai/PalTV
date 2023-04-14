from django import forms

from .models import Trip


class TripApproveForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=Trip.STATUS_CHOICES)
