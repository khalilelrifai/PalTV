# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
import re

from .forms import *
from .models import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/main.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        print(load_template)
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        

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


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
