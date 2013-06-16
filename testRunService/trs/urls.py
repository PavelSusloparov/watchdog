from django.conf.urls import patterns, url

from trs import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )
