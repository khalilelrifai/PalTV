from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name='assignment'


urlpatterns = [
    path('', login_required(VideoUploadView.as_view()), name='main'),
    path('upload/',login_required(VideoUploadView.as_view()), name='upload_video'),
    path('videoslist/', login_required(VideoListView.as_view()), name='video_list'),
    path('mylist/', login_required(OwnerVideoListView.as_view()), name='my_list'),
    path('list/detail/<int:pk>/', login_required(VideoDetailView.as_view()), name='video_detail'),
    path('status/', UpdateStatus.as_view(), name='status'),
]
