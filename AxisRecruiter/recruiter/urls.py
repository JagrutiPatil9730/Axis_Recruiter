from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexr,name='indexr'),
    path('/ATS', views.ATS, name='ATS'),
    path('/Communication', views.Communication,name='Communication'),
    path('/Interview', views.Interview,name='Interview'),
    path('/Jobposting', views.Jobposting,name='Jobposting'),
    path('/Shortlisted', views.Shortlisted,name='Shortlisted'),
    path('/sample', views.sample,name='sample'),
   ]