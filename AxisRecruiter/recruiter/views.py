from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Jobs
from django.db.models import Count
import json
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


def ATS(request):
    # usrs = UserProfile.objects.all()
    # jobs = Jobs.objects.all()
    # cr1=[]
    # cr1.append(jobs.creteria1) # ['Interpersonal Skills', 'Analytical Thinking', 'Customer Service', 'Marketing Proficiency', 'Operation Management', 'Business Acumen', 'Financial Management', 'Time Management', 'Leadership Skills', 'Commercial Awareness', 'Knowledge of financial principles and practices']
    # cr1.append(jobs.creteria2)
    # cr1.append(jobs.creteria3)
    # cr1.append(jobs.creteria4)
    # def extract_text_from_pdf(pdf_path):
    #     text = ""
    #     with open(pdf_path, 'rb') as pdf_file:
    #         pdf_reader = PyPDF2.PdfReader(pdf_file)
    #         for page in pdf_reader.pages:
    #             text += page.extract_text()
    #     return text

    # class Resume:
    #     def __init__(self, work_experience, education, skills, projects, certifications, personal_info=None, summary=None, references=None):
    #         self.personal_info = personal_info
    #         self.summary = summary
    #         self.education = education
    #         self.work_experience = work_experience
    #         self.skills = skills
    #         self.certifications = certifications
    #         self.references = references

    # def evaluate_resume(resume):
    #     score = 0
    #     score += resume.work_experience * 4
    #     score += resume.education * 2
    #     score += resume.skills * 2
    #     score += resume.projects
    #     score += resume.certifications
    #     return score

    # def provide_feedback(candidate_resumes):
    #     ranked_resumes = []
        
    #     for candidate_name, resume in candidate_resumes.items():
    #         total_score = evaluate_resume(resume)
    #         ranked_resumes.append((candidate_name, total_score, resume))

    #     ranked_resumes.sort(key=lambda x: x[1], reverse=True)
        
    #     feedback = []
    #     for rank, (candidate_name, total_score, resume) in enumerate(ranked_resumes, start=1):
    #         feedback_message = f"Rank: {rank}\n"
    #         feedback_message += f"Total Score: {total_score}\n"
            
    #         if rank == 1:
    #             feedback_message += "Congratulations! Your resume is highly competitive."
    #         else:
    #             feedback_message += "Your resume has potential for improvement. Consider the following suggestions:\n"
    #             feedback_message += "- Enhance your work experience section with more detailed accomplishments.\n"
    #             feedback_message += "- Highlight relevant skills that align with the job requirements.\n"
    #             feedback_message += "- Provide specific details about successful projects you've worked on.\n"
    #             # Add more specific suggestions based on the candidate's resume content.
            
    #         feedback.append(feedback_message)
        
    #     return feedback

    # def extract_text_from_pdf(pdf_path):
        # text = ""
        # with open(pdf_path, 'rb') as pdf_file:
        #     pdf_reader = PyPDF2.PdfReader(pdf_file)
        #     for page in pdf_reader.pages:
        #         text += page.extract_text()
        # return text

        # print("Resume Ranking")
        # pdf_path = input("Enter the path to the PDF resume file: ")
        # # Extract text from PDF and store it in a variable
        # resume_text = extract_text_from_pdf(pdf_path)
        # word_list = re.findall(r'\b\w+\b', resume_text)
        # print(word_list)
        # # Display the extracted text
        # cr1 = [word.lower() for word in cr1]

        # # Convert word_list to lowercase
        # cnt1 = 0
        # for word in word_list:
        #     w=word.lower()
        #     if w in cr1:
        #         cnt1 += 1
        # print("Count for CR1:", cnt1)
    return render(request, 'ATS.html', {'jobs': jobs,'applicants': usrs})


def Communication(request):
    return render(request,'Communication.html')

def Interview(request):
    return render(request,'Interview.html')

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
        print("Jobname:", jobname)
        return redirect('indexr')
    else:
        return render(request, 'Jobposting.html')


def Shortlisted(request):
    usrs = UserProfile.objects.all()
    jobs = Jobs.objects.all()

    return render(request, 'Shortlisted.html', {'jobs': jobs,'applicants': usrs})

def sample(request):
    return render(request,'sample.html')

