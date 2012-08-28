from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from tafe.models import Student, Subject, Enrolment, Course

urlpatterns = patterns('',
    url(r'^students/$',
        ListView.as_view(queryset=Student.objects.all())
       ),
        
    url(r'^student/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Student), name='student_view'),

    url(r'^courses/$',
        ListView.as_view(queryset=Course.objects.all())
       ),
        
    url(r'^course/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Course), name='course_view'),
    
    url(r'^subjects/$',
        ListView.as_view(queryset=Subject.objects.all())
       ),
        
    url(r'^subject/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Subject), name='subject_view'),
                      
)
