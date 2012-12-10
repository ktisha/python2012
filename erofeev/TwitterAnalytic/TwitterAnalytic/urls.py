#coding: utf-8

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TwitterAnalytic.views.home', name='home'),
    # url(r'^TwitterAnalytic/', include('TwitterAnalytic.foo.urls')),

    url(r'^recipient', 'Analytic.views.recipient'),
    #url(r'^$', 'Analytic.views.search'),
    url(r'^search', 'Analytic.views.search'),
    url(r'^result', 'Analytic.views.result'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
