from django.contrib import admin
from django.urls import path
from . import views
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import path
from .views import download_resume
from .views import contacts
urlpatterns = [
    path('', views.index,name='index'),
    path('index2', views.index2, name='index2'),
    path('contacts', views.contacts, name='contacts'),
    path('Guidlines', views.Guidlines,name='Guidlines'),
    path('jobs', views.jobs,name='jobs'),  
    path('interviewapp', views.interviewapp,name='interviewapp'),  
    path('chat_processing/', views.chat_processing, name='chat_processing'),
    path('apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('download_resume/<int:user_profile_id>/', download_resume, name='download_resume'),
    path('check_username/<str:username>/', views.check_username_availability, name='check_username'),
    path('signin', views.signin,name='signin'),
    path('signinrec', views.signinrec,name='signinrec'),
    path('signup', views.signup,name='signup'),
    path('StudenPrograms', views.StudenPrograms,name='StudenPrograms'),
    path('sample', views.sample,name='sample'),
   ]