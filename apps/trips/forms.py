from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import *


class CreateReportForm(forms.ModelForm):
    
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
        
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(qrcode__isnull=False)
        self.fields['driver'].queryset = Driver.objects.all()
        
        # labels = {
        #     'owner': ('Name'),

        # }
        
        
# class TripApproveForm(forms.ModelForm):
#     class Meta:
#         model = Trip
#         fields = []

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('Approved', 'Approve', css_class='btn-success'))
#         self.helper.add_input(Submit('Rejected', 'Reject', css_class='btn-danger'))

