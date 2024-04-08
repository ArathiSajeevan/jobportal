from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class regmodel(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    contact = models.CharField(max_length=20)
    date = models.DateField(null=True)
    qualification = models.CharField(max_length=30)
    password = models.CharField(max_length=20)

class Companyreg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class job(models.Model):
    companyname = models.CharField(max_length=20)
    email = models.EmailField()
    jobtitle = models.CharField(max_length=20)
    worktype = models.CharField(max_length=20)
    experience = models.CharField(max_length=20)
    jobtype = models.CharField(max_length=20)


class jobapply(models.Model):
    cname = models.CharField(max_length=20)
    email = models.EmailField()
    designation = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    qualification = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    experience = models.CharField(max_length=20)
    image = models.FileField(upload_to="job/static")
