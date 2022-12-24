# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import re
from datetime import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse

from .forms import *
from .models import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/main.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def view_report(request,id):
    context = {}
        
    context['segment'] =  request.path.split('/')
        
    set_details = Journalist_Report.objects.get(id=id)
    context['set_details'] = set_details
    
    
    if request.GET.get('approve')=='approve':
        Journalist_Report.objects.filter(id=id).update(status='Approved')
        return HttpResponseRedirect('/submitted-report')
    
    
    
                
    html_template = loader.get_template('home/details.html')
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
def submitted_form(request):
    context = {}
    context['segment'] =  request.path.split('/')



    get_all_data = reversed(Journalist_Report.objects.all().order_by('date'))

    context["show"]=get_all_data
       
    html_template = loader.get_template('home/submitted-report.html')
    return HttpResponse(html_template.render(context, request))






@login_required(login_url="/login/")
def profile(request):
    context = {}
    context['segment'] =  request.path.split('/')



    get_all_data = reversed(Journalist_Report.objects.all().order_by('date'))

    context["show"]=get_all_data
       
    html_template = loader.get_template('home/profile.html')
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
        get_all_data = reversed(Journalist_Report.objects.all().order_by('date'))
        get_report_count=Journalist_Report.objects.values_list('report_id').count()

        
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
        context["show"]=get_all_data
        context['default_id']=default_id
                
        # lst = Journalist_Report.objects.values_list('report_id', flat=True)

        # if load_template in lst:
        #     set_details = Journalist_Report.objects.get(report_id=load_template)
        #     context['set_details'] = set_details
        #     return render(request, 'home/details.html', context)
        
        # x = re.split("x", load_template)
        # if x[0] in lst and x[1]=='edit':
        #     set_details = Journalist_Report.objects.get(report_id=x[0])
        #     context['set_details'] = set_details
            
        #     return render(request, 'home/editform.html', context)
        
        
        # if x[0] in lst and x[1]=='view':
        #     set_details = Journalist_Report.objects.get(report_id=x[0])
        #     context['set_details'] = set_details
        #     if request.method == "GET":
        #         Journalist_Report.objects.filter(report_id=x[0]).update(status='Approved')
            
            
            
            
        #     return render(request, 'home/details.html', context)


        html_template = loader.get_template('home/reportform.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
    
    
    
    

