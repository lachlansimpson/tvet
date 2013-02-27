# Create your views here.

from tafe.models import EDUCATION_LEVEL_CHOICES
from tafe.models import Timetable, Session, Course, StudentAttendance, Subject, Assessment, StaffAttendance, Applicant, Student, Enrolment, Result, Grade
from tafe.forms import SessionRecurringForm, ApplicantSuccessForm, ReportRequestForm, TimetableAddSessionForm, AssessmentAddForm, ResultForm
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import modelformset_factory, inlineformset_factory
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
    
    class_day = True

    for session in range(4):
        daily_sessions.append([])
        daily_sessions[session] = Session.objects.filter(date=today).filter(session_number=session)
        class_day = len(daily_sessions[session])
        #if (not empty_day) and len(daily_sessions[session])!=0:
        #  empty_day = False
    
    if not class_day:
      return render_to_response('tafe/timetable_empty.html',{}, RequestContext(request))
    else:
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
    for student in session.subject.students.filter(enrolments__withdrawal_reason=''):
        new_attendance, created = StudentAttendance.objects.get_or_create(session=session,student=student, last_change_by=request.user)
    student_attendance = StudentAttendance.objects.filter(session=session)
    staff_member = session.subject.staff_member
    if staff_member is not None:
        staff_attendance, created = StaffAttendance.objects.get_or_create(session=session, staff_member=staff_member, last_change_by=request.user)
    else:
        staff_attendance = {}

    return render_to_response('tafe/session_detail.html',{'session':session, 'student_attendance':student_attendance, 'staff_attendance':staff_attendance}, RequestContext(request))

@login_required
def session_attendance_view(request, year, month, day, slug):
    ''' Shows the session, students and staff - for marking attendance.
    '''
    req_date = datetime.date(int(year), int(month), int(day))
    # Don't allow attendance to be marked for classes that haven't happened yet 
    if req_date > today:
        return HttpResponseRedirect('/tafe/session/%s/%s/%s/%s/' %(year,month,day,slug))
    session = get_object_or_404(Session, slug=slug, date=req_date)
    StaffAttendanceFormSet = modelformset_factory(StaffAttendance, fields = ('staff_member', 'reason', 'absent'), extra=0)
    StudentAttendanceFormSet = modelformset_factory(StudentAttendance, fields = ('student', 'reason', 'absent'), extra=0)
    if request.method == 'POST':
        student_formset = StudentAttendanceFormSet(request.POST, queryset=StudentAttendance.objects.filter(session=session), prefix='students')
        staff_formset = StaffAttendanceFormSet(request.POST, prefix='staff')
        if student_formset.is_valid():
            student_formset.save()
        if staff_formset.is_valid():
            staff_formset.save()
        return HttpResponseRedirect('/tafe/session/%s/%s/%s/%s/' %(year,month,day,slug))

    else:
        student_formset = StudentAttendanceFormSet(queryset=StudentAttendance.objects.filter(session=session).order_by('student'), prefix='students')
        staff_formset = StaffAttendanceFormSet(queryset=StaffAttendance.objects.filter(session=session), prefix='staff')
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
    sessions = []
    assessments = []

    '''We need to get the headers for each session - date and session_number for the attendance record header row'''
    for session in unit.sessions.all().order_by('date'):
        sessions.append(session)
    for assessment in unit.assessments.all().order_by('date_due'): 
        assessments.append(assessment)

    '''Add each student and their attendance record, per session, to the matrix'''
    for student in unit_students:
        '''the student is the first item in the list'''
        student_details = [student]
            
        all_sessions = unit.sessions.all().order_by('date')
        
        '''then add the attendance reason from each session in date order'''
        for session in all_sessions:
            # Sessions after today are marked -
            if today < session.date:
                 student_details.append('-')
            elif StudentAttendance.objects.filter(session=session).filter(student=student).exists():
                attendance_record = StudentAttendance.objects.get(student=student,session=session) 
                student_details.append(attendance_record.reason)
            # if it's not in the future or a Session doesn't exist, then they are withdrawn
            elif Enrolment.objects.get(student=student, course__subjects=unit).mark=='W':
                student_details.append('W')
            else:
                student_details.append('NA')
        student_details.append('|')
        results = Result.objects.filter(grade__student=student,grade__subject=unit)
        for result in results:
            student_details.append(result.mark)
                
        unit_attendance_matrix.append(student_details)
    
    return render_to_response('tafe/unit_detail.html', {'unit':unit,'unit_attendance_matrix':unit_attendance_matrix, 'sessions':sessions, 'assessments':assessments}, RequestContext(request))

