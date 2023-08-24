from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Jobs
from django.db.models import Count
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import PyPDF2
import re
from seeker.models import UserProfile

def indexr(request):
    # Fetching data for the chart
    jobs_datad = Jobs.objects.order_by('dobs')[:3]

    # Fetching data for annotation and chart
    jobs = Jobs.objects.annotate(application_count=Count('id'))

    # Creating a list of dictionaries containing job data
    job_data = [{'job_title': job.jobname, 'job_count': job.applied} for job in jobs]

    context = {'jobs': job_data}

    # Convert the context to a JSON string and escape it for safe use in JavaScript
    chart_data_json = json.dumps(context)

    return render(request, 'indexr.html', {"job_data": jobs_datad, "chart_data_json": chart_data_json})


def interView_candidate(request, job_id, applicant_id):
    # Get the UserProfile and Job instances based on IDs
    user_profile = get_object_or_404(UserProfile, id=applicant_id)
    job = get_object_or_404(Jobs, id=job_id)
    job.applicants.remove(user_profile)
    user_profile.status += 1
    job.interviewednts.add(user_profile)
    for applicjob in user_profile.applied_jobs.all():
        if(applicjob.id==job_id):
            applicjob.status=2
            applicjob.save()
    user_profile.save()
    job.save()
    
    return redirect('ATS')


def shortlist_candidate(request, job_id, applicant_id):
    # Get the UserProfile and Job instances based on IDs
    user_profile = get_object_or_404(UserProfile, id=applicant_id)
    job = get_object_or_404(Jobs, id=job_id)
    job.interviewednts.remove(user_profile)
    print('infun')
    # Perform the actions on the retrieved instances
    user_profile.status += 1
    
    job.shortlistedappl.add(user_profile)
    for applicjob in user_profile.applied_jobs.all():
        if(applicjob.id==job_id):
            applicjob.status=3
            applicjob.save()
    user_profile.save()
    job.save()


    print(user_profile,job.interviewednts)
    return redirect('ATS')

def Review_candidate(request, job_id, applicant_id):
    # Get the UserProfile and Job instances based on IDs
    user_profile = get_object_or_404(UserProfile, id=applicant_id)
    job = get_object_or_404(Jobs, id=job_id)
    job.applicants.remove(user_profile)
    
    for applicjob in user_profile.applied_jobs.all():
        if(applicjob.id==job_id):
            applicjob.status=4
            applicjob.save()
    # Perform the actions on the retrieved instances
    user_profile.status += 1
    job.interviewednts.add(user_profile)
    user_profile.save()
    job.save()
    
    return redirect('Interview')



def mail_candidate(request, job_id, applicant_id):
    # Get the UserProfile and Job instances based on IDs
    
    
    return redirect('Interview')


