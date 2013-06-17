from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^trs/', include('trs.urls')),
    url(r'^trs/admin/', include(admin.site.urls)),
)
