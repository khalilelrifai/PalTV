

from django.contrib import admin

from .models import Employee,Task_type,Department,Report,Job_title


class RAdmin(admin.ModelAdmin):

    list_display =['id','employee','task_type','created_at']

admin.site.register(Report,RAdmin)
admin.site.register(Employee)
admin.site.register(Task_type)
admin.site.register(Department)
admin.site.register(Job_title)

