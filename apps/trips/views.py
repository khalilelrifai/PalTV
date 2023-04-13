import cv2
import qrcode
from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from django.views.generic import DetailView
from .models import Trip, Vehicle
from django.urls import reverse
from django.shortcuts import get_object_or_404

def scan_qr_code(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
    except Vehicle.DoesNotExist:
        raise Http404('Vehicle not found')
    
    # Retrieve the last trip for the vehicle
    last_trip = Trip.objects.filter(vehicle=vehicle).order_by('-created_at').first()
    
    if last_trip:
        # Redirect the user to the trip detail page for the last trip
        return redirect(reverse('trip_detail', args=[last_trip.id]))
    else:
        raise Http404('No trips found for this vehicle')



def home(request):
   if request.method=="POST":
      Url=request.POST['url']
      QrCode.objects.create(url=Url)

   qr_code=QrCode.objects.all()
   return render(request,"home.html",{'qr_code':qr_code})