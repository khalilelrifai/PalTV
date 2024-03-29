from django.db import models
from ftplib import FTP
from django.conf import settings
from django.db.models import *

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    upload_status = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ftp_exists = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def check_ftp_exists(self):
        ftp = FTP(settings.FTP_HOST)
        ftp.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWORD)
        ftp.cwd(settings.FTP_UPLOAD_DIR)
        file_list = ftp.nlst()
        self.ftp_exists = self.file.name in file_list
        self.save()
        ftp.quit()
