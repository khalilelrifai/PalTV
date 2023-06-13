from ftplib import FTP

from django.conf import settings
from django.db import models
from django.db.models import *


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    upload_status = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ftp_exists = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def check_ftp_exists(self):
        try:
            ftp = FTP(settings.FTP_HOST)
            ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
            ftp.cwd(settings.FTP_UPLOAD_DIR)
            file_name = self.title
            files_List = [file_name.replace('videos/', '').split('.')[0] for file_name in ftp.nlst('videos/')]
            file_exists = file_name in files_List
            print(files_List)
            self.ftp_exists = file_exists
            self.save()
            ftp.quit()
        except Exception as e:
            # Handle FTP connection or error exception here
            self.ftp_exists = False
            self.save()
