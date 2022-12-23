from django import forms

from .models import *


def get_work():
    choices=[]
    get=Journalist_Report.WORK_DESCRIPTION
    for i in get:
        choices.append((i))
    return choices


class JournalistForm(forms.Form):
    
    work_type =forms.CharField(
        widget=forms.Select(choices=get_work(),
            attrs={
                
                "class":"form-select"
            }
        )
    )
    
    task=forms.CharField(
        widget=forms.Textarea(
            attrs=
            {"class":"form-control" ,"placeholder":"Enter your message...", "rows":"5"
            }
        )
    )