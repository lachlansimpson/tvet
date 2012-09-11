# Create your views here.

from tafe.models import Subject, Timetable
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def index(request):
    """ 
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    todays_subject_list = Subject.today.all()
    return render_to_response('tafe/index.html', {'todays_subject_list': todays_subject_list})

"""
def timetable_daily_view(request,date):
    timetable = get_object_or_404(Timetable, slug=slug)
    daily_sessions = [[]]
    if not date:
        date = date.datetime.today()
        for session in range(4):
            daily_sessions[session] = timetable.sessions.filter(date=date).filter(session_number=session)
            
    return render_to_response('tafe/timetable_daily__detail.html',{'timetable':timetable,'daily_sessions':daily_sessions})
"""

@login_required
def timetable_week_view(request, slug):
    timetable = get_object_or_404(Timetable, slug=slug)
    all_sessions = [[]]
    
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
