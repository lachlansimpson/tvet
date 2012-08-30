from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tafe.models import Student, Subject, Enrolment, Course, Grade

urlpatterns = patterns('',
    #url(r'^$', 'index'),
    url(r'^$', ListView.as_view(queryset=Subject.objects.all())),
    
    url(r'^students/$', ListView.as_view(queryset=Student.objects.all())),
    url(r'^student/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Student), name='student_view'),

    url(r'^courses/$', ListView.as_view(queryset=Course.objects.all())),
    url(r'^course/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Course), name='course_view'),
    
    url(r'^subjects/$', ListView.as_view(queryset=Subject.objects.all())),
    url(r'^subject/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Subject), name='subject_view'),
    
    url(r'^enrolments/$', ListView.as_view(queryset=Enrolment.objects.all())),
    url(r'^enrolment/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Enrolment), name='enrolment_view'),
                      
    url(r'^grades/$', ListView.as_view(queryset=Grade.objects.all())),
    url(r'^grade/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Grade), name='grade_view'),
                      
)