############### Students ###############
@login_required
def student_qualification(request):
    ''' All students will be listed by qualification '''
    enrolments = Enrolment.objects.filter(date_started__year=today.year).order_by('course__name')
    
    return render_to_response('tafe/student_qualifications.html', {'enrolments':enrolments}, RequestContext(request))

@login_required
def student_qualification_csv(request):
    ''' All students will be listed by qualification and output as csv'''
    courses = Course.objects.filter(year=today.year)
  
    students_by_course = SortedDict()
    for course in courses:
      if course.students.all().count()==0:
        continue
      students = []
      students.append(('First Name','Surname','Gender','Date of Birth','Address','Start date'))
      for student in course.students.all():
        students.append((student.first_name, student.surname, student.get_gender_display(), student.dob, student.address, student.enrolments.get(course=course).start_date))
      coursename = course.__unicode__()
      students_by_course[coursename] = students
    
    filename = '%s_students.csv' %(today.year)
    return students_list_csv_export(students_by_course,filename) 

def students_list_csv_export(students_by_course, filename):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    writer = csv.writer(response)
    for key, value in students_by_course.items():
        table = (str(key),)
        writer.writerow(table)
        for student in value:
          writer.writerow(student)
        writer.writerow("")
    return response


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

@login_required
def applicant_shortlist(request):
    ''' All applicants will be listed by qualification '''
    applicants = Applicant.all_short_listed.all()
    
    return render_to_response('tafe/applicant_shortlist.html', {'applicants':applicants}, RequestContext(request))

@login_required
def applicant_qualification(request):
    ''' All applicants will be listed by qualification '''
    applicants = Applicant.current.all().order_by('applied_for')
    courses = Course.objects.all().order_by('name')

    ''' This adds the courses and applicants to a dictionary '''
    apps_by_course = {}
    for course in courses:
      course_applicants = [] 
      for applicant in applicants:
        if applicant.applied_for == course:
          course_applicants.append(applicant)
      apps_by_course[course] = course_applicants
   
    ''' This sorts the dictionary for rendering in alphabetical order by the template '''
    key_list = apps_by_course.keys()
    key_list.sort()
    applicants_by_course = SortedDict()
    for key in key_list:
        applicants_by_course[key] = apps_by_course[key]

    return render_to_response('tafe/applicant_qualifications.html', {'applicants_by_course':applicants_by_course}, RequestContext(request))

@login_required
def applicant_shortlist_qualification(request):
    ''' All applicants will be listed by qualification '''
    applicants = Applicant.all_short_listed.all().order_by('applied_for')
    courses = Course.objects.all().order_by('name')

    applicants_by_course = {}
    for course in courses:
      course_applicants = [] 
      for applicant in applicants:
        if applicant.applied_for == course:
          course_applicants.append(applicant)
      if len(course_applicants)==0:
        continue
      applicants_by_course[course] = course_applicants
    
    return render_to_response('tafe/applicant_shortlist_qualifications.html', {'applicants_by_course':applicants_by_course}, RequestContext(request))
############### Timetables ###############

def generate_dates(start_date, end_date):
    td = datetime.timedelta(days=7)
    current_date = start_date
    list_dates = []

    while current_date <= end_date:
        list_dates.append(current_date)
        current_date += td

    return list_dates

