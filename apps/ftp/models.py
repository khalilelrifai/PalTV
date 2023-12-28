from ftplib import FTP

from django.conf import settings
from django.db import models
from django.db.models import *
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    upload_status = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ftp_exists = models.BooleanField(default=False)
    owner = ForeignKey(User, on_delete=SET_NULL, null=True)
    in_progress = BooleanField(default=False)

    class Meta:
        permissions = [
            ("normal_user", "Normal User"),
            ("admin_user", "Admin User"),
            ("upload_video", "Upload Video")
        ]

    def __str__(self):
        return self.title
