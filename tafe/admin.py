from tafe.models import Student, Course, Subject, Enrolment, Grade, Attendance, SubjectResults, Session, Timetable, Applicant
from django.contrib import admin
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget 
from django.forms.widgets import RadioSelect
import datetime

today = datetime.date.today()
this_year = datetime.date.today().year
BIRTH_YEARS = range(this_year-51, this_year-16)

#class StudentInlineAttendance(admin.TabularInline):
class ApplicantSuccess(admin.TabularInline):
    model = Student
    fields = ('__unicode__','successful')

class StudentInline(admin.StackedInline):
    model = Student

class GradeInline(admin.TabularInline):
    model = Grade

class SubjectInline(admin.StackedInline):
    model = Subject

class AttendanceInline(admin.TabularInline):
    model = Attendance
    template = 'admin/collapsed_tabular_inline.html'

class SubjectResultsInline(admin.StackedInline):
    model = SubjectResults
    template = 'admin/collapsed_tabular_inline.html'

class EnrolmentInline(admin.TabularInline):
    extra = 1    
    model = Enrolment

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    fields = ('date', 'session_number',)
    template = 'admin/collapsed_tabular_inline.html'

class CourseInline(admin.TabularInline):
    model = Course

class EnrolmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':['student','course','date_started','date_ended','mark']}),
    ]

class ApplicantAdminForm(ModelForm):
    class Meta:
        model = Applicant 
        widgets = {
            'dob': SelectDateWidget(years=BIRTH_YEARS),
            'gender': RadioSelect(),
        }            

class StudentAdminForm(ModelForm):
    class Meta:
        model = Student
        widgets = {
            'dob': SelectDateWidget(years=BIRTH_YEARS),
            'gender': RadioSelect(),
        }            

class StudentAdmin(admin.ModelAdmin):
    inlines = (EnrolmentInline,
               GradeInline,
               AttendanceInline,
              )
    fieldsets = (
        ('Bio', { 'fields':(('first_name','surname'),('dob','gender'), ('island', 'slug'))}),
        ('Contact Information', { 'fields':(('phone','email'),)}),
        ('Other Information', { 'fields':(('disability','disability_description'), 'education_level')}),)
    form = StudentAdminForm
    list_display = ('__unicode__', 'slug', 'gender', 'disability')
    list_filter = ('gender', 'disability')
    ordering = ('-slug',) 
    readonly_fields = ('slug',)

class ApplicantAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Bio', { 'fields':(('first_name','surname'),('dob','gender', 'island'))}),
                ('Contact Information', { 'fields':(('phone','email'),)}),
                ('Other Information', { 'fields':(('disability','disability_description'), 'education_level')}),
                ('Course Applied For', { 'fields':(('applied_for', 'short_listed'),)}),
        ('Test Results', {'fields':(('test_ap','test_ma','test_eng'),)}),
        ('Ranking, Eligibility and Success', {'fields':(('ranking','eligibility','successful'),)}),
        ('Offer details', {'fields':(('date_offer_sent','date_offer_accepted'),)}),
    )
    form = ApplicantAdminForm
    list_display = ('__unicode__', 'gender', 'disability', 'applied_for')
    list_filter = ('gender', 'disability', 'applied_for')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name','year','semester')
    list_filter = ('year', 'semester', 'name')
    model = Subject
    prepopulated_fields = {'slug': ('name','year')}
    inlines = [
        SessionInline,
        GradeInline,
    ]

class CourseAdmin(admin.ModelAdmin):
    inlines = (EnrolmentInline,)
    filter_horizontal = ('subjects',)
    fieldsets = (
        ('', { 'fields':(('name','slug'),)}),
        ('Subjects', { 'fields':('subjects',)}),
    )
    list_display = ('name', 'count_students', 'count_males', 'count_females', 'subjects_available')
    model = Course 
    prepopulated_fields = {'slug': ('name',)}

class GradeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('',{'fields':['student','subject','date_started','results']}),
    ]

class TimetableAdmin(admin.ModelAdmin):
    model = Timetable
    prepopulated_fields = {'slug': ('year','term')}

class SessionAdmin(admin.ModelAdmin):
    list_display = ('day_of_week','date','timetable','subject','get_session_number_display')
    list_filter = ('date','session_number')
    inlines = [
        AttendanceInline,
    ]
    model = Session

admin.site.register(Session, SessionAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Attendance)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Enrolment, EnrolmentAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(SubjectResults)
