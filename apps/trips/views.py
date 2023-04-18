
import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import *

from .forms import *
from .models import *


class CreateTripView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trips/trip_form.html'
    form_class = CreateTripForm
    
    success_url = reverse_lazy('trips:main')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



class TripApprove(LoginRequiredMixin,UserPassesTestMixin, View):
    template_name = 'trips/trip_approve.html'
    
    def test_func(self):
        # Check if the user is a Security user
        return self.request.user.security is not None
    
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            return render(request, self.template_name, {'trip': last_trip})
        else:
            raise Http404('No trips found for this vehicle')

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            action = request.POST.get('action')
            if action == 'approve':
                last_trip.status = 'Approved'
                last_trip.verified_by = request.user.security
                last_trip.save()
                return redirect('trip_detail', pk=vehicle.pk)
            elif action == 'reject':
                last_trip.status = 'Rejected'
                last_trip.verified_by = request.user.security
                last_trip.save()
                return redirect('trip_detail', pk=vehicle.pk)
            elif action == 'cancel':
                return redirect('trip_detail', pk=vehicle.pk)
            else:
                return HttpResponseBadRequest('Invalid action')
        else:
            raise Http404('No trips found for this vehicle')
