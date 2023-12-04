

from django.contrib import admin

from .models import  Report, Task_type


class RAdmin(admin.ModelAdmin):

    list_display =['id','owner','task_type','created_at']

admin.site.register(Report,RAdmin)
admin.site.register(Task_type)


