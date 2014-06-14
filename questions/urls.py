__author__ = 'shubham'

from django.conf.urls import patterns, include, url
from questions import views

urlpatterns = patterns(
    '',
    #url(r'^$', views.main, name='main'),

    url(r'^()$', views.all_questions_view, name='question'),

)