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


@permission_required('assignment.view_video')
def video_list(request):
    videos = Video.objects.all()
    list = ftp_list()
    for video in videos:
        if video.title in list:
            video.ftp_exists = True
    
    return render(request, 'assignment/list.html', {'videos': videos})



class VideoListView(View):
    template_name = 'assignment/list.html'
    paginate_by = 10

    def get(self, request):
        strval = request.GET.get("search", False)
        
        if request.user.is_authenticated:
            if strval:
                query = Q(description__icontains=strval)
                query.add(Q(title__icontains=strval), Q.OR)

                video_list = Video.objects.filter(query).select_related().order_by('-uploaded_at')
            else:
                video_list = Video.objects.all().order_by('-uploaded_at')
                
            paginator = Paginator(video_list, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {

                'page_obj':page_obj,
                'search': strval,
            }

            return render(request, self.template_name, context)