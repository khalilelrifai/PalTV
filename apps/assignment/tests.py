from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Video
from .forms import VideoForm

class VideoUploadTestCase(TestCase):
    def setUp(self):
        self.upload_url = reverse('assignment:upload_video')
        self.video_list_url = reverse('assignment:video_list')

    def test_successful_video_upload(self):
        # Create a valid video file for upload
        video_file = SimpleUploadedFile("video.mp4", b"video_content", content_type="video/mp4")

        # POST request to upload video
        response = self.client.post(self.upload_url, {'file': video_file})

        # Assert upload success
        self.assertEqual(response.status_code, 302)  # Redirect to video list page
        self.assertEqual(Video.objects.count(), 1)
        video = Video.objects.first()
        self.assertEqual(video.upload_status, 'Uploaded successfully!')
        self.assertTrue(video.check_ftp_exists())

    def test_video_upload_failure(self):
        # Create a mock form with invalid data
        form = VideoForm(data={})

        # POST request with invalid form data
        response = self.client.post(self.upload_url, {'form': form})

        # Assert upload failure
        self.assertEqual(response.status_code, 302)  # Redirect to video list page
        self.assertEqual(Video.objects.count(), 0)

    def test_video_list_display(self):
        # Create some sample videos
        Video.objects.create(upload_status='Uploaded successfully!')
        Video.objects.create(upload_status='Uploading...')
        Video.objects.create(upload_status='Failed')

        # GET request to video list page
        response = self.client.get(self.video_list_url)

        # Assert video list display
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['videos'], Video.objects.all())

    def test_video_list_display_ftp_existence(self):
        # Create a video with "Uploaded successfully!" status and existing file on FTP server
        video = Video.objects.create(upload_status='Uploaded successfully!')
        video.check_ftp_exists = lambda: True  # Mock FTP existence check

        # GET request to video list page
        response = self.client.get(self.video_list_url)

        # Assert video list display with FTP existence check
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['videos'], Video.objects.all())
        self.assertTrue(response.context['videos'][0].check_ftp_exists())

    def test_video_list_display_ftp_nonexistence(self):
        # Create a video with "Uploaded successfully!" status and non-existing file on FTP server
        video = Video.objects.create(upload_status='Uploaded successfully!')
        video.check_ftp_exists = lambda: False  # Mock FTP non-existence check

        # GET request to video list page
        response = self.client.get(self.video_list_url)

        # Assert video list display with FTP non-existence check
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['videos'], Video.objects.all())
        self.assertFalse(response.context['videos'][0].check_ftp_exists())
