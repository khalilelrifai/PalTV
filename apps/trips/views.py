import cv2
import qrcode
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import *
from .forms import *

from .models import *


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



# class TripApprove(View):
    
#     def get(self, request, pk):
#         try:
#             vehicle = Vehicle.objects.get(id=pk)
#         except Vehicle.DoesNotExist:
#             raise Http404('Vehicle not found')
        
#         # Retrieve the last trip for the vehicle
#         last_trip = Trip.objects.filter(vehicle=vehicle).order_by('-created_at').first()

        
#         if last_trip:
#             # Return the trip detail page for the last trip
#             return render(request, 'trips/trip_detail.html', {'trip': last_trip})
#         else:
#             raise Http404('No trips found for this vehicle')
        


class TripApprove(View):
    template_name = 'trips/trip_approve.html'
    
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            form = TripApproveForm(instance=last_trip)
            return render(request, self.template_name, {'form': form, 'trip': last_trip})
        else:
            raise Http404('No trips found for this vehicle')

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            form = TripApproveForm(request.POST, instance=last_trip)
            if form.is_valid():
                form.save()
                return redirect('trip_detail', pk=vehicle.pk)
            else:
                return render(request, self.template_name, {'form': form, 'trip': last_trip})
        else:
            raise Http404('No trips found for this vehicle')
