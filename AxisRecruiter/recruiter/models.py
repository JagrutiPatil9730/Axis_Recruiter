# models.py
from django.db import models

class Jobs(models.Model):
    jobid = models.CharField(max_length=100,default=0)
    jobname = models.CharField(max_length=100)
    applied = models.PositiveIntegerField(default=0)
    dobs = models.DateField()
    dobe = models.DateField()
    exp = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    TY = (
        ('p', 'Part Time'),
        ('f', 'Full Time'),
        ('i', 'Internship'),
    )
    typ = models.CharField(max_length=16, choices=TY, default='default_typ')
    status=models.IntegerField(default=0)
    sector = models.CharField(max_length=100)
    openings = models.CharField(max_length=100)
    creteria1 = models.CharField(max_length=100)
    creteria2 = models.CharField(max_length=100)
    creteria3 = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)
   
    applicants = models.ManyToManyField('seeker.UserProfile', related_name='job_applications', blank=True)
    interviewednts = models.ManyToManyField('seeker.UserProfile', related_name='interviewed_jobs', blank=True)
    shortlistedappl = models.ManyToManyField('seeker.UserProfile', related_name='shortlisted_jobs', blank=True)
    intervieweda = models.ManyToManyField('seeker.UserProfile', related_name='interviewed_as_applicant', blank=True)


    def __str__(self):
        return self.jobname
    

