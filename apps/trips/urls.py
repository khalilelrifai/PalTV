from django.urls import path

from .views import *

urlpatterns = [

    path('approve/<int:pk>/', TripApprove.as_view(), name='trip_detail'),

]