@login_required
def add_sessions_view(request, slug):
    timetable = get_object_or_404(Timetable, slug=slug)
    SessionFormset = modelformset_factory(Session, fields = ('subject', 'room_number'), max_num=13, extra=1)

    if request.method == 'POST':
        form = TimetableAddSessionForm(request.POST) 
        formset = SessionFormset(request.POST)
        if form.is_valid():
            session_choice = form.cleaned_data['session_choice']
            session_day = int(form.cleaned_data['day_choice'])
            first_session_date = timetable.start_date + datetime.timedelta(days=session_day)
            dates = generate_dates(first_session_date, timetable.end_date)
        if formset.is_valid():
            for smallform in formset.cleaned_data:
                for date in dates:
                  newsession = Session()
                  newsession.session_number = session_choice
                  newsession.timetable = timetable
                  newsession.subject = smallform['subject']
                  newsession.room_number = smallform['room_number']
                  newsession.date = date
                  newsession.save()
            
        return HttpResponseRedirect('/tafe/timetable/%s' %(timetable.slug))
    else:
        form = TimetableAddSessionForm()
        formset = SessionFormset(queryset=Session.objects.none())
    return render_to_response('tafe/timetable_add_session.html',{'form':form, 'formset':formset, 'timetable':timetable,}, RequestContext(request))


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
def timetable_weekly_view(request, slug, year=None, month=None, day=None):
    '''
    View of this week's timetable. 
    '''
    year = year or datetime.date.today().year
    month = month or datetime.date.today().month
    day = day or datetime.date.today().day
    start_date = datetime.date(int(year), int(month), int(day))
    
    timetable = get_object_or_404(Timetable, slug=slug)
    all_sessions = []
    
    monday = start_date - datetime.timedelta(days=start_date.weekday())

    ''' For each day of the week '''
    for day in range(5):
        ''' To show the timetable for this week we get the date of this week's Monday '''        
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
def assessment_mark_single(request, unit, assessment, student):
    subject = get_object_or_404(Subject, slug=unit)
    assessment = get_object_or_404(Assessment, slug=assessment)
    student = get_object_or_404(Student, slug=student)
    grade = get_object_or_404(Grade, student=student, subject=subject)
    user = request.user
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            newResult = Result()
            newResult.grade = grade
            newResult.assessment = assessment
            newResult.date_submitted = form.cleaned_data['date_submitted']
            newResult.mark = form.cleaned_data['mark']
            newResult.last_change_by = user
            newResult.save()
            return HttpResponseRedirect(assessment.get_absolute_url())
        else:
            pass
    else:
        form = ResultForm()
    return render_to_response('tafe/result_single_form.html', {'form':form}, RequestContext(request))

@login_required
def assessment_mark_all(request, unit, slug):
    user = request.user
    subject = get_object_or_404(Subject, slug=unit)
    assessment = get_object_or_404(Assessment, slug=slug)
    ResultFormSet = inlineformset_factory(Assessment, Result,form=ResultForm)
    ResultFormSet.form.base_fields['grade'].queryset = Grade.objects.filter(subject=subject)
    if assessment.subject.id != subject.id:
        return HttpResponseRedirect('/tafe/404.html')
    if request.method=='POST':    
        formset = ResultFormSet(request.POST, instance=assessment)
        if formset.is_valid():        
            results = formset.save(commit=False) 
            for result in results: 
                result.last_change_by = user
                result.save()
            return HttpResponseRedirect(assessment.get_absolute_url())
        else:
            pass
    else: 
        formset = ResultFormSet(instance=assessment)
    return render_to_response('tafe/result_all_form.html', {'assessment':assessment, 'formset':formset}, RequestContext(request))

