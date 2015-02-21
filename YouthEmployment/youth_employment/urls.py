__author__ = 'Jasneet Sabharwal <jsabharw@sfu.ca>'

from django.conf.urls import patterns, url

from youth_employment import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'))
