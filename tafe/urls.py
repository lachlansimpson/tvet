from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView, CreateView
from tafe.models import Student, Subject, Enrolment, Course, Grade, Timetable, Applicant, Staff
from tafe.views import session_create, session_view, session_attendance_view, timetable_daily_view, units_by_qualifications_view, unit_view, assessment_view, student_reports, applicant_reports, reports

urlpatterns = patterns('tafe.views',
    url(r'^$', 'index'),
    
    url(r'^reports/$', reports, name='reports'),
    
    url(r'^students/$', ListView.as_view(queryset=Student.objects.all().order_by('surname'))),
    url(r'^students/reports/$', student_reports, name='student_reports'),
    url(r'^students/reports/(?P<year>\d{4})/$', student_reports, name='student_reports'),
    url(r'^student/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Student), name='student_view'),

    url(r'^applicants/$', ListView.as_view(queryset=Applicant.current.order_by('surname'))),
    url(r'^applicants/reports/$', applicant_reports, name='applicant_reports'),
    url(r'^applicants/reports/(?P<year>\d{4})/$', applicant_reports, name='applicant_reports'),
    url(r'^applicants/successful/$', 'applicant_success'),
    url(r'^applicant/add/$', CreateView.as_view(model=Applicant)),
    url(r'^applicant/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Applicant), name='applicant_view'),

    url(r'^staff/$', ListView.as_view(queryset=Staff.people.all().order_by('surname'))),
    url(r'^staff/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Staff), name='staff_view'),
                       
    url(r'^qualifications/$', ListView.as_view(queryset=Course.objects.all())),
    url(r'^qualification/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Course), name='course_view'),

    url(r'^units/$', ListView.as_view(queryset=Subject.objects.all())),
    url(r'^units/qualifications/$', units_by_qualifications_view, name='units_by_qualifications_view'),
    url(r'^unit/(?P<slug>[-\w]+)/$', unit_view, name='unit_view'),
    url(r'^unit/(?P<unit>[-\w]+)/assessment/(?P<slug>[-\w]+)/$', assessment_view, name='assessment_view'),
    
    url(r'^enrolments/$', ListView.as_view(queryset=Enrolment.objects.all())),
    url(r'^enrolment/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Enrolment), name='enrolment_view'),
                      
    url(r'^grades/$', ListView.as_view(queryset=Grade.objects.all())),
    url(r'^grade/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Grade), name='grade_view'),
                      
    url(r'^timetables/$', ListView.as_view(queryset=Timetable.objects.all().order_by('-year'))),
    url(r'^timetable/today/$', 'index'), # important: ordering before the slug 
    url(r'^timetable/(?P<slug>[-\w]+)/$', 'timetable_weekly_view', name='timetable_view'),
    url(r'^timetable/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', timetable_daily_view),

    url(r'^session/create/$', session_create), 
    url(r'^session/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', session_view, name='session_view'), 
    url(r'^session/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/attendance/$', session_attendance_view, name='session_attendance_view'), 
)
