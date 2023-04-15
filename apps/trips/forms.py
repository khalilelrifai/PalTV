from django import forms

from .models import Trip
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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

