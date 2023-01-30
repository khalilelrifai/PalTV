from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import *

from .forms import *
from .models import *


class CreateReport(LoginRequiredMixin,CreateView):
    success_url = reverse_lazy('reports:main')
    template_name = 'reports/report_form.html'
    
    def get(self,request):
        form=CreateReportForm()
        x= get_object_or_404 (Job_title,employee__id=self.request.user.id)
        ctx={'form':form}
        ctx['job_title'] = x
        ctx['department'] = x.department
        ctx['form'].fields['task_type'].queryset = Task_type.objects.filter(job_title_id=x.id)
        return render(request,self.template_name,ctx)

    def post(self, request):
        form = CreateReportForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        data = form.save(commit=False)
        data.owner_id=self.request.user.id
        data.status='Pending'
        data.save()

        return redirect(self.success_url)
    
    
    
class ReportListView(LoginRequiredMixin,ListView):
    model = Report
        
    
    
    # def get(self, request):
    #     user =self.request.user
    #     form = CreateReportForm()
    #     x = Employee.objects.filter(id=user.id)
    #     context = {'x':x,'form':form}
    #     return render(request, self.template_name, context)
    
    
    # def get_form_kwargs(self):
    #     kwargs = super(CreateReport, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user.id
    #     return kwargs

    
    # def post(self, request):
    #     form = CreateReportForm(request.POST)
    #     if not form.is_valid():
    #         x = {'form': form}
    #         return render(request, self.template_name, x)
    #     data = form.save()

    #     return redirect(self.success_url)
    



    
    
    
    
    

