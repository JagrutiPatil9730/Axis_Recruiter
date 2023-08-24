from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserProfile, InterviewQ
from recruiter.models import Jobs 
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os
os.environ["OPENAI_API_KEY"] = "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"


from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.core.files.storage import default_storage
from django.db import transaction
import PyPDF2
from django.db.models import Count
from django.http import JsonResponse
from django.core.files.base import ContentFile
job_ids=None
loginu=True
profile_object={}
jid=None
user_profile=None
desuser=None
applied_jobs=None
cnt_que=0
preque=''
def chat_processing(request):
    global jid
    print(user_profile)
    website_data = ""
    urls = ['https://engineeringinterviewquestions.com/axis-bank-interview-questions-and-answers-pdf/']

    for url in urls:
        # text = jid.resumetxt
        text=pull_from_website(url) 
        website_data += text

    user_information = website_data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
    docs = text_splitter.create_documents([user_information])
    map_prompt=''' You are a helpful AI bot that takes the banking interview of the user .give list to interview question by analysing given resume  information by using this data as % START OF INFORMATION ABOUT {job}:
    {text}
    % END OF INFORMATION ABOUT {job}:'''
   
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "job"])

    combine_prompt = """
    You are a helpful AI bot that is an interviewer which takes the banking interview of the user and takes the input from the user for the answer.
    You will be given a list of potential interview questions that we can ask to the user related to the {job}.

    Please consolidate the questions and return set of questions 

    % INTERVIEW QUESTIONS
    {text}
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "job"])
    llm = ChatOpenAI(temperature=.25, model_name='gpt-3.5-turbo')

    chain = load_summarize_chain(llm,chain_type="map_reduce",map_prompt=map_prompt_template,combine_prompt=combine_prompt_template
    #,verbose=True
    )

    output = chain({"input_documents": docs, # The seven docs that were created before
                    "job": "cleark"
                })
    questions= (output['output_text'])

    questions_list = questions.split('\n')

    # Cleaning up the list to remove empty items and extracting the questions
    questions_list = [question.split('. ', 1)[1] for question in questions_list if question.strip()]

    print(questions_list,questions)
    global preque
    if request.method == 'POST':
        cnt_que+=1
        user_message = request.POST.get('user_message', '')
        print(user_message)
        # Process the user's message and generate a bot response
        bot_response = questions_list[cnt_que]
        
        # # Create sample interview questions
        question1 = InterviewQ.objects.create(
            Question=preque,
            Answer=user_message,
        )
        
        
        user_profile.applied_interview.add(question1) # Applicant 2 only answered the first question
        user_profile.save()
        preque=bot_response
        print(question1,bot_response,cnt_que)
        return JsonResponse({'bot_response': bot_response})

def index(request):
    # Jobs.objects.all().delete()
    # UserProfile.objects.all().delete()

    jobs_datad = Jobs.objects.order_by('dobs')[:3]

    # Fetching data for annotation and chart
    jobs = Jobs.objects.annotate(application_count=Count('id'))

    # Creating a list of dictionaries containing job data
    job_data = [{'job_title': job.jobname, 'job_count': job.applied} for job in jobs]

    global loginu
    loginu =True
    if loginu:
        return render(request,'index.html', {'login': loginu,"job_data": jobs_datad})
    else:
        return render(request,'index2.html', {'login': loginu,'appliedjob':profile_object.applied})
    


def index2(request):
    global loginu
    
    global user_profile
    global applied_jobs
    global jid
    jid=user_profile
    global desuser
    desuser=user_profile
    return render(request, 'index2.html', {'user_profile': user_profile, 'applied_jobs': applied_jobs})


def download_resume(request, user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)
    response = HttpResponse(user_profile.resume, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response

def interviewapp(request): 
    return render(request, 'interviewapp.html')

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

def pull_from_website(url):
    
    # Doing a try in case it doesn't work
    try:
        response = requests.get(url)
            # Put your response in a beautiful soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get your text
        text = soup.get_text()
    
        # Convert your html to markdown. This reduces tokens and noise
        text = md(text)
         
        return text
    except:
        # In case it doesn't work
        print ("Whoops, error")
        return None