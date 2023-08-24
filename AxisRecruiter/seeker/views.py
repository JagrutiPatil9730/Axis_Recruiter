from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserProfile
from recruiter.models import Jobs 
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.core.files.storage import default_storage
from django.db import transaction
import PyPDF2

from django.core.files.base import ContentFile
job_ids=None
loginu=True
profile_object={}
jid=0
user_profile=None
applied_jobs=None

def index(request):
    
    # jobs = Jobs.objects.annotate(application_count=Count('id'))

    # # Creating a list of dictionaries containing job data
    # job_data = [{'job_title': job.jobname, 'job_count': job.applied} for job in jobs]
    # rejobs = Jobs.objects.all()
    # for i in rejobs:
    #     if i.applied
    global loginu
    loginu =True
    if loginu:
        return render(request,'index.html', {'login': loginu})
    else:
        return render(request,'index2.html', {'login': loginu,'appliedjob':profile_object.applied})

def index2(request):
    global loginu
    
    global user_profile
    global applied_jobs
    global jid
    print(user_profile)
    # resume_path = user_profile.resume # Get the path to the resume file
    # pdf_url = user_profile.resume
    # print(pdf_url)
    response = HttpResponse(user_profile.resume, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    
    return render(request, 'index2.html', {'user_profile': user_profile, 'applied_jobs': applied_jobs, 'resume_path': response,'pdf_url': response})
    # return render(request, 'index2.html', {'user_profile': user_profile, 'applied_jobs': applied_jobs})
    # for arg in args:
    #     user = get_object_or_404(UserProfile, username=request.username)
    #     user.applied_jobs.add(arg)
    # return render(request,'index2.html', {'login': loginu,})


def download_resume(request, user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)
    response = HttpResponse(user_profile.resume, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response

def apply_for_job(request, job_id):
    global loginu
    global user_profile
    global applied_jobs
    global jid
    jid=job_id
    if user_profile and job_id:  # Check if user_profile is available and job_id is valid
        job = Jobs.objects.get(id=job_id)
        job.applied += 1
        job.applicants.add(user_profile)
        job.save()
        user_profile.applied_jobs.add(job)  # Add the job to applied_jobs
        applied_jobs = user_profile.applied_jobs.all()  # Update applied_jobs list
        user_profile.save()  # Save the user profile with the updated applied_jobs
    return redirect('index2')

def contacts(request):
    name_text = ""
    message_text = ""
    email_text = ""
    if request.method == 'POST':
        name_text = request.POST.get('name', '')
        email_text = request.POST.get('email', '')
        message_text = request.POST.get('message', '')


        subject = 'Contact Form Submission'
        message = f'Name: {name_text}\nEmail: {email_text}\nMessage: {message_text}'
        from_email = 'your_email@example.com'  # Replace with your email address
        recipient_list = ['jagrutipatil5433@gmail.com']

        # send_mail(subject, message, from_email, recipient_list)

    return render(request, 'contacts.html', {'name_text': name_text, 'email_text': email_text, 'message_text': message_text,'login': loginu,})


def Guidlines(request):
    return render(request, 'Guidlines.html', {'login': loginu,})

def jobs(request):
    jobs = Jobs.objects.all()

    return render(request, 'jobs.html', {'jobs': jobs,'login': loginu,})


def signin(request):
    global loginu
    names = UserProfile.objects.values_list('name', flat=True)
    global user_profile
    global applied_jobs
    if request.method == 'POST':
        name_text = request.POST.get('Uname', '')
        Password_text = request.POST.get('Password', '')
        
        
        loginu=False
        matching_profiles = UserProfile.objects.filter(username = name_text)
        filtered_profiles = [profile for profile in matching_profiles if profile.passw == Password_text]
        if filtered_profiles:
            loginu = False
            user_profile = filtered_profiles[0]
            applied_jobs = user_profile.applied_jobs.all()  # Retrieve applied jobs
            return render(request, 'index2.html', {'user_profile': user_profile, 'applied_jobs': applied_jobs})
   
        else:
            profile_object = None  # No matching or filtered profile found
            return render(request, 'signin.html',{'login_failed': True,})

    return render(request, 'signin.html')


def signinrec(request):
    names = UserProfile.objects.values_list('name', flat=True)

    name_text = ""
    Password_text = ""
    if request.method == 'POST':
        name_text = request.POST.get('Uname', '')
        Password_text = request.POST.get('Password', '')
        if 'rec' == name_text and 'rec' == Password_text:
            return redirect('indexr')
        else :
            return render(request, 'signinrec.html',{'login_failed': True,})

    return render(request, 'signinrec.html', {'name_text': name_text,'login': loginu,})


def signup(request):
    name = ""
    email = ""
    dob = ""
    exp = ""
    post = ""
    gen = ""
    ad1 = ""
    ad2 = ""
    pho1 = ""
    pho2 = ""
    work = ""
    edu = ""
    per = ""
    uni = ""
    about=""
    username=""
    passw=""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        dob = request.POST.get('dob', '')
        exp = request.POST.get('exp', '')
        post = request.POST.get('post', '')
        gen = request.POST.get('gen', '')
        ad1 = request.POST.get('ad1', '')
        ad2 = request.POST.get('ad2', '')
        pho1 = request.POST.get('pho1', '')
        pho2 = request.POST.get('pho2', '')
        work = request.POST.get('work', '')
        edu = request.POST.get('edu', '')
        per = request.POST.get('per', '')
        uni = request.POST.get('uni', '')
        about = request.POST.get('about', '')
        username = request.POST.get('username', '')
        passw = request.POST.get('pass1', '')
        
        uploaded_file = request.FILES.get('resume')
        text = ""
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        pdf_content = uploaded_file.read() 
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        print(text)
        UserProfile.objects.create(
            name = name,
            email = email,
            dob = dob,
            exp = exp,
            post = post,
            gen =gen,
            ad1 = ad1,
            ad2 = ad2,
            pho1 = pho1,
            pho2 = pho2,
            work = work,
            edu = edu,
            per = per,
            uni = uni,
            about = about,
            username=username,
            passw=passw,
            resumetxt=text,
            resume=pdf_content,
        )
        
        return redirect('signin')
    else:
        return render(request, 'signup.html', {'name  ': "",'email ': "",'dob   ': "",'exp   ': "",'post  ': "",'gen   ': "",'ad1   ': "",'ad2   ': "",'pho1  ': "",'pho2  ': "",'work  ': "",'edu   ': "",'per   ': "",'uni   ': "",'login': loginu,})



def StudenPrograms(request):
    return render(request, 'StudenPrograms.html', {'login': loginu,})

def sample(request):
    return render(request, 'sample.html', {'login': loginu,})

def check_username_availability(request, username):
    username_exists = UserProfile.objects.filter(username=username).exists()
    return JsonResponse({'exists': username_exists})