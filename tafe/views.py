# Create your views here.

from tafe.models import Timetable, Session, Course, StudentAttendance, Subject, Assessment, StaffAttendance, Applicant, Student
from tafe.forms import SessionRecurringForm, ApplicantSuccessForm, ReportRequestForm
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.template.defaultfilters import slugify
from dateutil.relativedelta import *
import csv

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
    if staff_member is not None:
        staff_attendance = StaffAttendance.objects.get_or_create(session=session, staff_member=staff_member, last_change_by=request.user)
    else:
        staff_attendance = {}

    return render_to_response('tafe/session_detail.html',{'session':session, 'student_attendance':student_attendance, 'staff_attendance':staff_attendance}, RequestContext(request))

@login_required
def session_attendance_view(request, year, month, day, slug):
    ''' Shows the session, students and staff - for marking attendance.
    TODO: Check to see if this is still used
    '''
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
    return render_to_response('tafe/units_by_qualifications.html',{'courses':courses}, RequestContext(request))

@login_required
def unit_view(request, slug):
    '''
    Shows a Unit's details, along with the student attendance per session and grades
    TODO: append the grade of each student to the graph
    '''
    unit = get_object_or_404(Subject, slug=slug)
    unit_students = unit.students.all()
    unit_attendance_matrix = []
    weekly_classes = [] 
    sessions = []
    
    '''We need to get the headers for each session - date and session_number for the attendance record header row'''
    for session in Session.objects.filter(subject=unit).order_by('date'):
        sessions.append(session)

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
    
    return render_to_response('tafe/unit_detail.html', {'unit':unit,'unit_attendance_matrix':unit_attendance_matrix, 'sessions':sessions, 'weekly_classes':weekly_classes}, RequestContext(request))

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
    start_date = timetable.start_date
    
    monday = start_date - datetime.timedelta(days=start_date.weekday())

    ''' For each day of the week '''
    for day in range(5):
        ''' To show the timetable for this week we get the date of this week's  Monday '''        
        weekday = monday + datetime.timedelta(day)
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
    ''' An Assessment's details '''
    subject = get_object_or_404(Subject, slug=unit)
    assessment = get_object_or_404(Assessment, slug=slug, subject=subject) 

    return render_to_response('tafe/assessment_detail.html',{'assessment':assessment,}, RequestContext(request))

############### Reports ###############

@login_required
def reports(request):
    '''
    GETs a year and report subject (Applicants, Students, Enrolments, Staff) and POSTS
    the relevant report
    '''
    if request.method=='POST':
        form = ReportRequestForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            data_type = form.cleaned_data['data_type']
            data_output = form.cleaned_data['data_output']
            return HttpResponseRedirect('/tafe/report/%s/%s/%s/' % (data_type, year, data_output))
        else:
            pass
    else:
        form = ReportRequestForm()

    return render_to_response('tafe/reports.html', {'form':form}, RequestContext(request))

@login_required
def applicant_reports(request, year=None, format=None):
    '''
    View returns the statistics on # of applicants, diff'd on gender across age ranges (16-24, 25+)
    Island and disability. Stats considered per course and overall
    '''
    year = year or datetime.date.today().year
    format = format or 'html'
    queryset = Applicant.objects.filter(applied_for__year__exact=year).exclude(successful=1)
    
    if queryset.count()==0: # If there are no objects in the queryset... 
        return render_to_response('tafe/applicants_report.html',{},RequestContext(request))
    if format=='raw': # If raw is required, no stats needed. Return raw queryset data
        return raw_csv_export(queryset)
    else: # we need to make the stats
        stats = SortedDict() 
        stats['All'] = total_stats(queryset) 
        
        courses = Course.objects.filter(year=year)
        for course in courses: 
            name = course.__unicode__()
            queryset = course.applicants.exclude(successful=1).exclude(successful=0)
            if queryset.count()==0:
                continue
            stats[name] = total_stats(queryset)
        
        if format == 'csv': # test to see if CSV dump of stats is wanted  
            filename = '%s_%s_stats.csv' %(slugify(queryset.model.__name__),year)
            return stats_csv_export(stats,filename)
        else: # format == 'html'
            return render_to_response('tafe/applicants_report.html',{'stats':stats}, RequestContext(request))        

