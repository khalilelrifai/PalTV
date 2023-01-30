from django.forms import *

from .models import *


class CreateReportForm(ModelForm):
    
    class Meta:
        model = Report
        fields='__all__'
        
        widgets = { 
            'employee':TextInput(attrs={}),
            'task_type': Select(attrs={}),
            'description': Textarea(attrs={'rows':'4'}),
        }
        
    # def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user')
    #    super(CreateReportForm, self).__init__(*args, **kwargs)
    #    self.fields['task_type'].queryset = Task_type.objects.filter(user=user)
        
        
        
        # labels = {
        #     'employee': ('Name'),
        #     'ren_date': ('Renewal Date'),
        # }




# class DriverForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields='__all__'
#         widgets = { 
#             'dob': forms.DateInput(attrs={'type':'date'}),
#             'address':forms.Textarea(attrs={'rows':'4'}),
#         }

# class SecurityForm(forms.ModelForm):
#     class Meta:
#         model = Security
#         fields='__all__'
#         widgets = { 
#             'dob': forms.DateInput(attrs={'type':'date'}),
#             'address':forms.Textarea(attrs={'rows':'4'}),
#         }
        
# class AssetForm(forms.ModelForm):
#     class Meta:
#         model = Asset
#         fields='__all__'
#         widgets = { 
#             'reg_date': forms.DateInput(attrs={'type':'date'}),
#             'ren_date': forms.DateInput(attrs={'type':'date'})
#         }
#         labels = {
#             'reg_date': ('Registeration Date'),
#             'ren_date': ('Renewal Date'),
#         }
        
        
# class TripForm(forms.ModelForm):
#     class Meta:
#         model = Trip
#         fields='__all__'
            
        
