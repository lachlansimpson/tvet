from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from django.views.generic import DetailView, ListView, CreateView
from tafe.models import Student, Subject, Enrolment, Course, Grade, Timetable, Applicant, Staff
from tafe.views import session_create, session_view, session_attendance_view, timetable_daily_view, units_by_qualifications_view, unit_view, assessment_view, student_reports, applicant_reports, reports, applicant_qualification, applicant_shortlist, applicant_shortlist_qualification

urlpatterns = patterns('tafe.views',
    url(r'^$', 'index'),
    
    url(r'^applicants/$', ListView.as_view(queryset=Applicant.current.order_by('first_name'))),
    url(r'^applicants/successful/$', 'applicant_success'),
    url(r'^applicants/qualifications/$', applicant_qualification),
    url(r'^applicants/short-list/$', applicant_shortlist),
    url(r'^applicants/short-list/qualifications/$', applicant_shortlist_qualification),
    url(r'^applicant/add/$', CreateView.as_view(model=Applicant)),
    url(r'^applicant/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Applicant), name='applicant_view'),

    url(r'^students/$', ListView.as_view(queryset=Student.objects.all().order_by('surname'))),
    url(r'^student/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Student), name='student_view'),

    url(r'^staff/$', permission_required('staff.can_change', raise_exception=True)(ListView.as_view(queryset=Staff.people.all().order_by('surname')))),
    url(r'^staff/(?P<slug>[-\w]+)/$', permission_required('staff.can_change', raise_exception=True)(DetailView.as_view(model=Staff)), name='staff_view'),
                       
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
    url(r'^timetable/(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'timetable_weekly_view', name='timetable_view'),
    url(r'^timetable/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', timetable_daily_view),

    url(r'^session/create/$', session_create), 
    url(r'^session/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', session_view, name='session_view'), 
    url(r'^session/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/attendance/$', session_attendance_view, name='session_attendance_view'), 
    
    url(r'^reports/$', reports, name='reports'),
    # html reports for this year
    url(r'^report/students/$', student_reports, name='student_reports'),
    url(r'^report/applicants/$', applicant_reports, name='applicant_reports'),
    # html reports of the stats
    url(r'^report/students/(?P<year>\d{4})/html/$', student_reports, name='student_reports'),
    url(r'^report/applicants/(?P<year>\d{4})/html/$', applicant_reports, name='applicant_reports'), 
    # csv download of the stats
    url(r'^report/applicants/(?P<year>\d{4})/csv/$', applicant_reports, {'format':'csv'}, name='applicant_reports'),
    url(r'^report/students/(?P<year>\d{4})/csv/$', student_reports, {'format':'csv'}, name='student_reports'), 
    # csv download of the raw data
    url(r'^report/applicants/(?P<year>\d{4})/raw/$', applicant_reports, {'format':'raw'}, name='applicant_reports'),
    url(r'^report/students/(?P<year>\d{4})/raw/$', student_reports, {'format':'raw'}, name='student_reports'), 
)