@login_required
def student_reports(request, year=None, format=None):
    '''
    View returns the statistics on # of Enrolments, diff'd on gender across age ranges (16-24, 25+)
    Island and disability. Stats considered per course and overall
    '''
    year = year or datetime.date.today().year
    queryset = Student.objects.filter(enrolments__course__year__exact=year) 
    
    if queryset.count()==0:
       return render_to_response('tafe/student_reports.html',{},RequestContext(request))
    if format == 'raw':
        return raw_csv_export(queryset)
    else:    
        stats = SortedDict()  
        stats['All'] = total_stats(queryset) 
        courses = Course.objects.filter(year=year)
        for course in courses:
            name = course.__unicode__() 
            queryset = course.students.all()
            if queryset.count()==0:
                continue
            stats[name] = total_stats(queryset)
       
        ''' test to see if CSV dump is wanted''' 
        if format == 'csv':
            filename = '%s_%s_stats.csv' %(slugify(queryset.model.__name__),year)
            return stats_csv_export(stats,filename)
        else:     #if not a CSV dump, send to web  
            return render_to_response('tafe/student_reports.html',{'stats':stats},RequestContext(request))

def stats_csv_export(stats, filename):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    writer = csv.writer(response)
    for key, value in stats.items():
        table = (str(key),)
        writer.writerow(table)
        writer.writerow(value.keys())
        writer.writerow(value.values())

    return response

def raw_csv_export(queryset):
    model = queryset.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    # Write headers to CSV file
    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in queryset:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def total_stats(queryset):
    queryset_m = queryset.filter(gender = 'M')
    queryset_f = queryset.filter(gender = 'F')
    totals = SortedDict()
    ## Stats for all queryset ##
    totals['queryset'] = queryset.count()    
    totals['queryset_m'] = queryset_m.count() 
    totals['queryset_f'] = queryset_f.count()
    totals['queryset_m_pc'] = totals['queryset_m']*100/totals['queryset']
    totals['queryset_f_pc'] = totals['queryset_f']*100/totals['queryset']
        
    ## 16-24, gender diff'd ##
    dob_for_25 = today-relativedelta(years=25) # date for those who are 25 today  
    totals['queryset_24m'] = queryset_m.filter(dob__lte=dob_for_25).count()
    totals['queryset_24f'] = queryset_f.filter(dob__lte=dob_for_25).count()
    totals['queryset_24'] = totals['queryset_24m'] + totals['queryset_24f']
    if totals['queryset_24']==0:
        totals['queryset_24_pc'] = totals['queryset_24m_pc'] = totals['queryset_24f_pc'] = 0 
    else:    
        totals['queryset_24_pc'] = totals['queryset_24']*100/totals['queryset']
        totals['queryset_24m_pc'] = totals['queryset_24m']*100/totals['queryset_24']
        totals['queryset_24f_pc'] = totals['queryset_24f']*100/totals['queryset_24']
    
    ## 25+, gender diff'd ##
    totals['queryset_25m'] = queryset_m.filter(dob__gt=dob_for_25).count()
    totals['queryset_25f'] = queryset_f.filter(dob__gt=dob_for_25).count()
    totals['queryset_25'] = totals['queryset_25m'] + totals['queryset_25f']
    if totals['queryset_25']==0:
        totals['queryset_25m_pc'] = totals['queryset_25f_pc'] = totals['queryset_25_pc'] = 0 
    else:
        totals['queryset_25m_pc'] = totals['queryset_25m']*100/totals['queryset_25']
        totals['queryset_25f_pc'] = totals['queryset_25f']*100/totals['queryset_25'] 
        totals['queryset_25_pc'] = totals['queryset_25']*100/totals['queryset']

    ## Outer Islands, gender diff'd ##
    totals['outer_m'] = queryset_m.exclude(island = '01').count() # 01 is Tarawa
    totals['outer_f'] = queryset_f.exclude(island = '01').count() # 01 is Tarawa
    totals['outer'] = totals['outer_m'] + totals['outer_f']
    if totals['outer'] == 0:
        totals['outer_m_pc'] = totals['outer_f_pc'] = totals['outer_pc'] = 0
    else:
        totals['outer_m_pc'] = totals['outer_m']*100/totals['outer'] 
        totals['outer_f_pc'] = totals['outer_f']*100/totals['outer']
        totals['outer_pc'] = totals['outer']*100/totals['queryset']

    ## Disability, gender diff'd ##
    totals['disability_m'] = queryset_m.filter(disability = 1).count()
    totals['disability_f'] = queryset_f.filter(disability = 1).count()
    totals['disability'] = totals['disability_m'] + totals['disability_f']
    if totals['disability'] == 0:
        totals['disability_m_pc'] = totals['disability_f_pc'] = totals['disability_pc'] = 0
    else:
        totals['disability_m_pc'] = totals['disability_m']*100/totals['disability']
        totals['disability_f_pc'] = totals['disability_f']*100/totals['disability']
        totals['disability_pc'] = totals['disability']*100/totals['queryset']
    
    return totals
