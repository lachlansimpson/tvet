# Create your views here.
'''
from tafe.models import Subject
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """ 
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    todays_subject_list = Subject.today.all()
    return render_to_response('tafe/index.html', {'todays_subject_list': todays_subject_list})
'''
