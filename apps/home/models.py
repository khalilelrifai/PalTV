# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



# Create your models here.


def journalist_id():
    year = datetime.now().year

    if not (Journalist_Report.objects.values_list('id',flat=True)) :
        form ="01-JN-{}".format(year)
    else :
        id=(Journalist_Report.objects.last()).report_id
        lst=id.partition('-')
        form="{}-JN-{}".format(int(lst[0]) + 1 ,year)
    return form


    

class Employee(models.Model):
    JOB_CHOICES= (
    ('IT', 'IT'),
    ('MCR', 'MCR'),
    ('ETESALAT', 'ETESALAT'),
    ('JOURNALIST', 'JOURNALIST'),
    ('PA', 'PA'),
    ('PRODUCER', 'PRODUCER'),
    ('EDITOR','EDITOR'),
    ('GRAPHIC','GRAPHIC'))
    
    DEP_CHOICES= (
    ('Engineering', 'Engineering'),
    ('NEWS', 'NEWS'),
    ('PROGRAMS', 'PROGRAMS'))
    
    id=models.AutoField(primary_key=True,editable=False)
    employee = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    job_title = models.CharField(max_length=50,choices=JOB_CHOICES,null=True)
    department = models.CharField(max_length=50,choices=DEP_CHOICES,null=True)

    
    def __str__(self):
        return self.employee.first_name +" " +self.employee.last_name

    @property
    def fullname(self):
        return self.employee.first_name +" "+self.employee.last_name




class Journalist_Report(models.Model):
    WORK_DESCRIPTION=(
        ('','Please select your task type'),
        ('VT','VT'),
        ('OOV','OOV'),
        ('SB','SB'),
        ('CAP','CAP'),
        ('GFX','GFX'),
        ('Filler','Filler'),
    )
    id=models.AutoField(primary_key=True,editable=False)
    report_id=models.CharField(max_length=20,default=journalist_id)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    work_desc=models.CharField(max_length=30,choices=WORK_DESCRIPTION)
    date=models.DateField(default=datetime.now)
    task=models.TextField()


    def __str__(self):
        return str(self.id)


