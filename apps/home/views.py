# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

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
from django.views.generic import ListView, View

from .forms import *
from .models import *

# class AllKeywordsView(ListView):
#     model = Journalist_Report
#     template_name = "home/test.html"


# def listing_api(request):
#     page_number = request.GET.get("page", 1)
#     per_page = request.GET.get("per_page", 5)
#     startswith = request.GET.get("startswith", "")
#     keywords = Journalist_Report.objects.filter(
#         report_id__startswith=startswith
#     )
#     paginator = Paginator(keywords, per_page)
#     page_obj = paginator.get_page(page_number)
#     data = [{"report_id": kw.report_id,"work_type":kw.work_type,'date':kw.date,'status':kw.status,'employee':kw.employee.fullname} for kw in page_obj.object_list]

#     payload = {
#         "page": {
#             "current": page_obj.number,
#             "has_next": page_obj.has_next(),
#             "has_previous": page_obj.has_previous(),
#         },
#         "data": data
#     }
#     return JsonResponse(payload)



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
def submitted_form(request,page):
    context = {}
    context['segment'] =  request.path.split('/')


    # lst=[]
    # get_all_data = reverse(Journalist_Report.objects.all().order_by('date'))

    get = Journalist_Report.objects.all().order_by('date')
    paginator = Paginator(get,per_page=10)
    page_object =paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)

    context['show']=page_object

    #context["show"]=get_all_data
       
    html_template = loader.get_template('home/submitted-report.html')
    return HttpResponse(html_template.render(context, request))






@login_required(login_url="/login/")
def profile(request,page):
    context = {}
    context['segment'] =  request.path.split('/')



    today=datetime.now().date()
    last_week = datetime.now().date() - timedelta(days=7)
    last_month= datetime.now().date() - timedelta(days=30)
    today_count=Journalist_Report.objects.filter(date=today).count()
    last_week_count=Journalist_Report.objects.filter(date__gte=last_week).count()
    last_month_count=Journalist_Report.objects.filter(date__gte=last_month).count()

    get = Journalist_Report.objects.all().order_by('date')
    paginator = Paginator(get,per_page=10)
    page_object =paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)

    context['show']=page_object
    
    context["today"]=today_count
    context["week"]=last_week_count
    context["month"]=last_month_count
       
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


    
    
    
    
    

