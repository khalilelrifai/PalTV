from django import forms

from .models import *
from django.contrib.auth.models import Group, Permission, User


from django import forms


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'category', 'remarks',
                  'status', 'target_date', 'reviews',]
        widgets = {
            'title': forms.Textarea(attrs={'rows': '1', 'required': True, 'style': 'text-align: right;'}),
            'remarks': forms.Textarea(attrs={'rows': '4', 'style': 'text-align: right;'}),
            'reviews': forms.Textarea(attrs={'rows': '4', 'style': 'text-align: right;'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

        labels = {
            'reviews': ('Director Notes:'),
            'remarks': ('User Notes:'),
        }


class DetailTaskForm(forms.ModelForm):
    class Meta:
        fields = ['task', 'remarks']
        widgets = {
            'owner': forms.TextInput(attrs={'disabled': True}),
            'task': forms.Textarea(attrs={'rows': '2', 'disabled': True}),
            'remarks': forms.Textarea(attrs={'rows': '4', 'disabled': True}),
        }



class TaskFilterForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Employee.objects.values_list('location', flat=True).distinct(),
        empty_label='Select Location',
        required=False
    )
    user = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)