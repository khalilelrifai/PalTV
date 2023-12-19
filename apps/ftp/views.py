import time
from ftplib import FTP

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import *

from .forms import VideoForm
from .models import *




def upload_file_to_ftp(file, ftp, new_file_name, video):
    chunk_size = 64 * 1024  # 64KB
    total_size = file.size
    bytes_uploaded = 0
    start_time = time.time()

    with file.open('rb') as file_stream:
        while True:
            chunk = file_stream.read(chunk_size)
            if not chunk:
                break
            ftp.storbinary(f'APPE {new_file_name}', ContentFile(chunk))
            bytes_uploaded += len(chunk)
            
            # Calculate progress and estimated time
            progress = bytes_uploaded / total_size
            elapsed_time = time.time() - start_time
            if progress > 0:
                estimated_time = elapsed_time / progress - elapsed_time
            else:
                estimated_time = 0
            
            # Update the video object with progress and estimated time
            uploaded_file_size = ftp.size(new_file_name)


            video.upload_status = f' Progress: {progress:.2%}. Estimated time: {estimated_time:.2f}s'
            video.save()
            if uploaded_file_size == total_size:
                video.in_progress = False
                break





class VideoUploadView(PermissionRequiredMixin,FormView):
    permission_required = 'ftp.add_video'
    template_name = 'ftp/upload.html'
    form_class = VideoForm
    success_url = 'ftp:my_list'

    def form_valid(self, form):
        video = form.save(commit=False)
        video.owner = self.request.user
        video.upload_status = 'Uploading...'
        video.in_progress = True
        video.save()

        try:
                # Upload the video file to the FTP server
                with FTP(settings.FTP_HOST) as ftp:
                    ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
                    ftp.cwd(settings.FTP_UPLOAD_DIR)

                    # Get the title from the form
                    title = form.cleaned_data['title']
                    file = self.request.FILES['file']
                    
                    # Generate new file name using the title
                    new_file_name = f'{title}.mp4'

                    ftp.cwd('videos')
                    
                    upload_file_to_ftp(file, ftp, new_file_name, video)
                            
                # Update the video object after successful upload
                video.upload_status = 'Uploaded successfully!'
                video.in_progress = False
                video.save()
                return redirect('ftp:my_list')
        except Exception as e:
            video.upload_status = f'Upload failed: {str(e)}'
            video.in_progress = False
            video.save()
            return redirect('ftp:video_list')


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
    ftp_file_list = ftp_list()
    for video in videos:
        video.ftp_exists = video.title in ftp_file_list
        video.save()

        
class VideoListView(PermissionRequiredMixin,ListView):
    permission_required = 'ftp.view_video'
    model = Video
    template_name = 'ftp/list.html'
    context_object_name = 'videos'
    paginate_by = 10
    def get_queryset(self):
        video_exist()
        queryset = Video.objects.filter().order_by('-uploaded_at')
        return queryset


class OwnerVideoListView(PermissionRequiredMixin,ListView):
    permission_required = 'ftp.add_video'
    model = Video
    template_name = 'ftp/list.html'
    context_object_name = 'videos'
    paginate_by = 10
    def get_queryset(self):
        video_exist()
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user).order_by('-uploaded_at')
        return queryset
        
class VideoDetailView(PermissionRequiredMixin,DetailView):
    permission_required = 'ftp.view_video'
    model = Video
    template_name= "ftp/video_detail.html"
    
    
    
class UpdateStatus(View):
    def get(self, request):
        videos = Video.objects.filter(in_progress=True)
        result = {}
        for video in videos:
            result[video.id] = video.upload_status
        if result:
            return JsonResponse(result, safe=False)
        else:
            return HttpResponse(status=204)


