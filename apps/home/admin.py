from django.contrib import admin

from .models import *

class RAdmin(admin.ModelAdmin):

    list_display =['fullname','location','department']

admin.site.register(Employee,RAdmin)
admin.site.register(Department)
admin.site.register(Job_title)
