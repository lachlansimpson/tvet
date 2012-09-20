from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from tafe.models import Student, Subject, Enrolment, Course, Grade, Timetable, Applicant, Attendance
from tafe.views import session_create, session_view, timetable_daily_view, units_by_qualifications_view

urlpatterns = patterns('tafe.views',
    url(r'^$', 'index'),
    #url(r'^$', ListView.as_view(queryset=Subject.objects.all())),
    
    url(r'^students/$', ListView.as_view(queryset=Student.objects.all().order_by('surname'))),
    url(r'^student/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Student), name='student_view'),

    url(r'^applicants/$', ListView.as_view(queryset=Applicant.objects.all().order_by('surname'))),
    url(r'^applicants/successful/', 'applicant_success'),
    url(r'^applicant/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Applicant), name='applicant_view'),

    url(r'^qualifications/$', ListView.as_view(queryset=Course.objects.all())),
    url(r'^qualification/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Course), name='course_view'),

    url(r'^units/$', ListView.as_view(queryset=Subject.objects.all())),
    url(r'^units/qualifications/$', units_by_qualifications_view, name='units_by_qualifications_view'),
    url(r'^unit/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Subject), name='subject_view'),
    
    url(r'^enrolments/$', ListView.as_view(queryset=Enrolment.objects.all())),
    url(r'^enrolment/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Enrolment), name='enrolment_view'),
                      
    url(r'^grades/$', ListView.as_view(queryset=Grade.objects.all())),
    url(r'^grade/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Grade), name='grade_view'),
                      
    url(r'^timetables/$', ListView.as_view(queryset=Timetable.objects.all().order_by('-year'))),
    url(r'^timetable/(?P<slug>[-\w]+)/$', 'timetable_weekly_view', name='timetable_view'),
    #url(r'^timetable/(?P<slug>[-\w]+)/?P<day>[-\w]+/$', 'timetable_day_view'),
    #url(r'^timetable/(?P<year>\d{4})/$','timetable'), 
    url(r'^timetable/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', timetable_daily_view),

    url(r'^session/create/$', session_create), 
    url(r'^session/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', session_view, name='session_view'), 

    url(r'^attendance/all/$', ListView.as_view(queryset=Attendance.objects.all())),
    url(r'^attendance/today/$', ListView.as_view(queryset=Attendance.objects.all())),
    url(r'^attendance/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Attendance), name='attendance_view'),
)
