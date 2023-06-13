from django.shortcuts import render, redirect
from .forms import VideoForm
from ftplib import FTP
from django.conf import settings
from .models import *

import os

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
                
                # Get the title from the form
                title = form.cleaned_data['title']
                file = request.FILES['file']
                # Generate new file name using the title
                new_file_name = f'{title}.mp4'
                
                ftp.cwd('videos')
                

                    # Use the new file name for FTP storage
                ftp.storbinary(f'STOR {new_file_name}', file)
                ftp.quit()
                
                # Update the video object with the new file name
                video.file.name = new_file_name
                video.upload_status = 'Uploaded successfully!'
                video.check_ftp_exists()
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

def video_list(request):
    videos = Video.objects.filter(upload_status='Uploaded successfully!')
    
    for video in videos:
        video.check_ftp_exists()
    
    return render(request, 'assignment/list.html', {'videos': videos})

