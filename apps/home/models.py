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
    id=AutoField(primary_key=True,editable=False)
    user = OneToOneField(User,on_delete=CASCADE)
    department = ForeignKey(Department,on_delete=SET_NULL,null=True)



    def __str__(self):
        return self.user.first_name +" " +self.user.last_name

    @property
    def fullname(self):
        return self.user.first_name +" "+self.user.last_name