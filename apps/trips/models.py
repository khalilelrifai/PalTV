import os
from io import BytesIO

import qrcode
from django.contrib.auth.models import User
from django.core.files import File
from django.db.models import *
from PIL import Image, ImageDraw

from core.settings import CORE_DIR


class Vehicle(Model):
    id = AutoField(primary_key=True, editable=False)
    qr_code = ImageField(blank=True,upload_to= 'apps/static/qr_code/vehicles', unique=True)
    make = CharField(max_length=50, null=True)
    model = CharField(max_length=50, null=True)
    license_plate = CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.make} {self.model} ({self.license_plate})'
    def save(self,*args,**kwargs):
        qr_image = qrcode.make(f'{self.make} {self.model} ({self.license_plate})')
        qr_offset = Image.new('RGB',(320,320),'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.make}-{self.model}-({self.license_plate})qr.png'
        stream = BytesIO()
        qr_offset.save(stream,'PNG')
        self.qr_code.save(files_name,File(stream),save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
        
        
        
class Driver(Model):
    id = AutoField(primary_key=True, editable=False)
    user = OneToOneField(User, on_delete=CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name


class Security(Model):
    id = AutoField(primary_key=True, editable=False)
    user = OneToOneField(User, on_delete=CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name

    
    
class Trip(Model):
    

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    
    vehicle = ForeignKey(Vehicle,on_delete=SET_NULL,null=True)
    driver = ForeignKey(Driver, on_delete=SET_NULL,null=True)
    starting_location = CharField(max_length=255,default='Main Branch')
    destination = CharField(max_length=255)
    created_at=DateTimeField(auto_now_add=True)
    check_in = TimeField()
    check_out = TimeField()
    status = CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    verified_by  = ForeignKey(Security, on_delete=SET_NULL,null=True)


    def __str__(self):
        return f'Trip from {self.starting_location} to {self.destination} by {self.driver.fullname}'