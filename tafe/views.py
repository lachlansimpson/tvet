# Create your views here.

from tafe.models import Subject, Timetable, Session
from tafe.forms import SessionRecurringForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime

@login_required
def index(request, date):
    """ 
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    todays_subject_list = Subject.today.all()
    return render_to_response('tafe/index.html', {'todays_subject_list': todays_subject_list})

@login_required
def timetable_weekly_view(request, slug):
    timetable = get_object_or_404(Timetable, slug=slug)
    all_sessions = []

    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())

    ''' For each day of the week '''
    for day in range(5):
        weekday = last_monday + datetime.timedelta(day)
        all_sessions.append([])
        ''' weekdays is the daily list of sessions '''
        weekdays = []
        ''' for each session of the day '''
        for session_choice in range(5):
            weekdays.append([])
            ''' retrieve what's on '''
            sessions = timetable.sessions.filter(date=weekday).filter(session_number=session_choice)
            ''' add it to the daily schedule list '''
            weekdays[session_choice].append(sessions)
            ''' add the just completed day of four sessions to the all_sessions list '''
        all_sessions[day].append(weekdays)

    return render_to_response('tafe/timetable_weekly_detail.html',{'timetable':timetable,'all_sessions':all_sessions})

@login_required
def session_create(request):
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
                return HttpResponseRedirect('/')

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

            return HttpResponseRedirect('')

    else:
        form = SessionRecurringForm()
    return render_to_response('tafe/session_create.html',{'form':form}, RequestContext(request))
"""
@login_required
def timetable_daily_view(request,year,month,day):
    timetable = get_object_or_404(Timetable, slug=slug)
    daily_sessions = []
    if not (year && month && day):
        date = date.datetime.today()

    for session in range(4):
        daily_sessions.append([])
        daily_sessions[session] = timetable.sessions.filter(date=date).filter(session_number=session)

    return render_to_response('tafe/timetable_daily_detail.html',{'timetable':timetable,'daily_sessions':daily_sessions, 'date':date})
"""
""" OLD WEEK VIEW
''' Get the first Monday of the Timetable/Semester '''
if timetable.start_date.weekday() == 0:
    first_monday_in_term = timetable.start_date
else:    
    first_monday_in_term = timetable.start_date + datetime.timedelta(7 - timetable.start_date.weekday())



    ''' For each day of the week '''
    for day in range(5):
        weekday = first_monday_in_term + datetime.timedelta(day)
        ''' weekdays is the daily list of sessions '''
        weekdays = [[]]
        ''' for each session of the day '''
        for session_choice in range(5):
            ''' retrieve what's on '''
            sessions = timetable.sessions.filter(date=weekday).filter(session_number=session_choice)
            ''' add it to the daily schedule list '''
            weekdays[session_choice].append(sessions)
            if session_choice < 4:
                weekdays.append([])
                ''' add the just completed day of four sessions to the all_sessions list '''
                all_sessions[day].append(weekdays)
                if day < 4:
                    all_sessions.append([])

    return render_to_response('tafe/timetable_detail.html',{'timetable':timetable,'all_sessions':all_sessions})
"""  
