''' forms.py holds the new forms for creating objects '''
from django import forms
from tafe.models import Timetable, Subject
from tafe.models import SESSION_CHOICES
from django.forms.extras.widgets import SelectDateWidget

class SessionRecurringForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    timetable = forms.ModelChoiceField(queryset=Timetable.objects.all().order_by('-start_date'))
    session_number = forms.ChoiceField(choices=SESSION_CHOICES)
    recurring = forms.BooleanField(required=False, help_text="Does this class happen every week")
    for_semester = forms.BooleanField(required=False, help_text="Will it happen for the whole semester")
    first_date = forms.DateField(help_text="Start date", widget = SelectDateWidget)
    second_date = forms.DateField(help_text="End date", required=False, widget = SelectDateWidget)