@login_required
def unit_add_assessment_view(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    if request.method=='POST':
        form = AssessmentAddForm(request.POST)
        if form.is_valid():
            newAssessment = Assessment()
            newAssessment.name = form.cleaned_data['name']
            newAssessment.date_given = form.cleaned_data['date_given']
            newAssessment.date_due = form.cleaned_data['date_due']
            newAssessment.subject = subject 
            newAssessment.slug = slugify(newAssessment.name)
            newAssessment.save()
            return HttpResponseRedirect('/tafe/unit/%s/' % (newAssessment.subject.slug))
        else:
            pass
    else:
        form = AssessmentAddForm()

    return render_to_response('tafe/assessment_add_form.html', {'form':form}, RequestContext(request))

@login_required
def assessment_view(request, unit, slug):
    ''' An Assessment's details '''
    subject = get_object_or_404(Subject, slug=unit)
    assessment = get_object_or_404(Assessment, slug=slug, subject=subject) 
    grades_no_results = Grade.objects.filter(subject=subject).exclude(results=assessment)

    return render_to_response('tafe/assessment_detail.html',{'assessment':assessment, 'grades_no_results':grades_no_results}, RequestContext(request))

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
    queryset = Applicant.objects.filter(applied_for__year__exact=year)
    
    if queryset.count()==0: # If there are no objects in the queryset... 
        return render_to_response('tafe/applicants_report.html',{},RequestContext(request))
    if format=='raw': # If raw is required, no stats needed. Return raw queryset data
        return raw_csv_export(queryset)
    else: # we need to make the stats
        stats = SortedDict()
        others = SortedDict() 
        others['All'] = other_stats(queryset)
        stats['All'] = total_stats(queryset) 
        courses = Course.objects.filter(year=year)
        for course in courses: 
            name = course.__unicode__()
            queryset = course.applicants.all()
            if queryset.count()==0:
                continue
            stats[name] = total_stats(queryset)
        
        if format == 'csv': # test to see if CSV dump of stats is wanted  
            filename = '%s_%s_stats.csv' %(slugify(queryset.model.__name__),year)
            return stats_csv_export(stats,filename)
        else: # format == 'html'
            return render_to_response('tafe/applicants_report.html',{'stats':stats, 'others':others}, RequestContext(request))        

@login_required
def student_reports(request, year=None, format=None):
    '''
    View returns the statistics on # of Enrolments, diff'd on gender across age ranges (16-24, 25+)
    Island and disability. Stats considered per course and overall
    '''
    year = year or datetime.date.today().year
    queryset = Student.objects.filter(enrolments__course__year__exact=year, enrolments__mark__exact='') 
    sponsored_qs = Student.sponsored_students.all()
    
    if queryset.count()==0:
       return render_to_response('tafe/student_reports.html',{},RequestContext(request))
    if format == 'raw':
        return raw_csv_export(queryset)
    else:    
        stats = SortedDict()
        others = SortedDict() 
        sponsored = SortedDict()
        sponsored['All'] = sponsored_stats(sponsored_qs)
        others['All'] = other_stats(queryset)
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
            return render_to_response('tafe/student_reports.html',{'stats':stats, 'others':others, 'sponsored':sponsored}, RequestContext(request))

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

def sponsored_stats(queryset):
    queryset_m = queryset.filter(gender = 'M')
    queryset_f = queryset.filter(gender = 'F')
    spons_stats = SortedDict() 

    a = queryset.values('address').distinct()
    m = queryset_m.values('address').distinct()
    f = queryset_f.values('address').distinct()

    spons_stats['Addresses'] = (f,m,a)
    return spons_stats

def other_stats(queryset):
    queryset_m = queryset.filter(gender = 'M')
    queryset_f = queryset.filter(gender = 'F')
    misc_stats = SortedDict() 

    for number,level in EDUCATION_LEVEL_CHOICES:
        a=queryset.filter(education_level=number).count()
        m=queryset.filter(education_level=number,gender='M').count()
        f=queryset.filter(education_level=number,gender='F').count()
        misc_stats[level] = (f,m,a)

    return misc_stats

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
