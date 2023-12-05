from django.contrib.auth.models import User
from django.db.models import *
from apps.home.models import *
from django.db import models



class Guest(models.Model):
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class GuestBooker(models.Model):
    anchor = models.ForeignKey(Employee, on_delete=models.CASCADE, limit_choices_to={'job_title__title': 'Anchor'})
    scheduled_date = models.DateTimeField()
    guests = models.ManyToManyField(Guest)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.anchor.name} - {self.scheduled_date}"

class GuestCSV(models.Model):
    file = models.FileField(upload_to='guest_csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSV File - {self.uploaded_at}"

class Role(Model):
    id=AutoField(primary_key=True,editable=False)
    title=CharField(max_length=50,null=True)

    def __str__(self):
        return self.title

class Task(Model):
    STATUS_CHOICES= (
    ('On Hold', 'On Hold'),
    ('Done', 'Done'),
    )
    id=AutoField(primary_key=True,editable=False)
    owner = ForeignKey(Employee,on_delete=SET_NULL,null=True)
    status=CharField(max_length=50,choices=STATUS_CHOICES,default='On Hold')
    title = CharField(max_length=200)
    created_date = DateTimeField(auto_now_add=True)
    target_date = DateField()
    remarks = TextField(blank=True)
    reviews = TextField(blank=True)
    assigned_to = ManyToManyField(Employee, related_name='tasks')


    def __str__(self):
        return str(self.owner)

    # class Meta:
    #     permissions=[('can_view_submitted_reports','Can View Submitted Reports'),('can_view_journalists_profiles','Can View Journalists Profiles'),(('can_view_all','Can View Journalists ALL'))]
