# models.py
from django.db import models
from recruiter.models import Jobs 

class UserProfile(models.Model):
    name = models.CharField(max_length=100,default='')
    username = models.CharField(max_length=100,default='')
    passw = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=100,default='')
    dob = models.DateField(default='2000-01-01')
    exp = models.CharField(max_length=100,default=0)
    POST = (
        ('Intern', 'Intern'),
        ('Cleark', 'Cleark'),
        # Add more nationality options as needed
    )
    post = models.CharField(max_length=13, choices=POST,default='')
  
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )
    gen = models.CharField(max_length=6, choices=GENDER_CHOICES,default='')
    applied = models.PositiveIntegerField(default=0)
    ad1 = models.CharField(max_length=100,default='')
    ad2 = models.CharField(max_length=100,default='')
    pho1 = models.CharField(max_length=100,default=0)
    pho2 = models.CharField(max_length=100,default=0)
    WORK = (
        ('Open to Work', 'Open to Work'),
        ('Viewer', 'Viewer'),
        # Add more nationality options as needed
    )
    work = models.CharField(max_length=13, choices=WORK,default='')
    edu = models.CharField(max_length=100,default='')
    per = models.CharField(max_length=100,default='')
    uni = models.CharField(max_length=100,default='')
    about = models.CharField(max_length=1000,default='')
    interviewres = models.CharField(max_length=1000,default='')
    applied_jobs = models.ManyToManyField('recruiter.Jobs', related_name='job_applicants', blank=True)

    ranking=models.IntegerField(default=0)
    skillstxt=models.CharField(max_length=10485750,default='')
    skills=models.IntegerField(default=0)
    match=models.IntegerField(default=0)
    status=models.IntegerField(default=0)
    interviewscore=models.IntegerField(default=0)
    match=models.IntegerField(default=0)
    hrreview=models.CharField(max_length=104750,default='')
    resumetxt=models.CharField(max_length=10485750,default='')
    resume = models.BinaryField(null=True, blank=True)
    applied_interview = models.ManyToManyField('InterviewQ', related_name='applied_interview', blank=True)



    def __str__(self):
        return self.username


class InterviewQ(models.Model):
    Question =models.CharField(max_length=10485750,default='')    
    Answer=models.CharField(max_length=10485750,default='')
    Evalution = models.CharField(max_length=100,default='')
    forjobs = models.CharField(max_length=100,default='')



    def __str__(self):
        return self.username