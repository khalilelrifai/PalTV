from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name='ftp'


urlpatterns = [
    path('', TemplateView.as_view(template_name="ftp/main.html"), name='main'),
    path('upload/',VideoUploadView.as_view(), name='upload_video'),
    path('videoslist/', VideoListView.as_view(), name='video_list'),
    path('mylist/', OwnerVideoListView.as_view(), name='my_list'),
    path('list/detail/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('status/', UpdateStatus.as_view(), name='status'),
]
