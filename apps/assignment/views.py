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


@permission_required('assignment.upload_video')
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.owner = request.user
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
                    file = request.FILES['file']
                    
                    # Generate new file name using the title
                    new_file_name = f'{title}.mp4'

                    ftp.cwd('videos')
                    
                    # Read and upload the file in chunks
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
                            
                # Update the video object after successful upload
                video.upload_status = 'Uploaded successfully!'
                video.in_progress = False
                video.save()
                return redirect('assignment:my_list')

            except Exception as e:
                video.upload_status = f'Upload failed: {str(e)}'
                video.in_progress = False
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
        video.save()

        
class VideoListView(PermissionRequiredMixin,ListView):
    permission_required = 'assignment.admin_user'
    model = Video
    template_name = 'assignment/list.html'
    context_object_name = 'videos'
    paginate_by = 10
    def get_queryset(self):
        video_exist()
        queryset = super().get_queryset()
        queryset = queryset.filter().order_by('-uploaded_at')
        return queryset


class OwnerVideoListView(PermissionRequiredMixin,ListView):
    permission_required = 'assignment.normal_user'
    model = Video
    template_name = 'assignment/list.html'
    context_object_name = 'videos'
    paginate_by = 10
    def get_queryset(self):
        video_exist()
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user).order_by('-uploaded_at')
        return queryset
        
class VideoDetailView(PermissionRequiredMixin,DetailView):
    permission_required = 'assignment.normal_user'
    model = Video
    template_name= "assignment/video_detail.html"
    
    
    
class UpdateStatus(View):
    def get(self, request):
        videos = Video.objects.filter(in_progress=True)
        result = {}
        for video in videos:
            result[video.id] = video.upload_status
        print(result)
        if result:
            return JsonResponse(result, safe=False)
        else:
            return HttpResponse(status=204)


