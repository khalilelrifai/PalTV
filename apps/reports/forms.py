from django import forms

from .models import *


class CreateReportForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields=['task_type','description']
        
        widgets = { 
            # 'owner':TextInput(attrs={'disabled':True}),
            'task_type': forms.Select(attrs={}),
            'description': forms.Textarea(attrs={'rows':'4'}),
        }
        
        labels = {
            'owner': ('Name'),

        }
        
        
class DetailReportForm(forms.ModelForm):
    class Meta:
        fields=['task_type','description']
        widgets = { 
            'owner':forms.TextInput(attrs={'disabled':True}),
            'task_type': forms.Select(attrs={'disabled':True}),
            'description': forms.Textarea(attrs={'rows':'4','disabled':True}),
        }
        
        
        
        
        
class ReportSearchForm(forms.Form):
    search_text =  forms.CharField(
        required = False,
        label='Search name or surname!',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )

    search_age_exact = forms.IntegerField(
        required = False,
        label='Search age (exact match)!'
    )

    search_age_min = forms.IntegerField(
        required = False,
        label='Min age'
    )

    search_age_max = forms.IntegerField(
      required = False,
      label='Max age'
    )
    # def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user')
    #    super(CreateReportForm, self).__init__(*args, **kwargs)
    #    self.fields['task_type'].queryset = Task_type.objects.filter(user=user)
        
        
        




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
            
        
