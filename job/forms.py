from django import forms
from .models import *

class regform(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    contact = forms.CharField(max_length=20)
    date = forms.DateField()
    qualification = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20)
    cpassword = forms.CharField(max_length=20)


class logform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=20)


class jobform(forms.Form):
    companyname = forms.CharField(max_length=20)
    email = forms.EmailField()
    jobtitle = forms.CharField(max_length=20)
    worktype = forms.CharField(max_length=20)
    experience = forms.CharField(max_length=20)
    jobtype = forms.CharField(max_length=20)

class jobapplyform(forms.ModelForm):
    class Meta:
        model = jobapply
        fields = '__all__'
