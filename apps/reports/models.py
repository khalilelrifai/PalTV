from django.contrib.auth.models import User
from django.db.models import *



# def journalist_id():
#     year = datetime.now().year

#     if not (Journalist_Report.objects.values_list('id',flat=True)) :
#         form ="01-JN-{}".format(year)
#     else :
#         id=(Journalist_Report.objects.last()).report_id
#         lst=id.partition('-')
#         form="{}-JN-{}".format(int(lst[0]) + 1 ,year)
#     return form


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


WORK_DESCRIPTION=(
    ('','Please select your task type'),
    ('VT','VT'),
    ('OOV','OOV'),
    ('SB','SB'),
    ('CAP','CAP'),
    ('GFX','GFX'),
    ('Filler','Filler'),
)








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

class Task_type(Model):
    id=AutoField(primary_key=True,editable=False)
    job_title=ForeignKey(Job_title,on_delete=CASCADE,null=True)
    type = CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.type
    
class Employee(Model):
    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    job_title = ForeignKey(Job_title,on_delete=SET_NULL,null=True)


    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name


class Report(Model):
    STATUS_CHOICES= (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    )
    id=AutoField(primary_key=True,editable=False)
    employee=ForeignKey(Employee,on_delete=SET_NULL,null=True)
    task_type=ForeignKey(Task_type,on_delete=SET_NULL,null=True)
    created_at=DateTimeField(auto_now_add=True)
    status=CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    description=TextField(null=True)


    def __str__(self):
        return str(self.employee)

    # class Meta:
    #     permissions=[('can_view_submitted_reports','Can View Submitted Reports'),('can_view_journalists_profiles','Can View Journalists Profiles'),(('can_view_all','Can View Journalists ALL'))]
