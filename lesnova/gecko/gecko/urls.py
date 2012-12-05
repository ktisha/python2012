from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from library import views


urlpatterns = patterns('',
    url(r'^$', views.hello),
    url(r'^issue_add$', views.issue_add),
    url(r'^issue_list$', views.issue_list),
    url(r'^book_add$', views.book_add),
    url(r'^book_list$', views.book_list),
    url(r'^faculty_add$', views.faculty_add),
    url(r'^faculty_list$', views.faculty_list),
    url(r'^group_add$', views.group_add),
    url(r'^group_list$', views.group_list),
    url(r'^department_add$', views.department_add),
    url(r'^department_list$', views.department_list),
    url(r'^teacher_add$', views.teacher_add),
    url(r'^teacher_list$', views.teacher_list),
    url(r'^student_add$', views.student_add),
    url(r'^student_list$', views.student_list),
    url(r'^author_add$', views.author_add),
    url(r'^author_list$', views.author_list),
    url(r'^issue_edit/(?P<id>\d+)$', views.issue_edit, name='%(id)s'),
    url(r'^issue_remove/(?P<id>\d+)$', views.issue_remove, name='%(id)s'),
    url(r'^book_edit/(?P<id>\d+)$', views.book_edit, name='%(id)s'),
    url(r'^book_remove/(?P<id>\d+)$', views.book_remove, name='%(id)s'),
    url(r'^faculty_edit/(?P<id>\d+)$', views.faculty_edit, name='%(id)s'),
    url(r'^faculty_remove/(?P<id>\d+)$', views.faculty_remove, name='%(id)s'),
    url(r'^group_edit/(?P<id>\d+)$', views.group_edit, name='%(id)s'),
    url(r'^group_remove/(?P<id>\d+)$', views.group_remove, name='%(id)s'),
    url(r'^department_edit/(?P<id>\d+)$', views.department_edit, name='%(id)s'),
    url(r'^department_remove/(?P<id>\d+)$', views.department_remove, name='%(id)s'),
    url(r'^teacher_edit/(?P<id>\d+)$', views.teacher_edit, name='%(id)s'),
    url(r'^teacher_remove/(?P<id>\d+)$', views.teacher_remove, name='%(id)s'),
    url(r'^student_edit/(?P<id>\d+)$', views.student_edit, name='%(id)s'),
    url(r'^student_remove/(?P<id>\d+)$', views.student_remove, name='%(id)s'),
    url(r'^author_edit/(?P<id>\d+)$', views.author_edit, name='%(id)s'),
    url(r'^author_remove/(?P<id>\d+)$', views.author_remove, name='%(id)s'),
)

urlpatterns += static(settings.STATIC_URL, documrnt_root = settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()