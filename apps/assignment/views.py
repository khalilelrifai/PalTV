from django.shortcuts import render, redirect
from .forms import VideoForm
from ftplib import FTP
from .models import *
from django.conf import settings

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # Upload the video file to the FTP server
            ftp = FTP(settings.FTP_HOST)
            ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
            ftp.cwd(settings.FTP_UPLOAD_DIR)
            with open(video.file.path, 'rb') as file:
                ftp.storbinary(f'STOR {video.file.name}', file)
            ftp.quit()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {'form': form})

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/list.html', {'videos': videos})
