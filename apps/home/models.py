from django.contrib.auth.models import User
from django.db.models import *


class Department(Model):
    id=AutoField(primary_key=True,editable=False)
    department = CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.department
    

class Job_title(Model):
    id=AutoField(primary_key=True,editable=False)
    title=CharField(max_length=50,null=True)
    department = ForeignKey(Department,on_delete=SET_NULL,null=True)
    def __str__(self):
        return self.title

    
class Employee(Model):
    STATUS_CHOICES= (
    ('Gaza', 'Gaza'),
    ('Daffa', 'Daffa'),
    ('Beirut', 'Beirut'),
    ('Syria', 'Syria'),
    ('Tahran', 'Tahran'),
    
    )
    
    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    department = ForeignKey(Department,on_delete=SET_NULL,null=True)
    job_title = ForeignKey(Job_title,on_delete=SET_NULL,null=True)
    location = CharField(max_length=50,choices=STATUS_CHOICES,blank=True)


    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name