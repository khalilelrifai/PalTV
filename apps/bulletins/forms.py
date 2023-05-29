from django import forms

from .models import Bulletin


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = '__all__'
