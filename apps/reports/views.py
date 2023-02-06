from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.models import Group, Permission

from .forms import *
from .models import *


class CreateReport(LoginRequiredMixin,View):
    success_url = reverse_lazy('reports:main')
    template_name = 'reports/report_form.html'

    def get(self,request):
        form=CreateReportForm()
        x = get_object_or_404 (Job_title,employee__user=self.request.user)
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
        data.owner_id = Employee.objects.get(user = self.request.user).id
        data.save()

        return redirect(self.success_url)
    
    
class ReportListView(LoginRequiredMixin,ListView):
    model = Report
    paginate_by = 5
    queryset = Report.objects.filter().order_by('-created_at')
    

class ReportDetailView(LoginRequiredMixin,DetailView):
    model = Report
    template_name= "reports/report_detail.html"
    
    def get_context_data(self, **kwargs) :
        ctx = super().get_context_data(**kwargs)
        ctx['group'] = User.objects.filter(groups__name__contains='director')
        return ctx
     

class ReportUpdateView(LoginRequiredMixin,UpdateView):
    model = Report
    form_class = CreateReportForm
    success_url = reverse_lazy('reports:list')
    template_name = 'reports/report_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        x = get_object_or_404 (Job_title,employee__user=self.request.user)
        context['job_title'] = x
        context['department'] = x.department
        context['form'].fields['task_type'].queryset = Task_type.objects.filter(job_title_id=x.id)
        return context


class ReportDeleteView(LoginRequiredMixin,DeleteView):
    model = Report
    success_url = reverse_lazy('reports:list')
    
    
class DirectiorView(ReportListView):
    template_name = 'reports/director_list.html'
    
    def get_queryset(self):
        x = get_object_or_404(Job_title,employee__user=self.request.user)
        queryset = Report.objects.filter(task_type__job_title=get_object_or_404(Job_title,employee__user=self.request.user)).order_by('-created_at')
        
        return queryset
    
class EmployeeView(ReportListView):
    
    def get_queryset(self):
        queryset = Report.objects.filter(owner__user=self.request.user).order_by('-created_at')
        return queryset
    

def approve(request,pk):
    Report.objects.filter(id=pk).update(status='Approved')
    return redirect('reports:director')
    

    
    
    
    
    

