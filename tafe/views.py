# Create your views here.

from tafe.models import Timetable, Session, Course, StudentAttendance, Subject, Assessment, StaffAttendance, Enrolment
from tafe.forms import SessionRecurringForm, ApplicantSuccessForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import modelformset_factory
from dateutil.relativedelta import *
import datetime
today = datetime.date.today()

''' Index page'''
@login_required
def index(request):
    """ 
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    daily_sessions = []

    for session in range(4):
        daily_sessions.append([])
        daily_sessions[session] = Session.objects.filter(date=today).filter(session_number=session)

    return render_to_response('tafe/timetable_today_detail.html',{'daily_sessions':daily_sessions}, RequestContext(request))

############### Sessions ###############

@login_required
def session_create(request):
    ''' For each subject, we will create a session object for each day that it is taught '''
    if request.method == 'POST':
        form = SessionRecurringForm(request.POST)
        if form.is_valid():
            s = Session()
            s.subject = form.cleaned_data['subject']
            s.timetable = form.cleaned_data['timetable']
            s.session_number = form.cleaned_data['session_number']

            recurring = form.cleaned_data['recurring']
            if not recurring:  
                s.date = form.cleaned_data['first_date']
                s.save()
                return HttpResponseRedirect('/tafe/')

            first_date = form.cleaned_data['first_date'] 
            for_semester = form.cleaned_data['for_semester'] 
            if for_semester:
                second_date = s.timetable.end_date
            else:
                second_date = form.cleaned_data['second_date']

            date = first_date
            while date <= second_date:
                new_s = Session()
                new_s.subject = form.cleaned_data['subject']
                new_s.timetable = form.cleaned_data['timetable']
                new_s.session_number = form.cleaned_data['session_number']
                new_s.date = date
                new_s.save()
                date += datetime.timedelta(7)

            return HttpResponseRedirect('/tafe/')

    else:
        form = SessionRecurringForm()
    return render_to_response('tafe/session_create.html',{'form':form}, RequestContext(request))

@login_required
def session_view(request, year, month, day, slug):
    ''' Show the details of the session '''
    req_date = datetime.date(int(year), int(month), int(day))
    session = get_object_or_404(Session, slug=slug, date=req_date)
    '''moving attendance record creation to here from convert_to_student in models'''
    for student in session.subject.students.all():
        new_attendance, created = StudentAttendance.objects.get_or_create(session=session,student=student, last_change_by=request.user)
    student_attendance = StudentAttendance.objects.filter(session=session)
    staff_member = session.subject.staff_member
    staff_attendance = StaffAttendance.objects.get_or_create(session=session, staff_member=staff_member, last_change_by=request.user)

    return render_to_response('tafe/session_detail.html',{'session':session, 'student_attendance':student_attendance, 'staff_attendance':staff_attendance}, RequestContext(request))

@login_required
def session_attendance_view(request, year, month, day, slug):
    req_date = datetime.date(int(year), int(month), int(day))
    session = get_object_or_404(Session, slug=slug, date=req_date)
    StaffAttendanceFormSet = modelformset_factory(StaffAttendance, fields = ('staff_member', 'reason', 'absent'), extra=0)
    StudentAttendanceFormSet = modelformset_factory(StudentAttendance, fields = ('student', 'reason', 'absent'))
    if request.method == 'POST':
        student_formset = StudentAttendanceFormSet(request.POST, queryset=StudentAttendance.objects.filter(session=session), prefix='students')
        staff_formset = StaffAttendanceFormSet(request.POST, prefix='staff')
        if student_formset.is_valid():
            student_formset.save()
        if staff_formset.is_valid():
            staff_formset.save()
    else:
        student_formset = StudentAttendanceFormSet(queryset=StudentAttendance.objects.filter(session=session).order_by('student'), prefix='students')
        staff_formset = StaffAttendanceFormSet(prefix='staff')
        return render_to_response('tafe/attendance_record.html',{'student_formset':student_formset, 'staff_formset':staff_formset, 'session':session,}, RequestContext(request))

############### Units ###############

@login_required
def units_by_qualifications_view(request):
    ''' Show all units or Subjects available for this Course'''
    courses = Course.objects.all().order_by('name')
    return render_to_response('tafe/units_by_qualifications.html',{'courses':courses})

@login_required
def unit_view(request, slug):
    unit = get_object_or_404(Subject, slug=slug)
    unit_students = unit.students.all()
    unit_attendance_matrix = []
    weekly_classes = [] 
    dates = []
    
    '''We need to get the headers for each session - date and session_number for the attendance record header row'''
    for session in Session.objects.filter(subject=unit).order_by('date'):
        date = session.date
        session_number = session.get_session_number_display()
        session_details = [date, session_number]
        dates.append(session_details)

    '''Add each student and their attendance record, per session, to the matrix'''
    for student in unit_students:
        '''the student is the first item in the list'''
        student_details = [student]
        all_sessions = Session.objects.filter(subject=unit, students=student).order_by('date')
        '''then add the attendance reason from each session in date order'''
        for session in all_sessions:
            attendance_records = StudentAttendance.objects.filter(student=student, session=session).order_by('session')
            for attendance_record in attendance_records:   
                if today < session.date:
                    student_details.append('-')
                else:
                    student_details.append(attendance_record.reason)
        unit_attendance_matrix.append(student_details)
    
    return render_to_response('tafe/unit_detail.html', {'unit':unit,'unit_attendance_matrix':unit_attendance_matrix, 'dates':dates, 'weekly_classes':weekly_classes}, RequestContext(request))

############### Applicants ###############

@login_required
def applicant_success(request):
    ''' All successful applicants will be turned into Student objects '''
    if request.method=='POST':
        form = ApplicantSuccessForm(request.POST)
        if form.is_valid():
            '''for each applicant, transfer the data across to a Student model'''
            applicants = form.cleaned_data['applicants']
            for applicant in applicants:
                applicant.convert_to_student()
            
            return render_to_response('tafe/applicants_to_students.html', {'applicants':applicants}, RequestContext(request))
        else:
            pass
    else:
        form = ApplicantSuccessForm()

    return render_to_response('tafe/applicant_success.html', {'form':form}, RequestContext(request))

############### Timetables ###############

@login_required
def timetable_daily_view(request, year, month, day):
    ''' Today's timetable  '''
    daily_sessions = []
    date = datetime.date(int(year), int(month), int(day))

    for session in range(4):
        daily_sessions.append([])
        daily_sessions[session] = Session.objects.filter(date=date).filter(session_number=session)

    return render_to_response('tafe/timetable_daily_detail.html',{'daily_sessions':daily_sessions, 'date':date}, RequestContext(request))

@login_required
def timetable_weekly_view(request, slug):
    '''
    View of this week's timetable. 
    '''
    timetable = get_object_or_404(Timetable, slug=slug)
    all_sessions = []
    
    last_monday = today - datetime.timedelta(days=today.weekday())

    ''' For each day of the week '''
    for day in range(5):
        ''' To show the timetable for this week we get the date of this week's  Monday '''        
        weekday = last_monday + datetime.timedelta(day)
        ''' all sessions is the dataset returned to the template'''
        all_sessions.append([])
        ''' weekdays is the daily list of sessions '''
        weekdays = []
        ''' for each session of the day '''
        for session_choice in range(5):
            weekdays.append([])
            ''' retrieve what's on '''
            sessions = timetable.sessions.filter(date=weekday).filter(session_number=session_choice)
            ''' add each session in the list to the daily schedule list for that session'''
            for session in sessions:
                weekdays[session_choice].append(session)
        ''' add the just completed day of four sessions to the all_sessions list '''
        all_sessions[day].append(weekdays)

    return render_to_response('tafe/timetable_weekly_detail.html',{'timetable':timetable,'all_sessions':all_sessions}, RequestContext(request))

############### Assessments ###############

@login_required
def assessment_view(request, unit, slug):
    subject = get_object_or_404(Subject, slug=unit)
    assessment = get_object_or_404(Assessment, slug=slug, subject=subject) 

    return render_to_response('tafe/assessment_detail.html',{'assessment':assessment,}, RequestContext(request))

############### Students ###############

@login_required
def student_reports(request, year=None):
    year = year or datetime.date.today().year
    courses = Course.objects.filter(year=year)
    course_stats ={}
    stats = {}
    for course in courses:
        name = course.__unicode__()
        enrolled_m = course.students.filter(gender='M')
        enrolled_f = course.students.filter(gender='F')

        course_stats['1 coursename'] = name
        course_stats['2 enrolled'] = course.students.all().count()
        course_stats['2 enrolled_m'] = enrolled_m.count() 
        course_stats['2 enrolled_f'] = enrolled_f.count()
            
        ## Students: 16-24, gender diff'd ##
        ## date for those who are 25 today ##
        dob_for_25 = today-relativedelta(years=25) 
        course_stats['3 enrolled_24m'] = enrolled_m.filter(dob__lte=dob_for_25).count()
        course_stats['3 enrolled_24f'] = enrolled_f.filter(dob__lte=dob_for_25).count()
        course_stats['3 enrolled_24'] = course_stats['3 enrolled_24m'] + course_stats['3 enrolled_24f']
        
        ## Students: 25+, gender diff'd ##
        course_stats['4 enrolled_25m'] = course_stats['2 enrolled_m'] - course_stats['3 enrolled_24m'] 
        course_stats['4 enrolled_25f'] = course_stats['2 enrolled_f'] - course_stats['3 enrolled_24f'] 
        course_stats['4 enrolled_25'] = course_stats['2 enrolled'] - course_stats['3 enrolled_24']

        ## Students: Outer Islands, gender diff'd ##
        course_stats['5 outer_m'] = enrolled_m.exclude(island = '01').count() # 01 is Tarawa
        course_stats['5 outer_f'] = enrolled_f.exclude(island = '01').count() # 01 is Tarawa
        course_stats['5 outer'] = course_stats['5 outer_m'] + course_stats['5 outer_f']

        ## Students: Disability, gender diff'd ##
        course_stats['6 disability_m'] = enrolled_m.filter(disability='True').count()
        course_stats['6 disability_f'] = enrolled_f.filter(disability='True').count()
        course_stats['6 disability'] = course_stats['6 disability_m'] + course_stats['6 disability_f']
    
        stats[name] = course_stats

    return render_to_response('tafe/student_reports.html',{'course_stats':course_stats,'stats':stats},RequestContext(request))
