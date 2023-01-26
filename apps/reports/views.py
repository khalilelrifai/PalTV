import re
from datetime import datetime, timedelta

from django import template
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views.generic import *

from .forms import *
from .models import *


class DetailView(DetailView):
    model=Journalist_Report
    template_name='home/details.html'
    context_object_name = 'set_details'
    
    
    def get_queryset (self):
        return Journalist_Report.objects.filter(id=self.kwargs['pk'])
    
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('approve')=='approve':
            self.model.objects.filter(id=self.kwargs['pk']).update(status='Approved')
            return HttpResponseRedirect('/submitted-report/1')



class ReportsListView(ListView):
    model=Journalist_Report
    paginate_by = 10
    submitted_template='home/submitted-report.html'
    profile_template ='home/profile.html'
    all_template ='home/all.html'
    queryset = Journalist_Report.objects.all().order_by('-date')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today=datetime.now().date()
        last_week = datetime.now().date() - timedelta(days=7)
        last_month= datetime.now().date() - timedelta(days=30)
        today_count=Journalist_Report.objects.filter(date=today).count()
        last_week_count=Journalist_Report.objects.filter(date__gte=last_week).count()
        last_month_count=Journalist_Report.objects.filter(date__gte=last_month).count()
        
        context["today"]=today_count
        context["week"]=last_week_count
        context["month"]=last_month_count
        return context
    
    def get_template_names(self) :
        
        if 'profile' in self.request.path.split('/'):      
            return [self.profile_template]
        elif 'all' in self.request.path.split('/'): 
            return [self.all_template]
        return [self.submitted_template]
            

class EditReportView(UpdateView):
    model=Journalist_Report
    



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/main.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def edit_report(request,id):
    
    context = {}
    
    context['segment'] =  request.path.split('/')
    
    
    
    work_type_list=[i[0] for i in Journalist_Report.WORK_DESCRIPTION]
    set_details = Journalist_Report.objects.get(id=id)
    context['set_details'] = set_details
    context['work_type'] = work_type_list
    
    
   
    work_type=request.GET.get('work_type')
    task_info=request.GET.get('task')
    if request.GET.get('save')=='save':
        Journalist_Report.objects.filter(id=id).update(work_type=work_type,task=task_info)
        return HttpResponseRedirect('/submitted-report')


    html_template = loader.get_template('home/editform.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def reportform(request):
    context = {} 
    context['segment'] =  request.path.split('/')

    try:

        
        default_id = Journalist_Report._meta.get_field('report_id').default
        user_id = request.user.id
        current_user = Employee.objects.get(employee_id=user_id)
        date = datetime.now()
        work_type_list=[i[0] for i in Journalist_Report.WORK_DESCRIPTION]
        form=JournalistForm(request.GET)


        
        if request.method == "GET":
            work_type=request.GET.get('work_type')
            task_info=request.GET.get('task')
            
            data=Journalist_Report(employee_id=current_user.id,work_type=work_type,date=date,task=task_info)
            if form.is_valid():
                data.save()
                form=JournalistForm()
                
        
        
        
        context['employee']=current_user
        context['date']=date
        context['work_type']=work_type_list
        context['form']=form
        context['default_id']=default_id
                


        html_template = loader.get_template('home/reportform.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


    
    
    
    
    

