from django.shortcuts import redirect, render
from django.views.generic import *
from formtools.wizard.views import *

from .forms import *
from .models import Bulletin

from django.shortcuts import redirect
from django.views.generic.edit import FormView


from .forms import *
from .models import Bulletin

# FORMS = [
#     ('step1', BulletinStep1Form),
#     ('step2', BulletinStep2Form),
#     ('step3', BulletinStep3Form),
#     ('step4', BulletinStep4Form),
#     ('step5', BulletinStep5Form),
# ]

# TEMPLATES = {
#     'step1': 'bulletin_step1.html',
#     'step2': 'bulletin_step2.html',
#     'step3': 'bulletin_step3.html',
#     'step4': 'bulletin_step4.html',
#     'step5': 'bulletin_step5.html',
# }

# class BulletinWizardView(SessionWizardView):
#     template_name = 'bulletin_wizard.html'
#     form_list = FORMS

#     def get_form_initial(self, step):
#         initial = self.initial_dict.get(step, {})
#         if step == 'step5':
#             initial.update({'type': self.get_cleaned_data_for_step('step1')['type'],
#                             'time': self.get_cleaned_data_for_step('step1')['time'],
#                             'resources': self.get_cleaned_data_for_step('step2')['resources'],
#                             'producers': self.get_cleaned_data_for_step('step3')['producers'],
#                             'editors': self.get_cleaned_data_for_step('step4')['editors']})
#         return initial

#     def done(self, form_list, **kwargs):
#         bulletin = Bulletin()
#         for form in form_list:
#             bulletin.__dict__.update(form.cleaned_data)
#         bulletin.save()
#         return redirect('bulletin_list')




class BulletinListView(ListView):
    model = Bulletin
    template_name = 'bulletins/bulletin_list.html'


class BulletinDetailView(View):
    def get(self, request, bulletin_id):
        bulletin = Bulletin.objects.get(id=bulletin_id)
        return render(request, 'bulletins/bulletin_detail.html', {'bulletin': bulletin})

class CreateBulletinView(View):
    def get(self, request):
        form = BulletinForm()
        return render(request, 'bulletins/create_bulletin.html', {'form': form})

    def post(self, request):
        form = BulletinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bulletins:list')
        return render(request, 'bulletins/create_bulletin.html', {'form': form})