def downloadresume_candidate(request, job_id, applicant_id):
    # Get the UserProfile and Job instances based on IDs
    print('download')
    applicant = get_object_or_404(UserProfile, id=applicant_id)
    user_profile = UserProfile.objects.get(id=applicant_id)
    response = HttpResponse(user_profile.resume, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response
    if applicant.resume:
        print("Resume found.")
        response = HttpResponse(applicant.resume, content_type='application/pdf')  # Adjust content type if needed
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'  # Adjust filename
        # response = HttpResponse(user_profile.resume, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        print(response)
        return response
    return response

def ATS(request):
    usrs = UserProfile.objects.all()
    jobs = Jobs.objects.all()
    sections = {
        'experience': (['experience', 'work history', 'employment', 'professional background'], 10),
        'education': (['education', 'academic background', 'degrees'], 8),
        'skills': (['skills', 'proficiencies', 'technical skills', 'software'], 9),
        'achievements': (['achievements', 'accomplishments', 'results'], 7),
        'leadership': (['leadership', 'teamwork', 'collaboration'], 6),
        'finance': (['finance', 'financial knowledge'], 8),
        'compliance': (['compliance', 'regulatory', 'legal'], 7),
        'customer_service': (['customer service', 'client interactions'], 6),
        'communication': (['communication', 'written', 'verbal'], 7),
        'detail_oriented': (['attention to detail', 'precision', 'accuracy'], 8),
        'problem_solving': (['problem-solving', 'analytical skills'], 9),
        'memberships': (['memberships', 'professional organizations'], 5),
        'adaptability': (['adaptability', 'learning', 'flexibility'], 6)
    }
    
    cr1 =  ['Interpersonal Skills', 'Analytical Thinking', 'Customer Service', 'Marketing Proficiency', 'Operation Management', 'Business Acumen', 'Financial Management', 'Time Management', 'Leadership Skills', 'Commercial Awareness', 'Knowledge of financial principles and practices','Analytical mind', 'knowledge of banking products', 'markets and relevant regulations', 'Sales and negotiation skills', 'Strong communication & presentation skills', 'Ability to Work Under Pressure', 'Customer Service', 'Ledger balancing', 'Balance allocation', 'Cash drawer maintenance','Project management', 'Teamwork', 'Time management', 'Risk management', 'Skilled at receiving and processing banking transactions', 'Strong mathematical skills', 'Attention to detail', 'Knowledge of proper cash handling procedures', 'Loan processing', 'Tax preparation', 'Petty cash management', 'Numeracy skills']

    
    job_applicants_data={}
    for job in jobs:
        for u in job.applicants.all():
            text = u.resumetxt.lower()
            section_info = {section: {'present': False, 'score': 0} for section in sections}

            total_score = 0
            for section, (keywords, score) in sections.items():
                for keyword in keywords:
                    if keyword in text:
                        section_info[section]['present'] = True
                        section_info[section]['score'] = score
                        total_score += score
                        break

            section_info['total_score'] = total_score
            
            word_list = re.findall(r'\b\w+\b', text)
            cnt1 = 0
            for word in word_list:
                w = word.lower()
                if w in cr1:
                    cnt1 += 1
                    u.skillstxt = w
                
            u.skills= cnt1
            user_ranking = cnt1 + total_score  # Combine CV and section scores
            ranking_percentage = (user_ranking / 90) * 100
            u.match=ranking_percentage
            u.save()


    return render(request, 'ATS.html', {'jobs': jobs,'allapplicants': usrs,'job_applicants_data':job_applicants_data})


def Communication(request):
    return render(request,'Communication.html')

def Interview(request):
    usrs = UserProfile.objects.all()
    
    
    # # Create sample interview questions
    # question1 = InterviewQ.objects.create(
    #     Question="Tell me about your experience with Python.",
    #     Answer="I have been using Python for 3 years...",
    #     # ... other fields ...
    # )
    
    # question2 = InterviewQ.objects.create(
    #     Question="Explain object-oriented programming.",
    #     Answer="Object-oriented programming is a programming paradigm...",
    #     # ... other fields ...
    # )
    # for i in usrs:
    # # Associate interview questions with applicants
    #     i.applied_interview.add(question1, question2) # Applicant 2 only answered the first question
    #     i.save()
    # # Fetch the applicants and their interview questions for rendering
    # applicants = UserProfile.objects.all()
    # context = {'applicants': applicants,'applicantsint': applicants}
    # print(context)
    # for i in usrs:
    # # Associate interview questions with applicants
    #     for j in i.applied_interview.all():
    #         print(j.Question) # Applicant 2 only answered the first question
        
    usrs = UserProfile.objects.all()
    jobs = Jobs.objects.all()
    return render(request, 'Interview.html', {'jobs': jobs,'allapplicants': usrs})

def Jobposting(request):
    
    
    if request.method == 'POST':
        jobname = request.POST.get('jobname', '').strip()
        dobs = request.POST.get('dobs', '').strip()
        dobe = request.POST.get('dobe', '').strip()
        exp = request.POST.get('exp', '').strip()
        place = request.POST.get('place', '').strip()
        typ = request.POST.get('typ', '').strip()
        sector = request.POST.get('sector', '').strip()
        openings = request.POST.get('openings', '').strip()
        creteria1 = request.POST.get('creteria1', '').strip()
        creteria2 = request.POST.get('creteria2', '').strip()
        creteria3 = request.POST.get('creteria3', '').strip()
        about = request.POST.get('about', '').strip()

        
        Jobs.objects.create(
            jobname =jobname,
            dobs = dobs,
            # applied=applied+1;
            dobe = dobe,
            exp = exp,
            place = place,
            typ = typ,
            sector =sector,
            openings =openings,
            creteria1 =creteria1,
            creteria2 =creteria2,
            creteria3 =creteria3,
            about =  about,
        )
        return redirect('indexr')
    else:
        return render(request, 'Jobposting.html')


def Shortlisted(request):
    usrs = UserProfile.objects.all()
    jobs = Jobs.objects.all()
    return render(request, 'Shortlisted.html', {'jobs': jobs,'allapplicants': usrs})

def sample(request):
    return render(request,'sample.html')

