

from django.contrib import admin

from .models import  *


class RAdmin(admin.ModelAdmin):

    list_display =['owner','created_date','title']

admin.site.register(Task,RAdmin)


admin.site.register(Guest)
admin.site.register(GuestBooker)
admin.site.register(GuestCSV)
admin.site.register(Role)

