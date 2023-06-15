from django.urls import path
from .views import upload_video, video_list
from django.contrib.auth.decorators import login_required

app_name='assignment'


urlpatterns = [
    path('', login_required(video_list), name='main'),
    path('upload/',login_required(upload_video), name='upload_video'),
    path('list/', login_required(video_list), name='video_list'),
]
