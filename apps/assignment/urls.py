from django.urls import path
from .views import upload_video, video_list

app_name='assignment'

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('list/', video_list, name='video_list'),
]
