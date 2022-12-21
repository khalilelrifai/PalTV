# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *

class JAdmin(admin.ModelAdmin):

    list_display =['report_id','employee','work_desc','date']

admin.site.register(Journalist_Report,JAdmin)
admin.site.register(Employee)

# Register your models here.
