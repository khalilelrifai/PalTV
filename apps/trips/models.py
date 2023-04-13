
from io import BytesIO

import qrcode
from django.contrib.auth.models import User
from django.core.files import File
from django.db.models import *
from django.urls import reverse
from PIL import Image, ImageDraw
import random


class QrCode(Model):
    
   url=URLField(default='http://127.0.0.1:8000/trips/detail/')
   image=ImageField(upload_to='qrcode',blank=True)

   def save(self,*args,**kwargs):
      qrcode_img=qrcode.make(self.url)
      canvas=Image.new("RGB", (400,400),"white")
      draw=ImageDraw.Draw(canvas)
      canvas.paste(qrcode_img)
      buffer=BytesIO()
      canvas.save(buffer,"PNG")
      self.image.save(f'image{random.randint(0,9999)}.png',File(buffer),save=False)
      canvas.close()
      super().save(*args,**kwargs)
      
      


class Vehicle(Model):
    id = AutoField(primary_key=True, editable=False)
    qrcode = OneToOneField(QrCode,on_delete=SET_NULL,null=True,blank=True)
    make = CharField(max_length=50, null=True)
    model = CharField(max_length=50, null=True)
    license_plate = CharField(max_length=10, unique=True)


    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # call the original save method to save the instance
        if not self.qrcode:
            url = f"http://127.0.0.1:8000/trips/detail/{self.id}/"
            qrcode_instance = QrCode.objects.create(url=url)
            self.qrcode = qrcode_instance
            self.save()

    def __str__(self):
        return f'{self.make} {self.model} ({self.license_plate})'
    
        
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
    check_in = TimeField(null=True,blank=True)
    check_out = TimeField(null=True,blank=True)
    status = CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    verified_by  = ForeignKey(Security, on_delete=SET_NULL,null=True,blank=True)


    def __str__(self):
        return f'Trip from {self.starting_location} to {self.destination} by {self.driver.fullname}'