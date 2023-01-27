from django import template
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
    model = Report
    form_class = CreateReportForm
    success_url = reverse_lazy('reports:main')
    
    

# class NewDriver(LoginRequiredMixin,CreateView):
#     form_class = DriverForm
#     model = Driver
#     success_url = reverse_lazy('home:home')


    
    
    
    
    

