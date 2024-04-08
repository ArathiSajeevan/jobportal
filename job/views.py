import uuid

from django.conf.global_settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate
# from userauth.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


#main page
def index(request):
    return render(request,'index.html')

#load login function
def loadloginform(request):
    return render(request,'login.html')

#register
def register(request):
    if request.method == 'POST':
        a = regform(request.POST)
        if a.is_valid():
            nm = a.cleaned_data['name']
            em = a.cleaned_data['email']
            cn = a.cleaned_data['contact']
            date = a.cleaned_data['date']
            qn = a.cleaned_data['qualification']
            pas = a.cleaned_data['password']
            cpas = a.cleaned_data['cpassword']

            if pas == cpas:
                b = regmodel(name=nm,  email=em, contact=cn, date=date, qualification=qn,password=pas)
                b.save()
                # return HttpResponse("Successfully Registered")
                return redirect(login)
            else:
                return HttpResponse("password and cpassword not match!")
        else:
            return HttpResponse("Enter valid data")
    return render(request, 'register.html')

#login
def login(request):
    if request.method == 'POST':
        a = logform(request.POST)
        if a.is_valid():
            em = a.cleaned_data['email']
            pas = a.cleaned_data['password']
            b = regmodel.objects.all()
            for i in b:
                if em==i.email and pas==i.password:
                    id = i.id
                    nm = i.name
                    em = i.email
                    cn = i.contact
                    dt = i.date
                    qn = i.qualification
                    pas = i.password
                    return render(request,'main.html',{'nm':nm,'em':em,'cn':cn,'dt':dt,'qn':qn,'pas':pas,'id':id})
            else:
                return HttpResponse("Email and password incorrect...!")
        else:
            return HttpResponse("Enter valid data")
    else:
        return render(request, 'login.html')


#edit profile
def editprofile(request,id):
    user = regmodel.objects.get(id=id)
    if request.method == "POST":
        user.name = request.POST.get('name')  #get edited values
        user.email = request.POST.get('email')
        user.contact = request.POST.get('contact')
        user.date = request.POST.get('date')
        user.qualification = request.POST.get('qualification')
        user.save()
        return redirect(login)

    return render(request,'edituser.html',{'user':user})

#company main page
def companylogin(request):
    global User;
    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_obj =User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'User not found')
            return redirect(companylogin)
        profile_obj = Companyreg.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'profile not verified check your email')
            return redirect(companylogin)
        User = authenticate(username=username, password=password)

        if User is None:
            messages.success(request,'wrong password or username')
            return redirect(companylogin)
        # return HttpResponse('success')
        #for displaying registered user's username and email id
        username = profile_obj.user.username
        email = profile_obj.user.email
        id = profile_obj.id
        return render(request, 'companymain.html',{'username':username,'email':email,'id':id})
    return render(request,'clogin.html')


def cregister(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        uname = request.POST.get('username')
        if password == cpassword:
            if User.objects.filter(username=uname).first():
                messages.success(request,"username already taken")
                return redirect(cregister)

            if User.objects.filter(email=email).first():
                messages.success(request,"email already taken")
                return redirect(cregister)

            user_obj=User(email=email,username=uname)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Companyreg.objects.create(user=user_obj, auth_token=auth_token)  # user.username
            profile_obj.save()
            send_mail_regis(email, auth_token)
            return HttpResponse("Success")
            # return redirect(companylogin)
    return render(request,'cregister.html')

def send_mail_regis(email,token):
    subject = "your account has been verified"
    message = f'pass the link to verify your account http://127.0.0.1:8000/verify/{token}'

    email_from=EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject,message,email_from,recipient)


def verify(request,auth_token):
    profile_obj = Companyreg.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,"your account already verified")
            redirect(companylogin)
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request,"your account verified")
        return redirect(companylogin)

    else:
        return redirect(error)


def error(request):
    return render(request,'error.html')


