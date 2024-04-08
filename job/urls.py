from django.urls import path
from .views import *
from django.contrib import messages

urlpatterns = [
    path('',index),
    path('loginform/',loadloginform),
    path('register/',register),
    path('login/',login),
    path('editprofile/<int:id>',editprofile),
    #company
    path('companylogin/',companylogin),
    path('cregister/',cregister),
    path('send/',send_mail_regis),
    path('verify/<auth_token>',verify),
    path('job/<int:id>',jobs),
    path('show/<int:id>',showjob),
    path('viewjob/<int:id1>/<int:id2>',viewjob),
    path('apply/<int:id1>/<int:id2>',apply),
    path('addjob/',addjob),
    path('applicant/<int:id>',applicant),
    path('viewcompany/',viewcompany),
    path('appliedjob/',appliedjob),
]