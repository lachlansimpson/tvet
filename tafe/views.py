# Create your views here.

from tafe.models import Subject, Timetable
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


wnames = ""
wnames = wnames.split()

@login_required
def index(request):
    """ 
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    todays_subject_list = Subject.today.all()
    return render_to_response('tafe/index.html', {'todays_subject_list': todays_subject_list})

@login_required
def timetable_view(request, slug):
    timetable = get_object_or_404(Timetable, slug=slug)
    all_sessions = [[]]
    weekdays = [[]]
    session_numbers=[]
    if timetable.start_date.weekday() == 0:
        first_monday_in_term = timetable.start_date
    else:    
        first_monday_in_term = timetable.start_date + datetime.timedelta(7 - timetable.start_date.weekday())

    ''' 
    The following gets a timetable's first full week of classes to use as a template for the visual timetable
    We will not render date fields on objects so as to generalise. The Timetable will have days of the week
    as columns, and sessions as rows. Each cell will have the list of subjects that are on at that day/time.
    For each of the session_choices: morning1, morning2, afternoon1, afternoon2 we want to make a row in the 
    template, in each row we will have a cell per day. In every cell a list of sessions
    '''
    for session_choice in range(0,4):
        '''
        for each of the days of the week, we will make a column within that row 
        '''
        session_numbers.append(session_choice)
        for day in range(0,5):
            ''' set the day of the week '''
            weekday = first_monday_in_term + datetime.timedelta(day)
            '''get a list of every session for that day and filter by the session_choice we have'''
            daily_sessions = timetable.sessions.filter(date=weekday).filter(session_number=session_choice)
            '''append the list to the day of the week list per day'''
            weekdays[day].append(daily_sessions)
            '''append the day of the week list to all_sessions per session_choice'''
            all_sessions[session_choice].append(weekdays[day])
            
            if len(weekdays) < 7:
                weekdays.append([])
        
        all_sessions.append([])

    return render_to_response('tafe/timetable_detail.html',{'timetable':timetable,'all_sessions':all_sessions})

'''
@login_required
def timetable(request, year=None, term=None):
    if year: year = int(year)
    else:    year = datetime.date.today().year
'''
