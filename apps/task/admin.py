

from django.contrib import admin

from .models import  *




admin.site.register(Task)
admin.site.register(Guest)
admin.site.register(GuestBooker)
admin.site.register(GuestCSV)
admin.site.register(Role)

