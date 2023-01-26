

from django.contrib import admin

from .models import *


class JAdmin(admin.ModelAdmin):

    list_display =['report_id','employee','work_type','date']

admin.site.register(Journalist_Report,JAdmin)
admin.site.register(Employee)

# Register your models here.
