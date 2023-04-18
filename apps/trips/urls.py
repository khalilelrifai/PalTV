from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

app_name='trips'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='trips/main.html')), name='main'),
    path('approve/<int:pk>/', TripApprove.as_view(), name='trip_detail'),
    path('create/', CreateTripView.as_view(), name='create'),

]