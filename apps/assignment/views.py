from django.shortcuts import render, redirect
from .forms import VideoForm
from ftplib import FTP
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import permission_required
import os
from django.views.generic import *
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

@permission_required('assignment.add_video')
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.owner = request.user
            video.upload_status = 'Uploading...'
            video.save()

            try:
                # Upload the video file to the FTP server
                ftp = FTP(settings.FTP_HOST)
                ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
                ftp.cwd(settings.FTP_UPLOAD_DIR)

                # Get the title from the form
                title = form.cleaned_data['title']
                file = request.FILES['file']
                # Generate new file name using the title
                new_file_name = f'{title}.mp4'

                ftp.cwd('videos')

                # Read the file content and upload it to the FTP server
                file_content = file.read()
                ftp.storbinary(f'STOR {new_file_name}', ContentFile(file_content))
                ftp.quit()

                # Update the video object with the new file name
                video.upload_status = 'Uploaded successfully!'
                video.file = new_file_name
                video.save()

                return redirect('assignment:video_list')

            except Exception as e:
                video.upload_status = f'Upload failed: {str(e)}'
                video.check_ftp_exists()
                video.save()
                return redirect('assignment:video_list')

    else:
        form = VideoForm()

    return render(request, 'assignment/upload.html', {'form': form})


def ftp_list():
    try:
        ftp = FTP(settings.FTP_HOST)
        ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
        ftp.cwd(settings.FTP_UPLOAD_DIR)
        files_List = [file_name.replace('videos/', '').split('.')[0] for file_name in ftp.nlst('videos/')]
        ftp.quit()
    except Exception as e:
        # Handle FTP connection or error exception here
        return False
    
    return files_List



def video_exist():
    videos = Video.objects.all()
    list = ftp_list()
    for video in videos:
        if video.title in list:
            video.ftp_exists = True
        else:
            video.ftp_exists = False
    
    return render(request, 'assignment/list.html', {'videos': videos})
