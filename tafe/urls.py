from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from tafe.models import Student, Subject, Enrolment, Course, Grade, Timetable
from tafe.views import session_create

urlpatterns = patterns('tafe.views',
    #url(r'^$', 'index'),
    url(r'^$', ListView.as_view(queryset=Subject.objects.all())),
    
    url(r'^students/$', ListView.as_view(queryset=Student.objects.all().order_by('surname'))),
    url(r'^student/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Student), name='student_view'),

    url(r'^courses/$', ListView.as_view(queryset=Course.objects.all())),
    url(r'^course/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Course), name='course_view'),
    
    url(r'^subjects/$', ListView.as_view(queryset=Subject.objects.all())),
    url(r'^subject/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Subject), name='subject_view'),
    
    url(r'^enrolments/$', ListView.as_view(queryset=Enrolment.objects.all())),
    url(r'^enrolment/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Enrolment), name='enrolment_view'),
                      
    url(r'^grades/$', ListView.as_view(queryset=Grade.objects.all())),
    url(r'^grade/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Grade), name='grade_view'),
                      
    url(r'^timetables/$', ListView.as_view(queryset=Timetable.objects.all().order_by('-year'))),
    #url(r'^timetable/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Timetable), name='timetable_view'),
    url(r'^timetable/(?P<slug>[-\w]+)/$', 'timetable_weekly_view'),
    #url(r'^timetable/(?P<slug>[-\w]+)/?P<day>[-\w]+/$', 'timetable_day_view'),
    #url(r'^timetable/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'timetable_daily_view'),
    #url(r'^timetable/(?P<year>\d{4})/$','timetable'),

    url(r'^session/create/$', session_create), 
)

