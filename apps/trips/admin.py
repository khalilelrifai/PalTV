

from django.contrib import admin

from .models import *

# class VehicleAdmin(admin.ModelAdmin):
#     list_display =  ('id',)
    
    
class TripAdmin(admin.ModelAdmin):
    list_display = ('driver', 'vehicle', 'destination', 'verified_by', 'check_in', 'check_out')

admin.site.register(Trip, TripAdmin)

admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(QrCode)
admin.site.register(Security)


