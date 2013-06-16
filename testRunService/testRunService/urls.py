from django.conf.urls import patterns, include, url

#import trs
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^trs/', include('trs.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^trs/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^trs/admin/', include(admin.site.urls)),
)
