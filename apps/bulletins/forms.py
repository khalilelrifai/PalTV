from django import forms
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView

from .models import Bulletin


class BulletinStep1Form(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['type', 'time']

class BulletinStep2Form(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['resources']

class BulletinStep3Form(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['producers']

class BulletinStep4Form(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['editors']

class BulletinStep5Form(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = []

class BulletinWizardView(SessionWizardView):
    template_name = 'bulletin_wizard.html'
    form_list = [
        ('step1', BulletinStep1Form),
        ('step2', BulletinStep2Form),
        ('step3', BulletinStep3Form),
        ('step4', BulletinStep4Form),
        ('step5', BulletinStep5Form),
    ]

    def done(self, form_list, **kwargs):
        bulletin = Bulletin()
        for form in form_list:
            bulletin.__dict__.update(form.cleaned_data)
        bulletin.save()
        return redirect('bulletin_list')

