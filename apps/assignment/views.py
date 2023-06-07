from django.shortcuts import render, redirect
from .forms import VideoForm
from ftplib import FTP
from django.conf import settings
from .models import *

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.upload_status = 'Uploading...'
            video.save()
            try:
                # Upload the video file to the FTP server
                ftp = FTP(settings.FTP_HOST)
                ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
                ftp.cwd(settings.FTP_UPLOAD_DIR)
                with open(video.file.path, 'rb') as file:
                    ftp.storbinary(f'STOR {video.file.name}', file)
                ftp.quit()
                video.upload_status = 'Uploaded successfully!'
                video.check_ftp_exists()
                return redirect('assignment:video_list')
            except Exception as e:
                video.upload_status = f'Upload failed: {str(e)}'
                video.check_ftp_exists()
                video.save()
                return redirect('assignment:video_list')
    else:
        form = VideoForm()
    return render(request, 'assignment/upload.html', {'form': form})


def video_list(request):
    videos = Video.objects.all()
    for video in videos:
        if video.upload_status == 'Uploaded successfully!':
            video.check_ftp_exists()
    return render(request, 'videos/list.html', {'videos': videos})




def video_list(request):
    videos = Video.objects.all()
    return render(request, 'assignment/list.html', {'videos': videos})
