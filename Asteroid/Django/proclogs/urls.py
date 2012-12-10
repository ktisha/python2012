from django.conf.urls import patterns, url

urlpatterns = patterns('proclogs.views',
    url(r'^$', 'index'),
    url(r'^asteroid/(?P<designated_name>\w+)$', 'asteroid_info'),
)