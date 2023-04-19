
import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.utils import timezone

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


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    paginate_by = 20
    ordering = ['-created_at']

class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    
    

class TripRequest(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'trips/trip_request.html'

    def test_func(self):
        # Check if the user is a Security user
        return self.request.user.security is not None

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(
            vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            return render(request, self.template_name, {'trip': last_trip})
        else:
            raise Http404('No trips found for this vehicle')

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        last_trip = Trip.objects.filter(
            vehicle=vehicle).order_by('-created_at').first()
        if last_trip:
            action = request.POST.get('action')
            
            if action == 'approve' and last_trip.check_out is not None:
                last_trip.check_in = timezone.now()
                last_trip.status = 'Closed'
                last_trip.save()
                return redirect('trips:trip_request', pk=vehicle.pk)
            elif action == 'approve':
                last_trip.approval_request = 'Approved'
                last_trip.verified_by = request.user.security
                last_trip.check_out = timezone.now()
                last_trip.save()
                return redirect('trips:trip_request', pk=vehicle.pk)
            elif action == 'reject':
                last_trip.approval_request = 'Rejected'
                last_trip.verified_by = request.user.security
                last_trip.save()
                return redirect('trips:trip_request', pk=vehicle.pk)
            elif action == 'cancel':
                return redirect('trips:main')
            else:
                return HttpResponseBadRequest('Invalid action')
        else:
            raise Http404('No trips found for this vehicle')