#add job
def jobs(request,id):
    u = Companyreg.objects.get(id=id)
    username = u.user.username
    email = u.user.email
    if request.method == "POST":
        a = jobform(request.POST)
        if a.is_valid():
            cn = a.cleaned_data['companyname']
            em = a.cleaned_data['email']
            jt = a.cleaned_data['jobtitle']
            wt = a.cleaned_data['worktype']
            exp = a.cleaned_data['experience']
            jtype = a.cleaned_data['jobtype']

            b = job(companyname=cn, email=em, jobtitle=jt, worktype=wt, experience=exp, jobtype=jtype)
            b.save()
            return HttpResponse("Job Posted Successfully")

        else:
            return HttpResponse("Invalid data")

    return render(request, 'job.html', {'username': username, 'email': email})


#show job openings
def showjob(request,id):
    uid = id
    sj = job.objects.all()
    cn = []
    jt = []
    id = []
    for i in sj:
        cns = i.companyname
        cn.append(cns)

        jtl = i.jobtitle
        jt.append(jtl)

        ids = i.id
        id.append(ids)
    mylist = zip(cn, jt, id)
    return render(request, 'showjob.html', {'sj': mylist,'uid':uid})

#view job details
def viewjob(request,id1,id2):
    vj = job.objects.get(id=id1)
    uid = id2
    cname = vj.companyname
    email = vj.email
    jt = vj.jobtitle
    wt = vj.worktype
    exp = vj.experience
    jobtype = vj.jobtype
    ids = vj.id
    return render(request, 'viewjob.html', {'cname':cname,'email':email,'jt':jt,'wt':wt,'exp':exp,'jobtype':jobtype,'ids':ids,'uid':uid})

def apply(request,id1,id2):
    form = jobapplyform
    a = job.objects.get(id=id1)
    user = regmodel.objects.get(id=id2)
    companyname = a.companyname
    jobtitle = a.jobtitle
    if request.method == "POST":
        b = jobapplyform(request.POST, request.FILES)
        if b.is_valid():
            cname = b.cleaned_data['companyname']
            email = b.cleaned_data['email']
            des = b.cleaned_data['designation']
            nm = b.cleaned_data['name']
            qn = b.cleaned_data['qualification']
            pn = b.cleaned_data['phone']
            exp = b.cleaned_data['experience']
            img = b.cleaned_data['image']
            ids = b.id

            c = jobapply(companyname=cname,email=email,designation=des,name=nm,qualification=qn,phone=pn,experience=exp,image=img,ids=ids)
            c.save()
            return HttpResponse("Application Successfull")
        else:
            return HttpResponse("Invalid data")

    return render(request, 'apply.html',{'data':form, 'companyname':companyname,'jobtitle':jobtitle,'user':user})

#add job
def addjob(request):
    a = jobapplyform(request.POST, request.FILES)
    if a.is_valid():
        a.save()
        return HttpResponse("Applied successfully")
    else:
        return HttpResponse("enter valid data")

def applicant(request,id):
    cmpny = Companyreg.objects.get(id=id)
    cmpny_name = cmpny.user.username   #get username
    jm = jobapply.objects.all()
    des = []
    nm = []
    email = []
    qn = []
    pn = []
    exp = []
    img = []
    for i in jm:
        if i.cname == cmpny_name:   #if company name and username is same
            des1 = i.designation
            des.append(des1)

            name1 = i.name
            nm.append(name1)

            email1 = i.email
            email.append(email1)

            qn1 = i.qualification
            qn.append(qn1)

            pn1 = i.phone
            pn.append(pn1)

            exp1 = i.experience
            exp.append(exp1)

            img1 = i.image
            img.append(str(img1).split('/')[-1])
    applicants = zip(des,nm,email,qn,pn,exp,img)
    return render(request,'applicant.html',{'applicants':applicants})

#dispaly registered companies
def viewcompany(request):
    jb = job.objects.all()
    cname = []
    email = []
    for i in jb:
        nm = i.companyname
        cname.append(nm)

        em = i.email
        email.append(em)

    mylist =zip(cname,email)
    return render(request,'viewcompany.html',{'company':mylist})

#display jobseekers applied jobs
def appliedjob(request):
    jobs = job.objects.all()
    cname = []
    jobt = []
    for i in jobs:
        cn = i.companyname
        cname.append(cn)

        jt = i.jobtitle
        jobt.append(jt)

    mylist = zip(cname,jobt)
    return render(request,'appliedjob.html',{'job':mylist})





